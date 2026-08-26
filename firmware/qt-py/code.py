"""
OPT4048 + MAX17048 -> MQTT publisher (own broker, not Adafruit IO)

Publishes CCT, lux, CIE x/y, and battery state as a single JSON payload
over MQTT to a self-hosted Mosquitto broker on DigitalOcean.

Battery temperature safety (Stage 1): a 10k NTC thermistor is wired to the
BQ24074 THERM pin. The charger uses it autonomously to throttle/cut charging
on a hot battery -- the MCU never reads it, so no temperature value appears in
the payload. Loggable temperature is a future Stage 3 job (a *second*,
independent NTC divider into GPIO2/A2); it does not touch the BQ24074.

Hardened for unattended operation: a single network/sensor error never
kills the loop, the connection is re-established automatically, and a
hardware watchdog reboots the board if it ever truly hangs.
"""

import time
import json
import os
import wifi
import socketpool
import board
import digitalio
import microcontroller
import alarm
from watchdog import WatchDogMode
import adafruit_opt4048
from adafruit_opt4048 import Mode, Range
from adafruit_max1704x import MAX17048
import adafruit_minimqtt.adafruit_minimqtt as MQTT

PUBLISH_INTERVAL = 120      # seconds between daytime readings (CALIBRATION: 2min so there's time to walk between sensors/read the meter/enter values; was 30s, revert to 300 for production)
WATCHDOG_TIMEOUT = 90       # board resets if the loop stalls longer than this
WATCHDOG_SLEEP_CHUNK = 10   # feed the watchdog this often while idling between readings
MAX_FAILURES = 5            # consecutive errors before a clean reboot

# --- Synchronised capture ---
# Two units left free-running drift apart by up to a full PUBLISH_INTERVAL,
# depending only on when each happened to boot, which makes side-by-side
# calibration readings hard to pair up. Instead each unit sleeps until the next
# PUBLISH_INTERVAL boundary on the *wall clock*, so every unit captures on the
# same absolute grid (e.g. at :00, :02, :04 past the hour at 120 s) regardless
# of boot time, and re-aligns itself after any reboot or network stall.
# Requires adafruit_ntp.mpy in lib/; without it the board free-runs as before.
SYNC_CAPTURES = True
NTP_HOST = "pool.ntp.org"
NTP_CACHE_SECONDS = 3600    # re-query NTP at most hourly; interpolate in between

# Night power saving. Below NIGHT_LUX_FLOOR the light sits at the sensor's noise
# floor and the colour data is useless (the chromaticity is pure noise), so the
# board deep-sleeps with the radio off. That is the only change that gives an
# order-of-magnitude battery saving; trimming idle draw while connected does
# not, because the always-on radio dominates. The board still wakes every
# NIGHT_INTERVAL for a battery/lux heartbeat (which keeps the overnight
# discharge curve and a grey night band on the grid), and stays connected for
# NIGHT_AWAKE_GRACE seconds around that heartbeat so wireless flashing remains
# catchable at night. Detection is purely from measured lux, so it needs no
# clock, location, or NTP, and it self-adjusts to season and weather.
NIGHT_LUX_FLOOR = 0.1       # lux; below this a reading is treated as true night
NIGHT_INTERVAL = 900        # seconds of deep sleep between night heartbeats (15 min, to catch dawn)
NIGHT_AWAKE_GRACE = 20      # seconds to stay connected around a night heartbeat (for flashing)
SENSOR_ID = os.getenv("SENSOR_ID", "sensor-01")
TOPIC = f"cct-sensor/{SENSOR_ID}/readings"

# --- Over-the-air (OTA) firmware ---
# The board PULLS new code.py from the Droplet, so flashing works from anywhere
# (not just the home LAN): the board makes the outbound HTTPS call, so no port
# forward, VPN, or inbound access to the home network is needed. On each check
# it reads a tiny manifest and downloads only when the server's version is
# newer than the one it last applied. Set OTA_BASE_URL in settings.toml to
# enable it (e.g. "https://your-server.example.com/firmware"); leave it unset to
# disable OTA entirely. OTA_TOKEN is optional and only needed if the server
# sets one. Wireless LAN flashing still works as before, and stays the fast
# path when you are at home.
OTA_BASE_URL = os.getenv("OTA_BASE_URL")
OTA_TOKEN = os.getenv("OTA_TOKEN")
OTA_CHECK_INTERVAL = 900     # seconds between OTA checks while awake (day path)
OTA_VERSION_FILE = "ota_version"  # last-applied integer version, on the flash

