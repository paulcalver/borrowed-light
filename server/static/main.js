// ---------------------------------------------------------------------------
// CCT full-screen colour
//
// The whole window is painted the single colour the sensor is seeing right now.
// Every poll we fetch the latest reading; the displayed colour then eases from
// wherever it currently is toward that new reading over TRANSITION_MS, so the
// screen drifts smoothly through the day instead of snapping between readings.
//
// The tiled history lives on a separate page — see /grid.
// ---------------------------------------------------------------------------

// ---- Config ----
// Served from the backend itself, so the API is same-origin: a relative path
// works on the Droplet and on localhost during development, with no CORS.
const API = "";  // same-origin; requests go to /api/...

const POLL_MS = 1000;             // how often the page re-fetches the latest reading
const TRANSITION_MS = 1000;       // how long to ease from one reading's colour to the next

// Below this lux the sensor signal sits near its noise floor and the measured
// chromaticity is unreliable — it wanders the whole diagram, so rendering it as
// true colour paints noise as a vivid saturated hue. Noise dominates below
// ~0.1 lux in practice; 1 lux keeps a 10x margin without clipping real daylight.
// Sub-floor readings are drawn as night instead.
const LUX_FLOOR = 1.0;            // lux; below this a reading is treated as night
const NIGHT_GREY = 17;            // #111 — night colour

// The colour eases along fromRgb -> toRgb over TRANSITION_MS. `current` is what
// is on screen this frame; a new reading starts a fresh ease from `current`.
let current = [255, 255, 255];
let fromRgb = [255, 255, 255];
let toRgb = [255, 255, 255];
let transStart = 0;               // millis() when the current ease began

function setup() {
  createCanvas(windowWidth, windowHeight);
  noStroke();
  fetchLatest();
  setInterval(fetchLatest, POLL_MS);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

async function fetchLatest() {
  try {
    const resp = await fetch(`${API}/api/latest`, { cache: "no-store" });
    const d = await resp.json();
    if (!d || d.cie_x == null || d.cie_y == null) return;

    const target =
      (d.lux != null && d.lux < LUX_FLOOR)
        ? [NIGHT_GREY, NIGHT_GREY, NIGHT_GREY]   // night — signal below the noise floor
        : xyToRgb(d.cie_x, d.cie_y);

    // Ease from whatever is on screen right now toward the new reading.
    fromRgb = current.slice();
    toRgb = target;
    transStart = millis();
  } catch (e) {
    console.error("data fetch failed:", e);
  }
}

// Measured CIE x,y chromaticity -> sRGB: the true colour the sensor saw,
// including any green/magenta tint that a single Kelvin number discards.
// Brightness is not represented — we normalise to a full-strength chip so the
// screen stays a pure colour comparison (as the Kelvin swatch also did).
function xyToRgb(x, y) {
  if (!(y > 0)) return [0, 0, 0];
  // x,y -> XYZ at unit luminance (Y = 1).
  const X = x / y;
  const Y = 1;
  const Z = (1 - x - y) / y;
  // Linear sRGB from XYZ (D65 primaries).
  let r =  3.2406 * X - 1.5372 * Y - 0.4986 * Z;
  let g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z;
  let b =  0.0557 * X - 0.2040 * Y + 1.0570 * Z;
  // Clamp out-of-gamut negatives to 0 (desaturates toward the gamut edge),
  // then normalise so the brightest channel is full strength.
  r = Math.max(0, r); g = Math.max(0, g); b = Math.max(0, b);
  const peak = Math.max(r, g, b);
  if (peak > 0) { r /= peak; g /= peak; b /= peak; }
  // sRGB gamma companding, then scale to 0..255.
  const gamma = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);
  const to255 = (c) => Math.max(0, Math.min(255, Math.round(gamma(c) * 255)));
  return [to255(r), to255(g), to255(b)];
}

function draw() {
  // Fraction of the current transition elapsed (0..1). Once complete the colour
  // simply holds at toRgb until the next reading restarts the ease.
  const t = constrain((millis() - transStart) / TRANSITION_MS, 0, 1);
  current = [
    lerp(fromRgb[0], toRgb[0], t),
    lerp(fromRgb[1], toRgb[1], t),
    lerp(fromRgb[2], toRgb[2], t),
  ];
  background(current[0], current[1], current[2]);
}
