// ---------------------------------------------------------------------------
// CCT grid
//
// Stateless: every poll we fetch the recent readings, sample one per square at
// SECONDS_PER_CELL spacing, and redraw the whole grid. The "rolling" behaviour
// is automatic — the newest reading enters at the end and the oldest drops off.
// Data fills from the top-left; empty slots wait at the end.
// ---------------------------------------------------------------------------

// ---- Config ----
// Served from the backend itself, so the API is same-origin: a relative path
// works on the Droplet and on localhost during development, with no CORS.
const API = "";  // same-origin; requests go to /api/...
const COLS = 60, ROWS = 60;  // grid size (width x height)
const CELLS = COLS * ROWS;        // 3600 (one per second over 1h)

// Which sensor this grid shows, taken from the page's own path
// (/grid-sensor-01, /grid-sensor-02, ...) rather than hardcoded here, so the
// same script serves every sensor's page. /grid (no suffix) falls back to
// sensor-01 rather than mixing every sensor's readings into one grid, which
// is what it did before this was added.
const SENSOR_ID = (() => {
  const m = window.location.pathname.match(/^\/grid-(sensor-.+)$/);
  return m ? m[1] : "sensor-01";
})();

// --- Play with this ---
// How much time each square represents, in seconds. The sensor reports every
// ~30s, so 30 = one raw reading per square. Bump it (60, 300 = 5 min,
// 3600 = 1 hour…) to stretch each square over a longer span. (It samples one
// reading per step — not an average.)
const SECONDS_PER_CELL = 1;       // each square = 1 second (1/s fast-capture: full 1440-cell grid ≈ 24 min)
const READING_PERIOD = 1;         // sensor publish cadence (s) — set to 1 for the 1/s fast-capture experiment (was 30)
const POLL_MS = 1000;             // how often the page re-fetches (1s so a new cell appears each second)
const RADIUS = 0;                 // sharp corners

// Below this lux the sensor signal sits near its noise floor and the measured
// chromaticity is unreliable — it wanders the whole diagram, so rendering it as
// true colour paints noise as a vivid saturated hue. Noise dominates below
// ~0.1 lux in practice; 1 lux keeps a 10x margin without clipping real daylight.
// Sub-floor readings are drawn as night instead.
const LUX_FLOOR = 1.0;            // lux; below this a reading is treated as night
const NIGHT_GREY = 17;            // #111 — night cell colour

// cells[i] = { hour, cct, lux, ... } or null for an empty slot
let cells = new Array(CELLS).fill(null);

function setup() {
  createCanvas(windowWidth, windowHeight);
  noStroke();
  noLoop();                       // redraw only on new data / resize
  fetchData();
  setInterval(fetchData, POLL_MS);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  redraw();
}

async function fetchData() {
  try {
    // How many raw readings make up one square (based on sensor cadence).
    const step = Math.max(1, Math.round(SECONDS_PER_CELL / READING_PERIOD));
    // no-store: without it the browser serves a cached response to each poll,
    // so the grid appears frozen until a manual page refresh.
    const resp = await fetch(`${API}/api/history?limit=${CELLS * step}&sensor_id=${SENSOR_ID}`, { cache: "no-store" });
    const data = await resp.json();          // oldest -> newest
    // Walk back from the newest, taking one reading every `step`.
    const sampled = [];
    for (let i = data.length - 1; i >= 0 && sampled.length < CELLS; i -= step) {
      sampled.push(data[i]);
    }
    sampled.reverse();                        // oldest -> newest
    const next = new Array(CELLS).fill(null);
    sampled.forEach((d, i) => { next[i] = d; });
    cells = next;
    redraw();
  } catch (e) {
    console.error("data fetch failed:", e);
  }
}

// Measured CIE x,y chromaticity -> sRGB: the true colour the sensor saw,
// including any green/magenta tint that a single Kelvin number discards.
// Brightness is not represented — we normalise to a full-strength chip so the
// grid stays a pure colour comparison (as the old Kelvin swatch also did).
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
  background(255);

  // Fill the whole window: cells are width/COLS by height/ROWS, so their ratio
  // follows the window's. No padding, no centring — the grid touches every edge.
  const cellW = width / COLS;
  const cellH = height / ROWS;

  for (let i = 0; i < CELLS; i++) {
    const col = i % COLS;
    const row = Math.floor(i / COLS);
    // Snap each edge to a whole pixel so a cell's right edge lands exactly on
    // the next cell's left edge — no sub-pixel seams between touching cells.
    const x0 = Math.round(col * cellW);
    const y0 = Math.round(row * cellH);
    const x1 = Math.round((col + 1) * cellW);
    const y1 = Math.round((row + 1) * cellH);
    const d = cells[i];

    if (d && d.cie_x != null && d.cie_y != null) {
      if (d.lux != null && d.lux < LUX_FLOOR) {
        fill(NIGHT_GREY);         // night — signal below the noise floor
      } else {
        const [r, g, b] = xyToRgb(d.cie_x, d.cie_y);
        fill(r, g, b);
      }
    } else {
      fill(255);                  // empty placeholder
    }
    rect(x0, y0, x1 - x0, y1 - y0, RADIUS);
  }
}