# --- Watchdog ---
# If the loop ever blocks longer than WATCHDOG_TIMEOUT (e.g. a network call
# hangs forever), the chip resets itself instead of sitting dead. We "feed"
# it once per loop to say "still alive".
wdt = microcontroller.watchdog
wdt.mode = None  # stop if already running from a previous crash/auto-reload
wdt.timeout = WATCHDOG_TIMEOUT
wdt.mode = WatchDogMode.RESET

# --- Power saving (radio stays always-on; these trim idle draw) ---
# Both are wrapped so a wrong pin/attr name on a firmware update can never crash
# the boot and cost us the wireless-flash path.
#
# 1) Turn off the onboard RGB NeoPixel's power rail. It draws ~1-2 mA even when
#    idle and we never light it.
try:
    _neopixel_power = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
    _neopixel_power.switch_to_output(value=False)
    print("NeoPixel power rail off.")
except Exception as e:
    print("NeoPixel power-off skipped:", e)

# 2) Most aggressive Wi-Fi modem sleep. MIN (modem sleep between the AP's DTIM
#    beacons) is the default; MAX wakes the radio less often for a bit more
#    saving. Fine here: we only publish every few minutes and never rely on
#    low-latency downlink, and the keep-alive is far longer than the interval.
try:
    wifi.radio.power_management = wifi.PowerManagement.MAX
    print("Wi-Fi power management: MAX.")
except Exception as e:
    print("Wi-Fi power_management set skipped:", e)

# --- Sensor setup ---
i2c = board.STEMMA_I2C()
opt4048 = adafruit_opt4048.OPT4048(i2c)
opt4048.mode = Mode.CONTINUOUS
opt4048.range = Range.AUTO
try:
    max17048 = MAX17048(i2c)
    # No quick_start on boot: the MAX17048 is powered from the cell, so it keeps
    # its learned ModelGauge state across MCU reboots. quick_start would discard
    # that and re-guess from instantaneous voltage, which reads high when USB/
    # charger is present. Only quick_start once, manually, on fresh battery swap.
    print("MAX17048 found.")
except Exception as e:
    max17048 = None
    print("MAX17048 not found (battery hardware not connected):", e)
print(f"Sensors configured. Sensor ID: {SENSOR_ID}")
time.sleep(0.5)  # let the first OPT4048 conversion complete

# --- Networking ---
pool = socketpool.SocketPool(wifi.radio)

# HTTPS session for OTA. Built defensively: if adafruit_requests/ssl are missing
# from lib/ (they are separate from the MQTT stack), OTA simply stays disabled
# rather than crashing the boot and costing us the wireless-flash path. Requires
# adafruit_requests.mpy in lib/ (adafruit_connection_manager is already there).
_ota_requests = None
if OTA_BASE_URL:
    try:
        import ssl
        import adafruit_requests
        _ota_requests = adafruit_requests.Session(pool, ssl.create_default_context())
        print("OTA enabled:", OTA_BASE_URL)
    except Exception as e:
        print("OTA disabled (requests/ssl unavailable):", e)

# Wall clock for synchronised capture. Built defensively, exactly like the OTA
# session above: if adafruit_ntp.mpy is missing from lib/ the board simply
# free-runs instead of crashing the boot and costing us the flash path. No
# network call happens here -- adafruit_ntp queries lazily on first use.
_ntp = None
if SYNC_CAPTURES:
    try:
        import adafruit_ntp
        _ntp = adafruit_ntp.NTP(pool, server=NTP_HOST, tz_offset=0,
                                cache_seconds=NTP_CACHE_SECONDS)
        print("Capture sync enabled via", NTP_HOST)
    except Exception as e:
        print("Capture sync disabled (adafruit_ntp unavailable):", e)

mqtt_client = MQTT.MQTT(
    broker=os.getenv("MQTT_BROKER"),       # e.g. "broker.example.com"
    port=1883,
    username=os.getenv("MQTT_USERNAME"),   # e.g. "feather"
    password=os.getenv("MQTT_PASSWORD"),
    socket_pool=pool,
    keep_alive=max(60, PUBLISH_INTERVAL * 3),  # floor at 60s so a short interval cannot thrash MQTT
)


