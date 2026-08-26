"""
Disable the CIRCUITPY USB mass-storage drive.

On native-USB boards (ESP32-S2/S3) the filesystem is reserved for USB MSC
unless this is disabled, which blocks writes from the web workflow (PUT to
/fs/... returns 500) even when no USB cable is attached. Disabling it here
is what makes WiFi flashing actually work. The USB serial/REPL console is
unaffected, so `screen /dev/tty.usbmodem...` still works as a fallback.
"""

import storage

storage.disable_usb_drive()

# Make the filesystem writable by CircuitPython itself, not just the web
# workflow. This is what lets code.py overwrite itself during an over-the-air
# update (see the OTA section in code.py). The web workflow and code.py share
# the same writable flag (USB is the only other claimant, and it is disabled
# above), so this does NOT break LAN wireless flashing -- both keep working.
# Wrapped so a remount failure can never halt boot and cost us the flash path.
try:
    storage.remount("/", readonly=False)
    print("Filesystem remounted read-write (OTA + web workflow can write).")
except Exception as e:
    print("Filesystem remount skipped:", e)