def _wifi_networks():
    """Every configured network, in the order they should be tried.

    CIRCUITPY_WIFI_SSID stays the primary because CircuitPython's own web
    workflow auto-connects to that one at boot, before code.py runs. The
    numbered pairs (CIRCUITPY_WIFI_SSID_2, _3, ...) are fallbacks used only by
    this loop, so a unit can follow a phone hotspot without losing the home
    network. Unset entries are skipped, so one network alone behaves as before.
    """
    nets = []
    for suffix in ("", "_2", "_3"):
        ssid = os.getenv("CIRCUITPY_WIFI_SSID" + suffix)
        if ssid:
            nets.append((ssid, os.getenv("CIRCUITPY_WIFI_PASSWORD" + suffix)))
    return nets


def connect():
    """(Re)establish Wi-Fi and MQTT. Raises if it can't — the caller handles it."""
    if not wifi.radio.connected:
        # Try each network in turn and keep the last error, so a total failure
        # still raises something meaningful for the caller's retry/reset logic.
        last_error = None
        for ssid, password in _wifi_networks():
            try:
                print("Connecting to Wi-Fi:", ssid)
                wifi.radio.connect(ssid, password)
                break
            except Exception as e:
                print("Wi-Fi failed on", ssid, "--", e)
                last_error = e
        if not wifi.radio.connected:
            raise last_error or RuntimeError("No Wi-Fi networks configured")
        print("Wi-Fi connected:", wifi.radio.ipv4_address)
    # Idempotent: only (re)connect MQTT if it is not already up. At the fast
    # daytime cadence, calling connect() every loop would otherwise open a new
    # connection every second (a reconnect storm). is_connected() raises rather
    # than returns False in some versions, so treat any error as "not connected".
    try:
        already_connected = mqtt_client.is_connected()
    except Exception:
        already_connected = False
    if not already_connected:
        print("Connecting to MQTT broker...")
        mqtt_client.connect()
        print("Connected to broker.")


def _ota_local_version():
    """The firmware version currently installed (0 if never OTA'd)."""
    try:
        with open(OTA_VERSION_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def _ota_url(name):
    url = OTA_BASE_URL.rstrip("/") + "/" + name
    if OTA_TOKEN:
        url += "?token=" + OTA_TOKEN
    return url


def check_and_apply_ota():
    """Pull newer firmware from the Droplet and self-install. Never raises.

    Flow: read the manifest, and if its version is newer than what we last
    applied, download code.py, verify its byte length matches the manifest
    (so a truncated download is rejected, not installed), write it via a temp
    file + atomic rename, record the new version, and reload. Because this runs
    early each awake cycle, a later bug in a freshly installed code.py can still
    be healed by pushing another update -- as long as Wi-Fi still comes up.
    """
    if _ota_requests is None:
        return
    try:
        r = _ota_requests.get(_ota_url("manifest.json"), timeout=20)
        manifest = r.json()
        r.close()
    except Exception as e:
        print("OTA: manifest check failed:", e)
        return

    remote_v = int(manifest.get("version", 0))
    if remote_v <= _ota_local_version():
        return  # already up to date

    print(f"OTA: version {remote_v} available (have {_ota_local_version()}); downloading.")
    try:
        r = _ota_requests.get(_ota_url("code.py"), timeout=60)
        source = r.content  # bytes
        r.close()
    except Exception as e:
        print("OTA: download failed:", e)
        return

    expected = manifest.get("size")
    if expected is not None and len(source) != expected:
        print(f"OTA: size mismatch (got {len(source)}, expected {expected}); aborting.")
        return

    try:
        # Stage to a temp file first (size already verified above), then swap it
        # in. FAT's rename won't overwrite an existing file, so remove the old
        # code.py first. The gap is tiny; if power is lost inside it, recover
        # over USB — code.py.new holds the complete new firmware.
        with open("code.py.new", "wb") as f:
            f.write(source)
        try:
            os.remove("code.py")
        except OSError:
            pass
        os.rename("code.py.new", "code.py")
        with open(OTA_VERSION_FILE, "w") as f:
            f.write(str(remote_v))
    except Exception as e:
        print("OTA: install failed (filesystem not writable? see boot.py):", e)
        return

    print(f"OTA: installed version {remote_v}; reloading.")
    import supervisor
    supervisor.reload()  # never returns: re-runs the new code.py from the top


OVERLOAD_FLAG = 0x08  # bit 3 of opt4048.flags == sensor saturated


def read_diagnostics():
    """Return raw-channel diagnostics as a dict, or {} on a sensor read error.

    - overload True  -> the sensor is saturated; the reading is unreliable.
    - low zx_ratio   -> little blue (Z) relative to red (X), e.g. window glass
      cutting blue, which warms the CCT.
    """
    try:
        x_ch, y_ch, z_ch, w_ch = opt4048.all_channels  # raw ADC counts
        flags = opt4048.flags
        return {
            "raw_x": x_ch,
            "raw_y": y_ch,
            "raw_z": z_ch,
            "raw_w": w_ch,
            "zx_ratio": round(z_ch / x_ch, 3) if x_ch else 0,
            "overload": bool(flags & OVERLOAD_FLAG),
        }
    except Exception as e:
        print("  diag read failed:", e)
        return {}


def read_battery():
    """Return battery voltage and SoC% from MAX17048, or {} on error.

    Temperature is handled autonomously by the BQ24074 via its THERM pin
    and is not read by the MCU in this configuration.
    """
    if max17048 is None:
        return {}
    try:
        return {
            "battery_v": round(max17048.cell_voltage, 3),
            "battery_pct": round(min(max17048.cell_percent, 100.0), 1),
        }
    except Exception as e:
        print("  battery read failed:", e)
        return {}


def read_and_publish(cie_x, cie_y, lux):
    """Publish one reading from already-read sensor values.

    The caller reads opt4048.cie once (radio off) to make the day/night
    decision and passes the values here, so the sensor is not read twice. May
    raise on a network error.
    """
    cct = opt4048.calculate_color_temperature(cie_x, cie_y)
    payload = {
        "sensor_id": SENSOR_ID,
        "cct": round(cct, 1),
        "lux": round(lux, 2),
        "cie_x": round(cie_x, 4),
        "cie_y": round(cie_y, 4),
    }
    payload.update(read_battery())      # adds battery_v, battery_pct
    payload.update(read_diagnostics())  # adds raw_x/y/z/w, zx_ratio, overload
    payload_json = json.dumps(payload)
    print(payload_json)
    mqtt_client.publish(TOPIC, payload_json)


def idle(seconds):
    """Sleep for `seconds`, feeding the watchdog in short chunks.

    A single long time.sleep would let the 90s watchdog fire during the normal
    multi-minute gap between readings, so we sleep in WATCHDOG_SLEEP_CHUNK steps
    and feed the watchdog each step. A genuine mid-work hang still trips the
    watchdog; the long idle gap does not.
    """
    slept = 0
    while slept < seconds:
        chunk = min(WATCHDOG_SLEEP_CHUNK, seconds - slept)
        time.sleep(chunk)
        wdt.feed()
        slept += chunk


def seconds_to_next_capture():
    """Seconds to wait so the next reading lands on a wall-clock boundary.

    Alignment is done modulo the hour rather than against a Unix epoch, which
    avoids depending on time.mktime being present in the build. That is exact
    only when PUBLISH_INTERVAL divides an hour evenly (120 s does; 300 s does
    too), so anything else falls back to free-running rather than producing a
    jump at the top of each hour. Any NTP failure also falls back, so a network
    blip costs alignment for one cycle instead of stalling the loop.
    """
    if _ntp is None or 3600 % PUBLISH_INTERVAL:
        return PUBLISH_INTERVAL
    try:
        now = _ntp.datetime
    except Exception as e:
        print("NTP unavailable, free-running this cycle:", e)
        return PUBLISH_INTERVAL
    wait = PUBLISH_INTERVAL - ((now.tm_min * 60 + now.tm_sec) % PUBLISH_INTERVAL)
    # Landing exactly on a boundary would otherwise mean a ~0 s wait and two
    # readings in the same slot, so take the next slot instead.
    if wait < 1:
        wait += PUBLISH_INTERVAL
    return wait


def deep_sleep(seconds):
    """Power the radio down and deep-sleep for `seconds`, then reboot into code.py.

    Deep sleep is the only real battery saving on this board (the always-on
    radio otherwise dominates). We disable the watchdog first so its short
    timeout cannot reset us mid-sleep, and best-effort close the MQTT link
    (deep sleep drops the connection anyway). This never returns: the board
    resets and re-runs code.py (and boot.py) from the top on wake.
    """
    try:
        mqtt_client.disconnect()
    except Exception:
        pass
    wdt.mode = None  # a 90s watchdog must not fire during a multi-minute sleep
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + seconds)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)


# --- Main loop ---
# We do NOT connect at boot: read the light level first (radio off) so a boot
# that lands in the true-night window goes straight back to deep sleep without
# ever powering the radio. Everything is wrapped so no single error halts the
# program; the watchdog reboots the board if the loop ever truly hangs.
fail_count = 0
_last_ota_check = None   # monotonic time of the last OTA check; None = never
while True:
    wdt.feed()  # "still alive" — resets the watchdog countdown

    # Read the sensor once (no radio needed) for the day/night decision and the
    # values to publish. If the sensor read itself fails, wait and retry.
    try:
        cie_x, cie_y, lux = opt4048.cie
    except Exception as e:
        print("Sensor read failed:", e)
        idle(PUBLISH_INTERVAL)
        continue

    if lux < NIGHT_LUX_FLOOR:
        # NIGHT: colour data is noise. Send a best-effort battery/lux heartbeat,
        # linger briefly so wireless flashing stays catchable, then deep-sleep
        # the radio off until the next check. This is where the battery is saved.
        print(f"Night (lux {lux:.2f} < {NIGHT_LUX_FLOOR}): heartbeat, then deep sleep {NIGHT_INTERVAL}s.")
        try:
            connect()
            read_and_publish(cie_x, cie_y, lux)
        except Exception as e:
            print("Night heartbeat failed (sleeping anyway):", e)
        idle(NIGHT_AWAKE_GRACE)      # radio still up — a window to catch OTA flashing
        deep_sleep(NIGHT_INTERVAL)   # never returns; board reboots on wake

    # DAY: stay connected (always-on) so wireless flashing keeps working, and
    # publish at the normal cadence.
    target_wait = None    # seconds-to-boundary, captured before this cycle's
    work_start = None     # network work so that work's own duration (which
                           # differs per unit -- reconnects, hotspot latency,
                           # OTA checks) can't shift the shared wall-clock grid
    try:
        connect()
        # Capture the schedule target as soon as we're connected, *before* the
        # OTA check and publish below. Those take a variable amount of time
        # (longer on a unit that had to reconnect Wi-Fi, or one on a slower
        # hotspot fallback), and computing the target only after they finish
        # would bake that unit-specific delay into the grid as a fixed phase
        # offset -- each unit stays internally steady but drifts apart from
        # the others, which is exactly the "in sync with itself, not with the
        # others" symptom this was written to prevent.
        target_wait = seconds_to_next_capture()
        work_start = time.monotonic()
        # Check for new firmware early (radio is up) but at most every
        # OTA_CHECK_INTERVAL, so the fast daytime cadence never hammers it.
        # If an update installs, check_and_apply_ota() reloads and never returns.
        now_mono = time.monotonic()
        if _last_ota_check is None or now_mono - _last_ota_check >= OTA_CHECK_INTERVAL:
            _last_ota_check = now_mono
            check_and_apply_ota()
        read_and_publish(cie_x, cie_y, lux)
        fail_count = 0  # success: clear the failure streak
    except Exception as e:
        fail_count += 1
        print(f"Loop error ({fail_count}/{MAX_FAILURES}):", e)
        # Drop the (probably stale) connection and try to rebuild it.
        try:
            mqtt_client.disconnect()
        except Exception:
            pass
        try:
            connect()
        except Exception as e2:
            print("Reconnect failed:", e2)
        # If we keep failing, reboot for a guaranteed-clean slate.
        if fail_count >= MAX_FAILURES:
            print("Too many failures in a row — resetting board.")
            time.sleep(2)
            microcontroller.reset()

    # Sleep to the next wall-clock boundary rather than a flat interval, so
    # this unit stays in step with the others. Subtract whatever time this
    # cycle's work already used since target_wait was captured, so the actual
    # wake time lands on the boundary regardless of how long that work took.
    if target_wait is not None:
        elapsed = time.monotonic() - work_start
        idle(max(1, target_wait - elapsed))
    else:
        idle(seconds_to_next_capture())
