"""
ip65_box_domes.py  --  rev C, "column" architecture
====================================================
IP65 enclosure for the V2 daylight chromaticity sensor. Complete rewrite:
the old side-wall dome port design is retired (it could not print in ASA
without warp in any orientation). This file is the single source of truth
for all enclosure geometry. Fusion 360 is downstream only.

VOCABULARY (fixed, used in all project threads)
  TOP        = the end containing the dome port = the screw-down lid.
  BOTTOM     = the opposite end. Carries PG7 gland + breather vent,
               points down when deployed.
  SIDE WALLS = the other four faces. Deployed, TOP faces the sky.

ARCHITECTURE
  Vertical column, 66 mm square exterior, open-top cup. Height is fully
  derived from content (seal stack + sensor deck + sled + bottom
  clearance); change a component and the box height follows.

  Hanging from the lid (nothing wired to it, lifts clean off):
    dome flange in recess -> 1 mm O-ring -> printed spacer shim ->
    clamp ring with integral mixing tube. Squeeze is set by the boss
    hard stop; the spacer thickness is the tuning knob, as before.

  Fixed to the box:
    SENSOR DECK: flat plate on wall ledges just below the mixing tube.
      OPT4048 on four standoffs, die up on the dome axis. The deck
      doubles as a light baffle; the STEMMA lead drops past its edge
      through the 3 mm perimeter gap. The ledges sit on the FRONT
      (-Y) side of the +/-X walls, a band the sled carries nothing
      in, so the battery keeps its lateral clearance during descent.
    SLED: flat plate sliding down rib channels on the +/-X walls,
      resting on the box floor (floor-rest is the vertical datum).
      Front (-Y facing) face top to bottom: QT Py on its Adafruit
      snap mount (#6183, 4x M3, native orientation, USB-C up),
      MAX17048 on bosses, BQ24074 on bosses -- BQ at the bottom,
      nearest the PG7 gland, so the solar lead has the shortest run.
      Battery rides in a separate printed cradle that rail-and-groove
      slides onto the sled's plain back face (2 rails slide into
      matching grooves, no screws, no bosses) -- no zip ties. Faces carry
      embossed/engraved labels. The box is widened (EXT_W) specifically
      to fit the QT mount's native, full-width orientation without
      fouling the deck ledge clearance on the +/-X walls. The assembly
      STEP includes translucent green reference bodies for the boards,
      battery and DC jack keep-out; these are visualisation only and
      appear in no part STEP.
    DOVETAIL RAIL: printed integrally on the +Y wall, centred on the
      box height as a short segment matching the bracket's engagement
      depth (not full height -- a full-height rail only ever had its
      bottom ~70 mm inside the bracket anyway, so the bracket gripped
      the box by its ankles; centring it lands the grip near the
      box's middle instead). Tapered (French cleat logic); drops into
      the female receiver on the pole bracket. Rail profile is the
      shared standard for all future mount types. Zero fasteners,
      zero wall penetrations.

  ASSEMBLY ORDER: sled in, deck screwed down (2x M2.5), deck_wall
                  dropped on top (no fasteners), lid on.
  SERVICE:       lift lid, lift deck_wall off, 2 deck screws, unplug
                  STEMMA, pull sled.

PRINT ORIENTATIONS (white ASA, Bambu P1S, enclosed chamber)
  box      bottom face down. Plain vertical walls, rail is a vertical
           extrusion, ledges carried on 45 degree corbels. Brim.
  lid      exterior face down (model is built interior-face-at-z0,
           so flip in the slicer). Weather skirt around the perimeter
           (SKIRT_H below the seal line) prints as a plain rising wall
           in this same orientation -- it hangs down in the model, so
           the slicer flip turns it into a wall going up from solid
           material, no overhang.
  clamp    tube up (model is built plate-top-at-z0, tube pointing down,
           so flip in the slicer).
  spacer   flat, either face.
  deck     as modelled, standoffs up.
  deck_wall  flat, either face -- a single continuous ring that hugs
           each corner pillar with the same notch clearance as the
           deck itself (see the section 10 comment for the offset
           direction that makes this stay connected), no overhangs.
           Drops onto the deck after it's screwed down (shields the
           box's own interior wall in the optical chamber above, so
           that section no longer needs painting).
  sled     as modelled, bosses up. Back face is genuinely flat --
           the battery cradle's rail grooves are a cut, not a boss, so
           nothing there breaks the flat-print orientation.
  bracket  as modelled, standing on its bottom face (the 80mm BRK_H
           axis vertical, receiver-slot end up). This is load-bearing,
           not a style preference: the V-groove and the dovetail slot
           are both extruded straight along Z with no taper in this
           orientation, so neither one is an overhang at all -- lying
           the block flat any other way (V facing up looks like the
           obvious way to set a V-block down, but isn't what this
           script assumes) puts a taper or a slot wall into an overhang
           it was never designed to survive as one. The only real
           bridge anywhere on this part is the tunnel roof at 8mm,
           well inside what this profile handles cleanly elsewhere.
           If a slicer's auto-orient feature is used, check it kept
           this orientation before committing to the print -- it has
           no reason to know this constraint exists.
  battery_cradle  as modelled, mounting face down. The 2 rails run
           almost the full length, so contact with the bed is a long
           thin strip, not an isolated island -- prints flat
           without supports.

HARDWARE (build notes)
  IMPORTANT: every screw length below is capped by its insert's REAL
  length (a blind pocket, not an open thread) -- (material the shank
  passes through unthreaded) + (real insert length) is a hard ceiling.
  Go over it and the screw bottoms out on the insert's own end before
  the joint can fully close, no matter how much thread is left unused.
  Confirmed real lengths: M2.5 = 4.0mm, M3 = 5.7mm. Standardised
  2026-07-20: button head (hex socket drive) on every screw. M2.5x6
  confirmed by hand-fit to work fine on every breakout-board joint
  (BQ24074, MAX17048, OPT4048, deck-to-ledges, and now QT Py too --
  the theoretical stack-up ceiling is tighter than this in a couple of
  spots, but real assembly has enough slack that x6 seats fine
  everywhere except the clamp ring). Clamp ring stays the one
  exception at M2.5x4 -- its ceiling is a hard 5.0mm, confirmed
  physically bottoming out at anything longer. Full stack-up math and
  the standardisation rationale are in mechanical/build-reference.md,
  not repeated here.
  4x  M3 heat-set inserts (pillars) + M3x10 button + NYLON SEALING
      WASHER. The lid screws sit inside the seal line on a sky-facing
      lid, so sealing washers are mandatory, not optional.
  3x  M2.5 inserts in lid port bosses + M2.5x4 button (clamp ring,
      from below) -- the one M2.5 exception; see IMPORTANT above.
  2x  M2.5 inserts in wall ledges + M2.5x6 button (deck).
  4x  M2.5 inserts in deck standoffs + M2.5x6 button (sensor; head
      clearance under the tube wall is 0.8mm -- a standard M2.5 button
      head, ~1.3mm tall, clears this comfortably, no special
      "low-profile" part needed).
  4x  M2.5 inserts in sled bosses + M2.5x6 button (BQ24074).
  2x  M2.5 inserts in sled bosses + M2.5x6 button (MAX17048, single
      edge).
  4x  M2.5 inserts in sled bosses + M2.5x6 button (QT Py snap mount,
      #6183) -- switched from M3 (2026-07-20): M3 was a tight fit on
      the snap mount's own holes. Uses the same shared boss/insert
      parameters as BQ24074 and MAX17048, no QT-specific ones any more.
  Battery cradle: no fasteners -- rail-and-groove slides onto the
      sled's back face (2 rails slide into matching grooves, gravity-
      seated against a hard stop, glued once seated). See the battery
      cradle section.
  PG7 gland (bottom), M12 breather vent (bottom, thread VERIFY),
  matte black paint or flock for the chamber side of the deck and the
  lid interior.

VERIFY BEFORE COMMITTING PLASTIC (marked in parameters)
  - BQ24074 and MAX17048 hole pitches are now taken from Adafruit's own
    STEP/dimensioned-drawing files in mechanical/adafruit-cad-files/
    (cross-checked against adafruit_BQ24074.png), not datasheet guesses.
    Still worth a caliper check against the physical boards before
    printing, since the reference files could be a different revision.
  - QT Py snap mount (#6183) hole pattern is measured from
    QTPy_Snap_Mount_SLA_V2.stl in the same folder.
  - Breather vent thread size (M12 assumed).
  - Dome batch dimensions if a new batch is ordered.

pole_mount_params.py migration to the rail-profile standard is a
separate follow-up task; this file is self-contained for now.
"""

import math
import os

import cadquery as cq

# =====================================================================
# 1. PARAMETERS  (mm throughout)
# =====================================================================

# ---- global form ----------------------------------------------------
EXT_W = 66.0          # exterior square width. Widened from 60 to fit
                      # the QT Py snap mount in its native orientation
                      # (long axis across the sled, USB-C at the top)
                      # plus a fully-enclosing battery cradle -- both
                      # need more width than the deck-ledge clearance
                      # zone had at 60. Minimums: 65.1 for the QT
                      # mount, 63.3 for the cradle; 66 clears both.
WALL = 2.5            # side wall thickness
BOTTOM_T = 3.0        # bottom face thickness
BOX_R = 4.0           # exterior corner radius

# ---- rim + lid face seal (proven flangeless design) -----------------
RIM_T = 5.0           # rim band wall thickness (opening = 50)
RIM_BAND = 12.0       # height of the thickened rim band
RIM_TAPER = 2.5       # 45 degree transition below the band
CORD_CS = 2.0         # O-ring cord diameter
GROOVE_W = 2.7        # groove width
GROOVE_D = 1.5        # groove depth -> 0.5 squeeze (25%) at hard stop
GROOVE_OFF = EXT_W / 2 - RIM_T / 2      # centreline offset, 30.5
GROOVE_RC = 6.75      # groove centreline corner radius

# Seal-inside-the-screws corner (2026-07-23). The groove used to run
# OUTSIDE the lid screws at every corner -- the screws pierced the
# sealed area, which is why nylon sealing washers under the heads were
# mandatory. Sealing washers add head height on a sky-facing lid, and
# head height is what casts shadows toward the dome at low sun angles,
# so the seal now dips inboard at each corner and passes BETWEEN the
# box centre and the screw. The screw holes end up outside the sealed
# boundary entirely: water can sit in a screw pocket without any path
# into the box, and the washers are gone.
#
# The dip is a plain 45 degree chamfer across each corner rather than a
# tighter corner arc, for one specific reason: a chamfer is parallel to
# the corner's own diagonal, so the gap between the groove's inner edge
# and the material backing it (the corner gusset below) is CONSTANT the
# whole way across. A constant-radius arc dipping to the same depth
# runs off the inner edge of the rim band partway round -- checked, it
# leaves the rim between roughly 28 and 40 degrees, where neither the
# rim band nor the corner post reaches far enough inboard to back it.
SEAL_SCREW_WALL = 2.0   # rim material between the groove's outer edge
                        # and the lid-screw insert pocket. The binding
                        # number in the whole corner: it is what pushes
                        # PIL_POS out to the corner and sets how deep
                        # the chamfer has to dip.
GUSSET_MARGIN = 0.8     # material inboard of the groove's inner edge,
                        # i.e. how much of the corner gusset stands
                        # proud of the groove before the void starts
CORNER_CHAMF_CLR = 0.5  # clearance from the deck / deck wall corner
                        # chamfer to the gusset, on the way past it

# ---- corner pillars (lid screws) ------------------------------------
# Pushed as far into the corners as the exterior allows (2026-07-23,
# was a fixed 25.5), so the seal groove has somewhere to run inside
# them. Derived, not typed: whichever of the flat wall face and the
# exterior corner radius runs out of material first sets the limit.
PIL_R = 5.2           # post radius. The post is CLIPPED to the box
                      # exterior in the build below -- at this PIL_POS a
                      # free cylinder would poke out through the wall,
                      # so it becomes the corner solid instead.
M3_INS_D = 4.0        # M3 heat-set insert pilot dia
M3_INS_L = 6.0        # pocket depth
SCREW_WALL_OUT = 2.0  # material outboard of the insert pocket, both to
                      # the flat wall face and to the exterior corner
_pil_max_flat = EXT_W / 2 - M3_INS_D / 2 - SCREW_WALL_OUT
_pil_max_diag = (((EXT_W / 2 - BOX_R) * math.sqrt(2) + BOX_R)
                 - M3_INS_D / 2 - SCREW_WALL_OUT) / math.sqrt(2)
PIL_POS = min(_pil_max_flat, _pil_max_diag)

# ---- lid ------------------------------------------------------------
LID_T = 5.0
LID_SCREW_D = 3.4     # M3 clearance. No counterbore at all (2026-07-20,
                      # final): both the 2mm-deep counterbore and the
                      # 0.6mm shallow washer-locating recess strung/
                      # printed roughly in ASA on this face-down
                      # orientation. Head + nylon washer now sit fully
                      # proud on the flat exterior surface -- a plain
                      # through-hole has nothing to bridge at all.
SKIRT_CLR = 0.4       # radial clearance between the skirt's inner face
                      # and the box's actual exterior wall -- lets the
                      # lid lift straight off without binding
SKIRT_T = 2.0         # skirt wall thickness
SKIRT_H = 8.0         # skirt drop below the seal line (2026-07-21,
                      # added): a downward-facing lip around the lid's
                      # new, slightly larger outer edge, wrapping past
                      # the box's exterior wall to shed wind-driven
                      # rain off the seal line and the proud screw
                      # heads before it ever reaches them. Prints clean
                      # in the same exterior-face-down orientation as
                      # the rest of the lid: the whole lid gets flipped
                      # for printing, so a feature that hangs DOWN in
                      # real life becomes a wall rising UP from solid
                      # material in the print, the same class of
                      # feature as the box's own vertical walls -- not
                      # a bridge over a void like the two retired
                      # recessed-screw attempts were. Modest height:
                      # only needs to clear a few mm past the wall to
                      # do its job, and must stay well clear of the
                      # pole-mount rail lower down (checked by
                      # assertion, not just by eye).
LID_W = EXT_W + 2 * (SKIRT_CLR + SKIRT_T)   # lid grows to meet the
                      # skirt's outer face flush -- "a tiny bit bigger"
                      # than the box, not a separate stepped ring

# ---- dome (measured, this batch) ------------------------------------
FLANGE_T = 2.0
DOME_OD = 25.0
FLANGE_OD = 28.0
DOME_H = 17.0         # total incl flange

# ---- port seal stack (proven, unchanged) ----------------------------
APERTURE_D = 25.5     # through-lid clearance bore
NECK_D = 25.2         # necked top section hugging the dome
NECK_L = 1.0
RECESS_D = 0.5        # flange recess depth into the lid interior face
RECESS_DIA = FLANGE_OD + 0.6
ORING_CS = 1.0
ORING_SQUEEZE = 0.25  # fraction of cord
SPACER_T_NOMINAL = 3.0
                      # The reference thickness baked into the LID's own
                      # boss height (CLAMP_FACE_DROP below) -- this is what
                      # a freshly-reprinted lid's port bosses are sized
                      # against, and matches what's already printed into
                      # any existing physical lid. Only change this if the
                      # lid itself is being redesigned/reprinted; it should
                      # NOT be used as the per-print squeeze-tuning knob
                      # (that's SPACER_T_TRIM below) -- the two used to be
                      # one combined parameter (SPACER_T), which meant
                      # tuning squeeze on an already-printed lid also
                      # silently changed the boss-height formula for any
                      # *future* reprinted lid, cancelling the tuning back
                      # out. Split 2026-07-22 so the two prints (lid vs
                      # spacer) can vary independently.
SPACER_T_TRIM = 0.3   # Added on top of SPACER_T_NOMINAL for the spacer's
                      # own printed thickness only -- reprint the spacer
                      # alone with this nudged thinner/thicker to tune
                      # O-ring squeeze against your *existing* lid, with no
                      # effect on CLAMP_FACE_DROP or anything else.
                      # Currently +0.3mm (2026-07-22): dry-fit showed the
                      # spacer sitting flush at the boss/mounting holes --
                      # the boss's own height already has SPACER_T_NOMINAL
                      # baked in as a fixed budget shared with the
                      # compressed O-ring, so a flush fit against an
                      # already-printed lid means the real [O-ring +
                      # spacer] stack is coming up short of that budget
                      # (undersized cord, dome flange a hair thinner than
                      # modelled, etc) and the O-ring never actually gets
                      # compressed. A taller spacer eats more of that same
                      # fixed gap, forcing the real O-ring to compress --
                      # this is a first test increment, re-check squeeze by
                      # eye/feel after printing and keep tuning
                      # thinner/thicker from here rather than assuming
                      # this is the final number.
SPACER_T = SPACER_T_NOMINAL + SPACER_T_TRIM  # actual printed spacer
                      # thickness -- everything below keeps referencing
                      # SPACER_T as before; only the two inputs above are
                      # new.
SPACER_OD = 29.0      # limited by the port boss inner faces
SPACER_ID = 25.0
SPACER_GRV_C = 26.75  # locating groove centreline dia (top face)
SPACER_GRV_W = 1.3
SPACER_GRV_D = 0.35
EAR_W = 12.0          # tangential width of each retention ear, at the
                      # boss radius -- reaches out from the spacer OD
                      # and clips around a port boss (P_BOSS_ANGS) so
                      # the spacer can't drift or fall out of place
                      # during assembly. Wide enough that the notch cut
                      # below still leaves ~2mm shoulders either side
                      # of the boss, not a fragile sliver.
EAR_CLR = 0.3         # radial clearance around the boss for a light
                      # clip fit, not an interference press-fit (ASA
                      # doesn't flex well for a true snap)
EAR_REACH = 1.0       # how far the ear's tip reaches past the boss's
                      # own outer edge

CLAMP_OD = 44.0
CLAMP_T = 2.5
TUBE_OD = 27.0
TUBE_ID = 23.0
TUBE_L = 12.0
SEAT_GAP = 2.5        # tube end to sensor board top
P_BOSS_BCD = 37.0
P_BOSS_D = 7.0
P_BOSS_ANGS = (90, 210, 330)   # notches at 0/180 stay free
M25_INS_D = 3.5       # M2.5 heat-set insert pilot dia
M25_INS_L = 4.0
CLAMP_SCREW_D = 2.9
CLAMP_CB_D = 5.5
CLAMP_CB_DEPTH = 1.5
# Socket notches at the tube end, +/-X: clearance for the OPT4048's
# two STEMMA QT (JST-SH) connectors at the board's +/-X ends. Sized
# from the connectors' real geometry (measured off "6335 OPT4048 XYZ
# Color Sensor.step"), not a guess -- previously an oversized 8 x 6mm
# placeholder with ~5.5mm of unused height margin.
CONNECTOR_W = 6.0     # connector Y-extent (measured)
CONNECTOR_H = 2.96    # connector height above the board (measured)
NOTCH_SIDE_CLR = 0.4  # width clearance per side, beyond the connector
NOTCH_MARGIN = 1.0    # height clearance beyond the actual interference
NOTCH_W = CONNECTOR_W + 2 * NOTCH_SIDE_CLR
# The notch only needs to cover however far the connector pokes above
# the tube's own bottom edge (SEAT_GAP is smaller than the connector's
# height, so it currently does poke in a little) -- not the
# connector's full height, since below the tube's bottom edge is open
# SEAT_GAP air anyway, nothing to clear there.
NOTCH_H = max(CONNECTOR_H - SEAT_GAP, 0) + NOTCH_MARGIN

# ---- OPT4048 board --------------------------------------------------
BOARD_L = 25.4        # along X (sockets on the +/-X ends)
BOARD_W = 17.78
BOARD_T = 1.6
HOLE_PX = 20.32       # mounting hole pitch
HOLE_PY = 12.7
DIE_OFFSET = (0.0, 0.0)   # shift the standoff group if the die is
                          # not at the board centre
STAND_H = 6.0
STAND_D = 8.0         # 5.5 -> 8.0 -> 10.0 -> back to 8.0 (2026-07-23).
                      # 5.5 gave a 1.0mm wall around the M2.5 insert
                      # pilot (M25_INS_D=3.5), which deformed/bulged on
                      # insertion; 8.0 (wall 2.25mm) was the fix that
                      # actually worked, and 10.0 was extra margin asked
                      # for afterwards. First full assembly showed 10.0
                      # costs more than it buys: the two standoffs on
                      # the board's SHORT side sit at HOLE_PY = 12.7mm
                      # pitch, so at 10.0 the channel between them is
                      # only 2.7mm -- not enough to route the OPT4048's
                      # STEMMA lead through to DECK_CABLE_D neatly.
                      # Back to the proven 8.0, which opens that channel
                      # to 4.7mm (assertion below) and keeps the wall at
                      # the thickness that stopped the bulging.
SCREW_HEAD_H = 1.7    # low-profile M2.5 pan; checked against SEAT_GAP

# STEMMA cable pass-through, deck centre: routes the OPT4048-to-MAX17048
# lead straight down through the deck instead of round the 3mm
# perimeter gap, so it (and the hole) stay hidden under the OPT4048
# board rather than visible round the deck's edge. Centred on the dome
# axis (DIE_OFFSET) rather than directly under either STEMMA connector
# (which sit close to the standoffs, leaving too little clearance) --
# the cable gets a short ~9.5mm sideways jog to the centre instead,
# still far shorter than the old 27.5mm perimeter route.
DECK_CABLE_D = 10.0

# ---- sensor deck ----------------------------------------------------
DECK_T = 3.0
DECK_W = 55.0                 # square; rim opening is 56. Grown from
                              # 49 by the same 6 mm EXT_W grew, using
                              # the wider rim opening rather than
                              # leaving the extra room unused.
DECK_HOLE_D = 2.9
# Corner relief is now a 45 degree chamfer (CORNER_CHAMF, derived in
# section 2), not the circular notches that used to hug the pillars.
# The corner gusset that backs the dipped seal groove reaches further
# inboard than the corner post does, so the deck and the deck wall have
# to clear the gusset on the way past it -- a circle centred on the
# post would have to be ~9.7mm radius to do that, chewing far more out
# of the deck edge than a straight chamfer does.

# Deck perimeter wall (separate printed part, 2026-07-20): stands on
# top of the deck to shield the box's own interior wall in the optical
# chamber above, so that section no longer needs painting/flocking --
# matches the deck's own footprint (same corner notches, same pillar
# registration) so it just drops down over the same 4 pillars and
# rests on top once the deck is already screwed down. A separate part
# rather than printed integrally with the deck, since a wall running
# right at the deck's edge would sit directly over the deck's own
# screw heads (see DECK_WALL_CUT_* below) -- printing it separately
# means the deck can be screwed down first, then the wall dropped in
# after, so it never needs to double as screwdriver access.
DECK_WALL_T = 2.0        # wall thickness
DECK_WALL_H = 24.0       # wall height above the deck's top surface --
                         # comfortably below the ~32.85mm gap to the
                         # lid's interior face (the P_BOSS clamp-ring
                         # bosses hang down into part of that gap, but
                         # sit at a much smaller radius -- max 22.0mm --
                         # than the wall itself, so they don't actually
                         # constrain wall height; the real ceiling is
                         # just leaving clearance to the lid's flat
                         # face so a loose drop-in part never touches it)
DECK_WALL_CUT_W = 8.0    # screw-head clearance notch width, centred
                         # on each deck screw (DECK_SCREW_X, LEDGE_CY)
DECK_WALL_CUT_H = 4.0    # notch height from the wall's base -- clears
                         # the screw head once the deck is screwed
                         # down; the wall only needs to drop in after,
                         # not provide ongoing screwdriver access
LEDGE_P = 12.75       # ledge depth from the exterior face (+/-X walls).
                      # Grown 2mm (2026-07-23, was 10.75) together with
                      # DECK_SCREW_X: at the old depth the insert pilot
                      # sat 5.5mm off the interior wall face, 33mm down
                      # a 66mm-wide open box, and there was no room to
                      # get a soldering iron in square to set the heat-
                      # set insert (nor a screwdriver on the deck screw
                      # afterwards). Now 7.5mm off the wall.
LEDGE_WY = 12.0
LEDGE_CY = -14.5      # ledge centre Y: FRONT (-Y) side, a band the
                      # sled carries nothing in, so the battery on the
                      # back face keeps its clearance to the ribs
LEDGE_H = 12.0
DECK_SCREW_X = 23.0   # deck screw axis; drives ledge pilot AND deck
                      # hole so the two can never drift apart. Was
                      # 22.0 at DECK_W=49, then 25.0; moved back in by
                      # 2mm (2026-07-23) with LEDGE_P, for iron and
                      # screwdriver access -- see the LEDGE_P note. The
                      # ledge grew inboard by the same 2mm so the pilot
                      # keeps its wall on the inboard side.
DECK_SLED_GAP = 3.0   # deck underside to sled top edge

# ---- sled -----------------------------------------------------------
SLED_T = 3.0
SLED_W = 55.0                 # grown to match DECK_W (see above)
SLED_PLANE_Y = 6.0    # mid-plane of the sled (biased +Y, battery side)
CH_GAP = SLED_T + 0.4
FENCE_CLR = 0.4       # per-side X clearance either side of the sled
                      # edge, left open in the guide fences below (see
                      # "Fixed 2026-07-20 (sled X-play)" -- the rib
                      # channel used to leave the sled's whole width
                      # unconstrained sideways since CH_GAP was open
                      # across the full rib span, not just at the
                      # sled's own edge)
RIB_W = 4.0
RIB_P = 6.0           # rib protrusion from the wall. Was 5.5 at
                      # EXT_W=60/SLED_W=49; only nudged, not scaled
                      # 1:1 with EXT_W, because RIB_IN_X needs to sit
                      # in a narrow band now: <=25.5 to keep >=2 mm
                      # sled engagement (SLED_W grew to 55 too), but
                      # >=23.65 to leave the battery cradle >=2 mm to
                      # the rib channels. RIB_P=6.0 gives RIB_IN_X=24.5,
                      # comfortably inside both.
SLED_BOT_CLEAR = 0.0  # sled rests on the box floor: floor-rest IS the
                      # vertical datum (cable loop coils beside it)
SLED_TOP_MARGIN = 4.0
SLED_BOT_MARGIN = 30.0 # was 8; the BQ DC-jack keep-out already eats
                      # ~3 mm of this (see BQ_W/BQ_L note), and a real
                      # DC barrel plug plus its cable bend needs a lot
                      # more room than that below it to actually mate
                      # with the jack, on top of the PG7 gland/vent
                      # sitting in this same bottom zone. Unverified
                      # against the actual plug -- revisit once it's
                      # in hand.
ROW_GAP = 6.0
BOSS_D = 8.6          # was 6.0, then 8.0 -- same insert-bulge issue and
                      # same extra-margin request as STAND_D (wall
                      # around M25_INS_D now 2.55mm, up from 2.25mm).
                      # Capped below the 10.0 used for STAND_D: this is
                      # now also the QT Py mount's boss diameter (QT
                      # switched from M3 to M2.5, 2026-07-20), and QT's
                      # wide 34mm hole pitch means anything above ~8.9
                      # fouls the deck ledge clearance the sled must
                      # pass during insertion (see the FRONT_ENV_X
                      # assertion below) -- 8.6 leaves a bit of margin
                      # under that ceiling.
BOSS_H = 4.0

# board registry: outline (W across sled, L along sled) + hole pitch.
# Measured from Adafruit's own CAD, not datasheet guesses -- see
# mechanical/adafruit-cad-files/. Re-check with calipers before printing.
BQ_W, BQ_L, BQ_PX, BQ_PY = 33.02, 38.1, 27.94, 33.02
    # Adafruit_BQ24074_V5.step, confirmed against adafruit_BQ24074.png
    # (1.50 x 1.30 in outline, 1.30 x 1.10 in pitch; W/L and PX/PY
    # swapped from the native drawing on purpose). 4 corner holes,
    # Ø2.5 mm, inset 2.54 mm (0.1 in) from every edge.
    # Board is rotated 90 deg from its native orientation: the DC/
    # barrel-jack connector overhangs the native-X edge, and mounting
    # it that way round put the jack's overhang into the deck-ledge
    # clearance band (real pitch is 2.5 mm bigger than the old
    # placeholder, which is what surfaced this). Rotating it means the
    # jack now overhangs along the sled length instead of across it --
    # which also happens to point the connector at the bottom of the
    # box, right next to the PG7 gland, which is where the solar lead
    # needs to plug in anyway.
MAX_W, MAX_L = 25.4, 20.32    # "5580 MAX17048.step"; outline unchanged
MAX_PX = 20.32                # from the previous VERIFY-flagged value
    # Real board has only 2 mounting holes, both on one edge (not the
    # symmetric 4-hole rectangle the old MAX_PY assumed) -- Ø2.5 mm,
    # offset MAX_HOLE_DY below the board centreline.
MAX_HOLE_DY = -7.62

# QT Py: the bare board has no mounting holes, so it rides in
# Adafruit's snap mount (#6183) instead of the old zip-tied tray.
# Measured from QTPy_Snap_Mount_SLA_V2.stl (native footprint 42 x 28,
# 4x M3 holes at 34 x 20 pitch). Native orientation (long axis ACROSS
# the sled) puts the USB-C port at the top for easy(ish) access; an
# earlier revision rotated this 90 deg to dodge the deck-ledge
# clearance zone, but that buried the USB-C port sideways, so the box
# was widened instead (EXT_W) to keep the native orientation.
QT_MOUNT_W, QT_MOUNT_L = 42.0, 28.0
QT_MOUNT_PX, QT_MOUNT_PY = 34.0, 20.0
# QT mount switched from M3 to M2.5 (2026-07-20): M3 was a tight fit on
# the snap mount's own holes. Now uses the shared BOSS_D/BOSS_H/
# M25_INS_D/M25_INS_L, same as BQ24074 and MAX17048 -- no QT-specific
# boss/insert parameters needed any more.
QT_MOUNT_LIFT = 2.4   # snap mount's own lift of the PCB above the boss
                      # face (same figure the reference body uses)
QT_STACK_Y = 4.0      # everything standing proud of the QT Py's PCB:
                      # the USB-C shell and the snap mount's retaining
                      # walls. VERIFY with calipers -- this is the one
                      # number in the ledge clearance check below that
                      # isn't taken from Adafruit's own CAD, and the
                      # check has ~0.6mm of margin, so a bad guess here
                      # is a real collision, not a rounding error.
QT_W, QT_L = 17.78, 20.70     # bare QT Py PCB, reference body only now
BAT_L, BAT_W, BAT_T = 62.5, 38.5, 8.3
BAT_TOP_OFF = 52.0    # battery top below the sled top edge. Was 20;
                      # moved down 32 mm (2026-07-19)

# JST-PH pass-through, back face to front face: lets the battery's own
# JST-PH lead reach through the sled to plug into MAX17048's battery
# input on the front face. Sits beside MAX's board (to its left, at
# MAX's own row centre), clear of MAX's mounting boss, the QT mount
# boss above, and the cradle's own mounting screws behind it.
PH_HOLE_D = 8.0
PH_HOLE_X = -20.0      # left of MAX_W's own edge (board is +/-12.7
                      # wide, centred at X=0)
# PH_HOLE_OFF (MAX's own row centre) is derived in section 2, once
# MAX_CTR exists.

# Battery cradle: a separate printed part that clips onto the sled's
# plain back face via a rail-and-groove slide -- replacing both the
# old zip-tie slots AND the screw-mounted bosses that came after them
# (2 small boss studs still broke the sled's flat-print face; see the
# sled's print-orientation note). Reuses the same slide-and-gravity-
# seat idiom already proven for the pole mount rail and the sled's own
# rib channels: 2 rails on the cradle's base slide down into 2
# matching grooves cut into the sled (a cut, not a boss, so the sled
# stays flat) and seat against a closed-bottom hard stop, glued once
# seated -- plain right-angle cross-section, not tapered, since glue
# (not a dovetail undercut) is what actually holds it now. Zero
# screws, zero inserts for this joint. It encloses the battery on 4 sides
# (base, 2 long walls, closed end, top wall) and is open only at one
# end for a lengthwise slide-in -- no ties needed (doesn't need to be
# airtight, just enough to keep the battery from sliding around).
CRADLE_CLR = 0.4       # snug clearance around the battery's W and T
CRADLE_CLR_L = 1.0     # extra length clearance at the open (slide-in) end
CRADLE_WALL = 2.0      # cradle wall thickness (sides, closed end, top, base)
CRADLE_SLOT_W = 24.0   # wide open column through the top wall: clears a
                      # thermistor taped to the battery pack, which the
                      # tight 0.4 mm CRADLE_CLR top clearance wouldn't
                      # otherwise fit.
CRADLE_SLOT_MARGIN = 4.0  # top-wall material kept at the closed end of
                      # the slot, tying the 2 side walls together
                      # there (the mouth end is already open, so the
                      # slot just runs out to it, no margin needed)

# Rail-and-groove slide mount (rail on the cradle, matching groove cut
# into the sled). Plain right-angle cross-section, no taper (de-
# chamfered 2026-07-20 -- see the "Simplified" note below): glue
# provides the actual retention now that it's a proven part of the
# assembly, so the dovetail-style undercut this used to have is no
# longer needed, and a straight-walled slot is far simpler to print
# and fit reliably than a tapered one.
CRADLE_RAIL_W = 5.0     # rail/groove width (constant along the depth)
CRADLE_RAIL_H = 1.2     # rail height = groove depth into the sled
                       # (well inside the 3 mm plate; leaves 1.8 mm of
                       # solid sled material toward the front face)
CRADLE_RAIL_CLR = 0.3   # per-side/per-depth sliding clearance
CRADLE_RAIL_X = 15.0    # rail offset from centreline (+/-), 2 rails
CRADLE_RAIL_END_MARGIN = 3.0  # rail doesn't run the cradle's full
                       # length -- stops short at each end so there's
                       # solid wall material there

# ---- bottom fittings ------------------------------------------------
GLAND_D = 12.5        # PG7 -- confirmed 2026-07-21 against the actual
                      # fitting: 12.2mm (the original guess, shared
                      # with the vent) printed too tight to thread the
                      # gland body through
GLAND_POS = (-12.0, -15.0)
VENT_D = 12.2         # M12 breather -- confirmed fit at 12.2mm 2026-07-21
VENT_POS = (12.0, -15.0)

# ---- external antenna bulkhead (+X wall, WiFi or Cellular-1) --------
# Only one antenna is ever fitted at a time -- WiFi (Taoglas GW.29.A153,
# RP-SMA(M), via the RS PRO 794-2841 RP-SMA(F)-to-uFL pigtail, datasheet
# in mechanical/reference-links/) or Cellular-1's M5Stamp CAT-M modem
# (Siretta ASMGB020X113S11, SMA(F)-to-MHF5L) -- so one hole serves
# either. Both are standard 1/4-36 UNS-2A SMA-family bulkhead thread;
# polarity (SMA vs RP-SMA) only changes the centre pin, not the thread
# or panel-hole geometry, confirmed against the 794-2841 datasheet.
# Wall choice (+X vs -X) is arbitrary -- geometry is symmetric, so this
# is trivially mirrorable if the deployed orientation ends up preferring
# the other side.
ANT_HOLE_D = 6.5      # 1/4-36 UNS-2A major dia 6.35mm + clearance --
                      # unverified against the actual part; treat like
                      # GLAND_D/VENT_D and confirm/tune on a test-fit
                      # before committing to a full box print. Also
                      # worth a slicer check before printing: unlike
                      # the gland/vent (vertical-axis holes through the
                      # bottom face, no overhang), this is a horizontal
                      # hole through a vertical wall -- the same class
                      # of bridging concern that got the -Y switch hole
                      # left as a dimple-only, hand-drilled feature
                      # below. At 6.5mm (vs the switch's problematic
                      # 16mm) this should bridge fine in ASA, but it's
                      # a judgement call, not a proven one.
ANT_HOLE_Y = LEDGE_CY  # same front-band Y position as the deck mounts,
                      # per Paul's placement call -- clear of the rib
                      # channels/guide fences (a different Y-band, see
                      # assertion below) and of the sled's own
                      # front-facing components, which don't reach this
                      # far forward. The deck ledge shares this Y band
                      # too but sits high near DECK_SEAT_Z, well above
                      # ANT_HOLE_Z below -- no Z overlap.
ANT_HOLE_Z = 20.0     # off the floor -- raised from an initial ~12-15mm
                      # first pass at Paul's request, for real
                      # finger/wrench access to run the nut on from
                      # inside the box.

# ---- on/off switch (-Y wall, Cellular-1) -----------------------------
# Adafruit #916 16mm rugged metal on/off switch, "kill load only" --
# splices into BQ24074 LOAD/OUT between it and the QT Py 5V pin (see
# CLAUDE.md). Position agreed 2026-07-23 via an interference sweep
# against sled_refs_asm/cradle_asm: the -Y wall's only obstruction is
# the BQ24074 DC-jack keepout (z~30-45, x~-8..+20), well clear of here.
SWITCH_D = 16.0        # not cut yet -- the size to hand-drill later.
                        # Kept as documentation/reference, not consumed
                        # by any geometry below.
SWITCH_X = 0.0
SWITCH_Z = 95.0
SWITCH_DIMPLE_D = 2.0   # shallow drill-guide dimple, exterior face --
SWITCH_DIMPLE_DEPTH = 0.6  # a punch mark, not a hole. Depth << WALL so
                        # the box stays sealed if never drilled.
                        # NO INTERIOR BOSS -- Paul's explicit call,
                        # requested twice (2026-07-27, then again
                        # 2026-07-28 after it was mistakenly restored
                        # here from an unrelated session's diff). Do
                        # NOT re-add SWITCH_BOSS_D/SWITCH_BOSS_H: he is
                        # handling guaranteed-solid material at this
                        # spot himself via a slicer modifier (solid
                        # infill painted on this region), not CAD. The
                        # wall here is plain WALL-thickness material,
                        # same as the rest of the -Y wall.

# ---- dovetail rail (+Y wall, shared mount standard) -----------------
RAIL_TIP_TOP = 23.0   # outer face width at the top of the rail segment
RAIL_NECK_TOP = 17.0  # width at the wall at the top of the rail segment
RAIL_DEPTH = 4.5
RAIL_TAPER = 1.4      # total width reduction top -> bottom, AS IF the
                      # rail ran the full box height (approx 0.5
                      # degrees, self-seating). The rail itself is now
                      # a shorter centred segment (see RAIL_LEN below),
                      # so the angle -- not this absolute mm figure --
                      # is what actually carries over; RAIL_TAPER_SEG
                      # derives the shorter segment's real reduction.
RAIL_MARGIN = 5.0     # printed rail length = bracket engagement depth
                      # (BRK_H - BRK_FLOOR) + this margin, so there's a
                      # little lead-in before the rail hits the hard
                      # stop

# ---- pole bracket ---------------------------------------------------
BRK_W = 40.0
BRK_D = 30.0
BRK_H = 80.0
BRK_FLOOR = 10.0      # receiver floor height = backup hard stop
BRK_CLR_SIDE_TOP = 0.25    # per flank, at the slot's TOP (where the box
BRK_CLR_DEPTH_TOP = 0.3    # first enters) -- kept generous for a smooth,
                        # forgiving initial engagement regardless of
                        # print variance.
BRK_CLR_SIDE_BOT = 0.10    # at the slot's BOTTOM (the hard stop, where
BRK_CLR_DEPTH_BOT = 0.15   # it fully seats) -- deliberately tighter than
                        # the top. With no thumbscrew backup any more
                        # (removed 2026-07-24, friction-only retention),
                        # the final seated grip has to come from here:
                        # a uniform clearance loose enough to slide on
                        # easily was also too loose to hold once seated
                        # (confirmed on a real print, 2026-07-27). A
                        # first test increment, not a guaranteed final
                        # number -- print, test-fit, and tune from here
                        # the same way SPACER_T_TRIM gets tuned in the
                        # Cellular-1 dome seal. Deliberately still a
                        # positive clearance, not an interference fit --
                        # ASA doesn't flex well enough to press-fit
                        # safely (see the battery cradle ear-clip note).
VG_DEPTH = 8.0        # 120 degree pole V-groove
VG_HALF = 14.0
TUN_Y = (9.0, 17.0)   # clamp tunnel band (local y, from the front face)
TUN_ZC = (22.0, 58.0)
TUN_H = 16.0           # tunnel's vertical extent -- the dimension the
                        # clamp band's own width has to pass through.
                        # Widened 12->16mm (2026-07-24) for Paul's actual
                        # jubilee clamps, ~14mm band width; 12mm was too
                        # tight. TUN_Y (the 8mm depth/thickness-clearance
                        # band) was already generous and is unchanged.
BRK_CHAMF = 3.0        # stress-relief chamfer where the clamp band bends
                        # round a sharp printed edge: the block's front
                        # corner (side face meets the V-groove/back face,
                        # full BRK_H) and all 4 tunnel mouths (side face
                        # meets the tunnel's inner wall, full TUN_H)

# ---- wall-mount bracket (alternative to the pole bracket) ------------
# Same box-mating block/dovetail receiver as the pole bracket above
# (identical BRK_W/BRK_D/BRK_H, same slot/engagement/friction-fit
# clearances), so it's a drop-in alternative on the box side. Instead of
# the V-groove + hose-clamp tunnels, it has two countersunk screw holes
# drilled through the floor of the dovetail channel itself -- driven
# from inside the open channel (accessible before the box is fitted),
# countersunk flush with the channel floor so the heads never protrude
# into the rail's path. Once the box's rail slides down into the slot,
# it covers the screw heads completely.
WMT_HOLE_D = 5.0        # clearance hole, #8 wood screw shank + clearance
WMT_CS_D = 9.0           # countersink (flat-head) diameter, #8 wood screw
WMT_CS_ANGLE = 82.0      # degrees -- standard wood-screw countersink
WMT_HOLE_ZC = (20.0, 65.0)   # near the block's bottom / top, clear of
                              # BRK_FLOOR and the slot's top mouth
WMT_CS_Y0 = RAIL_DEPTH + BRK_CLR_DEPTH_BOT - 0.3
                              # countersink must OPEN INTO the slot
                              # channel (that's the whole point -- a
                              # screwdriver reaches it through the open
                              # channel before the box is fitted), not
                              # sit sealed behind it. The channel's own
                              # floor is only ~4.65-4.8mm deep over the
                              # loft; starting the countersink 0.3mm
                              # shallower than the shallowest point
                              # guarantees real overlap/breakthrough at
                              # every WMT_HOLE_ZC position, the same
                              # "genuine overlap" idiom used elsewhere
                              # in this script for guaranteed boolean
                              # connections.
WMT_CS_DEPTH = ((WMT_CS_D - WMT_HOLE_D) / 2
                / math.tan(math.radians(WMT_CS_ANGLE / 2)))

EXPORT = True
OUT_DIR = "exports"    # individual parts land in OUT_DIR/components/,
                        # the full assembly in OUT_DIR/assembly/ --
                        # kept apart so a fresh assembly export can't
                        # get mistaken for (or overwrite) a part file
BUILD_COUPON = False   # port test coupon (seal stack on a pocket-sized
                      # plate) -- was a proven-fit check early on;
                      # off by default now the port seal stack is
                      # settled, flip back on to re-check after any
                      # port/seal parameter change
BUILD_GLAND_COUPON = False  # small bottom-face test plate (PG7 gland +
                      # M12 vent holes, real spacing) -- was on while
                      # GLAND_D was being confirmed against the actual
                      # fitting (2026-07-21: bumped 12.2 -> 12.5 after
                      # the gland printed too tight); confirmed fitting
                      # 2026-07-22, off by default now. Flip back on to
                      # re-check after any bottom-fitting change

# =====================================================================
# 2. DERIVED DIMENSIONS
#    Everything hangs off the lid interior plane and flows down.
# =====================================================================

# port stack, measured as drop below the lid interior face
P_BOSS_STAND = (FLANGE_T - RECESS_D) + ORING_CS * (1 - ORING_SQUEEZE)
CLAMP_FACE_DROP = P_BOSS_STAND + SPACER_T_NOMINAL  # boss hard-stop faces
                                                  # -- keyed to the nominal,
                                                  # not the trimmed actual
                                                  # spacer thickness, so
                                                  # tuning SPACER_T_TRIM
                                                  # never moves the lid's
                                                  # own boss geometry
TUBE_END_DROP = CLAMP_FACE_DROP + CLAMP_T + TUBE_L
BOARD_TOP_DROP = TUBE_END_DROP + SEAT_GAP
BOARD_BOT_DROP = BOARD_TOP_DROP + BOARD_T
DECK_TOP_DROP = BOARD_BOT_DROP + STAND_H
DECK_BOT_DROP = DECK_TOP_DROP + DECK_T
SLED_TOP_DROP = DECK_BOT_DROP + DECK_SLED_GAP

# sled height from the component stack (front face rows), top to
# bottom: QT Py snap mount, MAX17048, BQ24074 -- BQ last so it sits
# nearest the bottom PG7 gland for the solar lead.
_row0 = SLED_TOP_MARGIN                          # QT Py snap mount
_row1 = _row0 + QT_MOUNT_L + ROW_GAP             # MAX17048
_row2 = _row1 + MAX_L + ROW_GAP                  # BQ24074
SLED_H = _row2 + BQ_L + SLED_BOT_MARGIN
QT_CTR = _row0 + QT_MOUNT_L / 2
MAX_CTR = _row1 + MAX_L / 2
BQ_CTR = _row2 + BQ_L / 2

# box height, fully derived
INT_D = SLED_TOP_DROP + SLED_H + SLED_BOT_CLEAR
H_BOX = BOTTOM_T + INT_D
RIM_IN = EXT_W - 2 * RIM_T
DECK_SEAT_Z = H_BOX - DECK_BOT_DROP

# ---- seal-inside-the-screws corner geometry -------------------------
# All four numbers are one chain, each derived from the one above it,
# so the only knob is SEAL_SCREW_WALL. Expressed as "x + y = <sum>"
# lines, because every boundary here is a 45 degree chamfer across a
# corner: a perpendicular offset of d moves the line's sum by d*sqrt(2).
#
#   SEAL_CHAMF    groove CENTRELINE across the corner, set by keeping
#                 SEAL_SCREW_WALL between the groove's outer edge and
#                 the screw's insert pocket
#   GUSSET_SUM    inner face of the corner gusset: the material that
#                 backs the groove where it has left the rim band
#   GUSSET_H      how far down the gusset runs: a straight section that
#                 carries the groove's full depth, then a 45 degree
#                 printable underside receding back into the corner
#   CORNER_CHAMF  the deck / deck wall corner chamfer, which has to get
#                 past the gusset on its way in and out
SEAL_CHAMF = 2 * PIL_POS - math.sqrt(2) * (M3_INS_D / 2
                                           + SEAL_SCREW_WALL
                                           + GROOVE_W / 2)
GUSSET_SUM = SEAL_CHAMF - math.sqrt(2) * (GROOVE_W / 2 + GUSSET_MARGIN)
# The straight section is NOT optional and NOT just belt and braces:
# the groove is cut GROOVE_D into the rim face, and a gusset that
# starts receding at the face itself has already pulled back behind the
# groove's inner wall by the time you are halfway down the channel --
# caught by point-probing the groove's inner land at mid-depth, where a
# check on the rim face alone looked perfectly fine. Same failure as
# the 2026-07-19 corner gap (an O-ring channel open into a void), one
# feature along. Keep the taper below the groove floor, never beside it.
GUSSET_STRAIGHT = GROOVE_D + 1.0
GUSSET_TAPER = (RIM_IN + 0.6 - GUSSET_SUM) / math.sqrt(2)
GUSSET_H = GUSSET_STRAIGHT + GUSSET_TAPER
CORNER_CHAMF = GUSSET_SUM - math.sqrt(2) * CORNER_CHAMF_CLR
SLED_TOP_Z = H_BOX - SLED_TOP_DROP
PIL_TOP_Z = H_BOX      # pillars now run flush to the true rim top (see
                      # the corner-pillar build below for why this
                      # changed from H_BOX - GROOVE_D)
PORT_ENV_R = max(CLAMP_OD / 2, P_BOSS_BCD / 2 + P_BOSS_D / 2)
RIB_IN_X = EXT_W / 2 - WALL - RIB_P              # rib inner face, 22.0

# battery cradle footprint, offset-from-sled-top terms (see CRADLE_*
# params). V0 = open (slide-in) end, V1 = closed (hard-stop) end.
CRADLE_V0 = BAT_TOP_OFF - CRADLE_CLR_L
CRADLE_V1 = BAT_TOP_OFF + BAT_L
CRADLE_LEN = CRADLE_V1 - CRADLE_V0        # open-to-closed span
CRADLE_OUT_L = CRADLE_LEN + CRADLE_WALL   # + wall at the closed end only

# JST-PH pass-through offset: MAX's own row centre, nudged up clear of
# the battery cradle's mouth-end corner if the two would otherwise
# overlap (the cradle's width reaches out to +/-CRADLE_OUT_W/2, wide
# enough to still catch the hole even though PH_HOLE_OFF < CRADLE_V0).
PH_HOLE_OFF = min(MAX_CTR, CRADLE_V0 - PH_HOLE_D / 2 - 2.0)
CRADLE_OUT_W = BAT_W + 2 * CRADLE_CLR + 2 * CRADLE_WALL
CRADLE_OUT_T = BAT_T + 2 * CRADLE_CLR + 2 * CRADLE_WALL

# rail span (offset-from-sled-top terms): rail's own bottom
# (CRADLE_RAIL_BOT) is the hard-stop end, matching the groove's closed
# bottom, so the cradle always seats at the same position regardless
# of how far it started from engaged. No separate "channel" span any
# more -- with the taper gone there's no assembly-path problem to
# solve with an oversized entry zone, so the groove just matches the
# rail's own length exactly.
CRADLE_RAIL_TOP = CRADLE_V0 + CRADLE_RAIL_END_MARGIN
CRADLE_RAIL_BOT = CRADLE_V1 - CRADLE_RAIL_END_MARGIN
CRADLE_RAIL_LEN = CRADLE_RAIL_BOT - CRADLE_RAIL_TOP

# dovetail rail: a short segment matching the bracket's engagement
# depth, centred on the box height, not full height. A full-height
# rail only ever had its bottom (BRK_H - BRK_FLOOR) worth of length
# actually inside the bracket -- the bracket's receiver is a closed-
# bottom pocket, so the rail's own bottom end is what travels down and
# hits the hard stop, regardless of how much rail hangs above the
# bracket unengaged. Centring the segment moves that grip point from
# the box's bottom to its middle.
RAIL_ENGAGE = BRK_H - BRK_FLOOR
RAIL_LEN = RAIL_ENGAGE + RAIL_MARGIN
RAIL_Z0 = (H_BOX - RAIL_LEN) / 2      # rail's own bottom (box-absolute z)
RAIL_TAPER_SEG = RAIL_TAPER * RAIL_LEN / H_BOX
    # RAIL_TAPER was tuned as a total reduction over the full box
    # height (the ~0.5 degree self-seating angle); scale it down so
    # the shorter segment keeps that same angle instead of steepening.

def _rail_halves(z_local):
    """Half widths (tip, neck) at height z_local above the rail's own
    bottom end (the end that seats against the bracket's hard stop)."""
    shrink = RAIL_TAPER_SEG * (1 - z_local / RAIL_LEN)
    return (RAIL_TIP_TOP - shrink) / 2, (RAIL_NECK_TOP - shrink) / 2

# =====================================================================
# 3. ASSERTION GUARDS
#    Illegal moves fail loudly, with the remedy named.
# =====================================================================

def _req(ok, msg):
    if not ok:
        raise AssertionError(msg)

_req(RIM_IN / 2 >= PORT_ENV_R + 1.0,
     "Rim opening too small for the port hardware envelope. "
     "Reduce CLAMP_OD / P_BOSS_BCD or reduce RIM_T.")

_req(PIL_POS * math.sqrt(2) - PIL_R >= PORT_ENV_R + 1.0,
     "Corner pillars intrude on the port hardware envelope. "
     "Increase PIL_POS or reduce PIL_R.")

_req(PIL_POS + PIL_R >= EXT_W / 2 - WALL,
     "Corner pillars no longer weld into the walls; they would print "
     "as free-standing towers. Increase PIL_POS or PIL_R.")

# groove ring must stay on the rim face with 0.8 lands
_req(GROOVE_OFF - GROOVE_W / 2 - 0.8 >= RIM_IN / 2 and
     GROOVE_OFF + GROOVE_W / 2 + 0.8 <= EXT_W / 2,
     "Seal groove leaves the rim face. Adjust GROOVE_OFF/GROOVE_W "
     "or widen RIM_T.")

# ---- the seal must pass INSIDE the lid screws, all the way round ----
# Perpendicular distance from a corner screw axis to the groove's
# chamfer line. Positive = the chamfer is on the box-centre side of the
# screw, which is the whole point of the corner rework.
_scr_to_chamf = (2 * PIL_POS - SEAL_CHAMF) / math.sqrt(2)

_req(_scr_to_chamf - GROOVE_W / 2 - M3_INS_D / 2 >= SEAL_SCREW_WALL - 1e-9,
     "Seal groove runs into the lid-screw insert pocket at the corner. "
     "The groove has to stay inboard of the screw with SEAL_SCREW_WALL "
     "of rim material between them -- reduce SEAL_SCREW_WALL, or the "
     "screws have nowhere further out to go and the corner needs a lug.")

_req(_scr_to_chamf - GROOVE_W / 2 - LID_SCREW_D / 2 >= 1.0,
     "Lid screw clearance hole breaks into the seal groove at the "
     "corner. Reduce LID_SCREW_D or increase SEAL_SCREW_WALL.")

# the groove's 8 vertices are rounded off so the cord never turns a
# sharp corner. The inner ring takes the smallest radius, and each
# fillet has to fit on the edges either side of its own vertex.
_req(GROOVE_RC - GROOVE_W / 2 >= 0.5,
     "Seal groove's inner corner radius has collapsed -- the ring can't "
     "keep a constant width round a corner tighter than its own half "
     "width. Increase GROOVE_RC.")
for _tag, _half, _sum, _rad in (
        ("outer", GROOVE_OFF + GROOVE_W / 2,
         SEAL_CHAMF + math.sqrt(2) * GROOVE_W / 2, GROOVE_RC + GROOVE_W / 2),
        ("inner", GROOVE_OFF - GROOVE_W / 2,
         SEAL_CHAMF - math.sqrt(2) * GROOVE_W / 2, GROOVE_RC - GROOVE_W / 2)):
    _tan = _rad * math.tan(math.radians(22.5))   # 135 deg interior angle
    _flat_run = _sum - _half                     # vertex to the mid-flat
    _chamf_run = math.sqrt(2) * abs(_half - _sum / 2)  # vertex to 45 deg
    _req(_tan <= _flat_run and _tan <= _chamf_run,
         f"Seal groove corner fillet doesn't fit on the {_tag} ring: "
         f"needs {_tan:.2f}mm of run either side of the vertex, has "
         f"{_flat_run:.2f} along the flat and {_chamf_run:.2f} along the "
         f"chamfer. Reduce GROOVE_RC.")

# ...and the screws must keep their own wall to the outside world,
# which is what pins PIL_POS. Both directions matter: the flat wall
# face and the exterior corner radius.
_req(EXT_W / 2 - PIL_POS - M3_INS_D / 2 >= SCREW_WALL_OUT - 1e-9,
     "Lid-screw insert pocket has no wall left to the flat exterior "
     "face. Reduce SCREW_WALL_OUT/M3_INS_D or widen EXT_W.")
_req(((EXT_W / 2 - BOX_R) * math.sqrt(2) + BOX_R)
     - PIL_POS * math.sqrt(2) - M3_INS_D / 2 >= SCREW_WALL_OUT - 1e-9,
     "Lid-screw insert pocket has no wall left to the exterior corner "
     "radius. Reduce SCREW_WALL_OUT/M3_INS_D or increase BOX_R.")

# The dipped groove has left the rim band, so the corner gusset is now
# the only thing backing its inner wall -- the same class of failure as
# the 2026-07-19 corner-gap bug (groove channel opening into a void),
# just at a different feature. Chamfer-to-chamfer, so this margin is
# uniform the whole way across the corner, not a worst-case point.
_req((SEAL_CHAMF - math.sqrt(2) * GROOVE_W / 2 - GUSSET_SUM)
     / math.sqrt(2) >= GUSSET_MARGIN - 1e-9,
     "Corner gusset doesn't reach inboard of the seal groove -- the "
     "groove's inner wall would open into the box. Reduce GUSSET_SUM "
     "or SEAL_SCREW_WALL.")

# the gusset is an added-material chamfer inside the rim opening, so it
# has to be a real corner cut and not swallow the flats
_req(RIM_IN / 2 < GUSSET_SUM < RIM_IN,
     "Corner gusset chamfer is degenerate: it must cut the rim "
     "opening's corner without reaching its flat faces. Check "
     "SEAL_CHAMF/GUSSET_MARGIN.")

# the gusset's straight section must carry the groove's full depth
# before the underside starts receding -- otherwise the groove's inner
# wall is backed at the rim face and unbacked at the bottom of the
# channel, which reads as fine on a face-level check
_req(GUSSET_STRAIGHT >= GROOVE_D + 0.5,
     "Corner gusset starts tapering beside the seal groove rather than "
     "below it -- the groove's inner wall would lose its backing part "
     "way down the channel. Increase GUSSET_STRAIGHT.")

# the gusset's 45 degree printable underside has to recede back into
# the corner within the straight rim band, not down into the taper
_req(GUSSET_H <= RIM_BAND,
     "Corner gusset runs past the bottom of the rim band into the 45 "
     "degree cavity taper. Increase RIM_BAND or GUSSET_SUM.")

# everything that is lowered in through the rim opening has to get past
# the gusset. The deck and the deck wall are chamfered to match; the
# sled and the battery cradle are not, so they are checked outright.
_req(CORNER_CHAMF + math.sqrt(2) * CORNER_CHAMF_CLR <= GUSSET_SUM + 1e-9,
     "Deck / deck wall corner chamfer fouls the corner gusset during "
     "insertion. Reduce CORNER_CHAMF.")

_req(SLED_W <= RIM_IN - 0.5,
     "Sled cannot pass the rim opening. Reduce SLED_W or RIM_T.")

_req(SLED_W / 2 - RIB_IN_X >= 2.0,
     "Sled edges engage the rib channels by less than 2 mm. "
     "Increase RIB_P or SLED_W.")

_req(DECK_W <= RIM_IN - 0.5,
     "Deck cannot pass the rim opening. Reduce DECK_W or RIM_T.")

# the sled and the battery cradle go in through the same rim opening
# but carry no corner chamfer of their own -- their plan-view corners
# are checked against the gusset directly. (Both sit in a narrow Y band
# well away from the corners, so these have plenty of margin; they are
# here so a future growth in SLED_W or the battery can't quietly start
# fouling a corner that nothing used to reach.)
_req(SLED_W / 2 + (SLED_PLANE_Y + SLED_T / 2) + 0.8 <= GUSSET_SUM,
     "Sled corner fouls the corner gusset on the way in. Reduce "
     "SLED_W/SLED_PLANE_Y or move GUSSET_SUM outboard.")
_req(CRADLE_OUT_W / 2 + (SLED_PLANE_Y + SLED_T / 2 + CRADLE_OUT_T)
     + 0.8 <= GUSSET_SUM,
     "Battery cradle corner fouls the corner gusset on the way in. "
     "Reduce the cradle envelope or move GUSSET_SUM outboard.")

# the deck's corner chamfer must clear the corner posts too, not just
# the gusset (the posts run full height; the gusset is rim-band only).
# Perpendicular distance from the post's axis to the chamfer line.
_req((2 * PIL_POS - CORNER_CHAMF) / math.sqrt(2) >= PIL_R + 0.5,
     "Deck corner chamfer fouls the corner posts. Reduce CORNER_CHAMF "
     "or PIL_R.")

# deck screw holes must survive the corner chamfer
_req((CORNER_CHAMF - (DECK_SCREW_X + abs(LEDGE_CY))) / math.sqrt(2)
     >= DECK_HOLE_D / 2 + 0.6,
     "Deck screw holes fall into the deck's corner chamfer. Move "
     "LEDGE_CY/DECK_SCREW_X further from the corner.")

# deck screw holes must sit fully inside the deck edge
_req(DECK_SCREW_X + DECK_HOLE_D / 2 + 0.4 <= DECK_W / 2,
     "Deck screw holes break out of the deck edge. Reduce "
     "DECK_SCREW_X or enlarge DECK_W (rim opening permitting).")

# ledge insert pilot must sit inside the ledge material
LEDGE_IN_X = EXT_W / 2 - LEDGE_P
_req(DECK_SCREW_X - M25_INS_D / 2 - 0.8 >= LEDGE_IN_X - 0.01,
     "Ledge insert pilot has no wall on its inboard side. Increase "
     "LEDGE_P or DECK_SCREW_X.")

# ledges live on the front: they must clear the sled channel band...
_req(LEDGE_CY + LEDGE_WY / 2 <= SLED_PLANE_Y - CH_GAP / 2 - 0.4 or
     LEDGE_CY - LEDGE_WY / 2 >= SLED_PLANE_Y + CH_GAP / 2 + 0.4,
     "Deck ledges intrude into the sled channel band. Move LEDGE_CY "
     "clear of SLED_PLANE_Y.")

# ...and clear everything mounted on the sled front face during descent.
#
# This used to be a single X-only test against the widest thing on the
# front face (the QT snap mount's bosses, at +/-21.3), which capped
# LEDGE_IN_X at 22.1 and left LEDGE_P with 0.15mm of slack -- no room
# at all to move the ledges inboard for tool access. That test was
# simply too blunt (2026-07-23): a ledge and a board only collide if
# they overlap in BOTH axes, and the ledges sit in a narrow Y band on
# the FRONT of the box that most of the front-face stack never reaches
# into. Confirmed against the physical assembly before relaxing it.
#
# So each front-face item is checked properly: it must clear the ledge
# either in X (it never passes over the ledge) or in Y (it is not deep
# enough to touch it when it does). Y projections are measured off the
# sled's own front face, and match the reference bodies below.
FRONT_ENV_X = max(BQ_PX / 2 + BOSS_D / 2, MAX_PX / 2 + BOSS_D / 2,
                  QT_MOUNT_PX / 2 + BOSS_D / 2,
                  BQ_W / 2, QT_MOUNT_W / 2)
FRONT_TALL_X = 10.5   # BQ DC/barrel jack zone, post-rotation: the jack
FRONT_TALL_Y = 11.0   # overhangs ~10.1 mm off centre across the sled
                      # (was ~22 mm before rotating BQ 90 deg -- that
                      # overhang now runs along the sled length instead,
                      # where there's no ledge to foul). FRONT_TALL_Y is
                      # the jack's height above its board.
                      # Both measured off Adafruit_BQ24074_V5.step.
BOARD_COMP_Y = 5.0    # generic component height above a breakout PCB,
                      # for the boards with nothing tall on them

# (name, half X extent, Y projection off the sled's front face)
_FRONT_ITEMS = (
    ("QT Py snap mount", max(QT_MOUNT_W / 2, QT_MOUNT_PX / 2 + BOSS_D / 2),
     BOSS_H + QT_MOUNT_LIFT + 1.2 + QT_STACK_Y),
    ("MAX17048", max(MAX_W / 2, MAX_PX / 2 + BOSS_D / 2),
     BOSS_H + 1.6 + BOARD_COMP_Y),
    ("BQ24074", max(BQ_W / 2, BQ_PX / 2 + BOSS_D / 2),
     BOSS_H + 1.6 + BOARD_COMP_Y),
    ("BQ24074 DC jack", FRONT_TALL_X, BOSS_H + 1.6 + FRONT_TALL_Y),
)
_sled_front_y = SLED_PLANE_Y - SLED_T / 2      # face the boards sit on
_ledge_near_y = LEDGE_CY + LEDGE_WY / 2        # ledge edge facing them

for _nm, _ix, _iy in _FRONT_ITEMS:
    _req(LEDGE_IN_X >= _ix + 0.8
         or _sled_front_y - _iy >= _ledge_near_y + 0.8,
         f"Front-side ledges foul {_nm} during the sled's descent: it "
         f"reaches out to +/-{_ix:.2f} in X and {_iy:.2f} off the sled "
         f"face in Y, and clears the ledge in neither. Reduce LEDGE_P, "
         f"or move LEDGE_CY further onto the front wall.")

# sensor screw heads under the tube wall
_req(SEAT_GAP - SCREW_HEAD_H >= 0.6,
     "Sensor screw heads foul the mixing tube end. Increase SEAT_GAP, "
     "use countersunk M2.5, or source lower-profile hardware.")

_req(NOTCH_H > NOTCH_MARGIN,
     "NOTCH_H collapsed to its own margin -- CONNECTOR_H/SEAT_GAP "
     "changed enough that the derived notch height is degenerate. "
     "Check the CONNECTOR_H - SEAT_GAP relationship.")

# standoffs stay clear of the descending tube
_req(BOARD_BOT_DROP > TUBE_END_DROP,
     "Standoff tops rise past the tube end. Check STAND_H/SEAT_GAP.")

# STEMMA cable hole (centred at DIE_OFFSET) must clear all 4 standoffs
# (each offset +/-HOLE_PX/2, +/-HOLE_PY/2 from DIE_OFFSET, so the
# hole-to-standoff distance is translation-invariant)
_cable_to_standoff = math.hypot(HOLE_PX / 2, HOLE_PY / 2)
_req(DECK_CABLE_D / 2 + STAND_D / 2 + 0.8 <= _cable_to_standoff,
     "STEMMA cable hole fouls a standoff. Reduce DECK_CABLE_D or "
     "increase HOLE_PX/HOLE_PY.")

# ...and the lead has to get from the OPT4048's socket (on a SHORT end
# of the board) in to that hole, which means running between the two
# standoffs at that end. Added 2026-07-23 after the first full build:
# at STAND_D = 10.0 this channel was 2.7mm and the cable would not sit
# in it neatly.
STEMMA_CHANNEL_MIN = 4.5   # 4-way STEMMA QT lead, wires laid side by
                           # side rather than bundled round
_req(HOLE_PY - STAND_D >= STEMMA_CHANNEL_MIN,
     "No room to route the STEMMA lead between the standoffs on the "
     "board's short side. Reduce STAND_D (watch the insert wall: "
     "STAND_D must stay >= M25_INS_D + 4.5 to avoid the bulging that "
     "the 5.5mm version had).")

# ...without giving back the insert-bulge fix that drove STAND_D up in
# the first place
_req((STAND_D - M25_INS_D) / 2 >= 2.2,
     "Standoff wall around the M2.5 insert pilot is back below the "
     "2.25mm that stopped it bulging on insertion. Increase STAND_D.")

# JST-PH pass-through must clear the QT mount bosses and MAX bosses
_ph_to_qt = min(math.hypot(sx * QT_MOUNT_PX / 2 - PH_HOLE_X,
                          QT_CTR + sy * QT_MOUNT_PY / 2 - PH_HOLE_OFF)
                for sx in (1, -1) for sy in (1, -1))
_ph_to_max = min(math.hypot(sx * MAX_PX / 2 - PH_HOLE_X,
                            MAX_CTR + MAX_HOLE_DY - PH_HOLE_OFF)
                 for sx in (1, -1))
_req(PH_HOLE_D / 2 + BOSS_D / 2 + 0.8 <= _ph_to_qt,
     "JST-PH pass-through fouls a QT mount boss. Reduce PH_HOLE_D or "
     "move PH_HOLE_OFF/PH_HOLE_X.")
_req(PH_HOLE_D / 2 + BOSS_D / 2 + 0.8 <= _ph_to_max,
     "JST-PH pass-through fouls a MAX17048 boss. Reduce PH_HOLE_D or "
     "move PH_HOLE_OFF/PH_HOLE_X.")

# M2.5 insert pocket (shared by QT Py, BQ24074, MAX17048 bosses) must
# stay within the boss height, not reach down into the sled's thin
# base plate
_req(M25_INS_L <= BOSS_H,
     "M2.5 sled boss insert pocket reaches past the boss into the "
     "sled base plate. Increase BOSS_H or use a shorter insert.")
_req(abs(PH_HOLE_X) + PH_HOLE_D / 2 + 2.0 <= SLED_W / 2,
     "JST-PH pass-through breaks out through the sled edge. Reduce "
     "PH_HOLE_D or move PH_HOLE_X inward.")

# ...and must clear the cradle's own body -- the cradle is wide enough
# (+/-CRADLE_OUT_W/2) that its mouth-end corner can still reach the
# hole even though PH_HOLE_OFF sits above CRADLE_V0.
if abs(PH_HOLE_X) <= CRADLE_OUT_W / 2 + PH_HOLE_D / 2:
    _req(PH_HOLE_OFF + PH_HOLE_D / 2 + 2.0 <= CRADLE_V0,
         "JST-PH pass-through overlaps the battery cradle's own body "
         "at its mouth-end corner. Move PH_HOLE_OFF further above "
         "CRADLE_V0, or PH_HOLE_X outside +/-CRADLE_OUT_W/2.")

# ...and must clear the rail grooves (if it's within their Y-span at
# all -- the groove starts well above QT's row, see below)
if CRADLE_RAIL_TOP <= PH_HOLE_OFF <= CRADLE_RAIL_BOT:
    _ph_to_rail = min(abs(sx * CRADLE_RAIL_X - PH_HOLE_X) for sx in (1, -1))
    _req(PH_HOLE_D / 2 + CRADLE_RAIL_W / 2 + 0.8 <= _ph_to_rail,
         "JST-PH pass-through fouls a rail groove. Reduce PH_HOLE_D or "
         "move PH_HOLE_X/CRADLE_RAIL_X apart.")

_req(SLED_TOP_Z <= DECK_SEAT_Z - DECK_SLED_GAP + 0.01,
     "Sled top rises into the deck. Increase DECK_SLED_GAP or check "
     "the derived chain.")

# deck perimeter wall must clear the lid's interior face with real
# margin -- it's a loose drop-in part, not fixed, so it must never be
# able to touch the lid on the way past. The P_BOSS clamp-ring bosses
# also hang down from the lid, but sit at a much smaller radius (max
# 22.0mm) than the wall (25.5mm+), so they never actually overlap the
# wall regardless of Z -- the lid's own flat face is the real ceiling
_req(DECK_SEAT_Z + DECK_T + DECK_WALL_H <= H_BOX - 3.0,
     "Deck perimeter wall reaches too close to the lid. Reduce "
     "DECK_WALL_H.")
_req(DECK_W / 2 - DECK_WALL_T >= P_BOSS_BCD / 2 + P_BOSS_D / 2 + 1.0,
     "Deck perimeter wall's inner face reaches into the P_BOSS "
     "clamp-ring boss envelope. Reduce DECK_WALL_T or check P_BOSS_BCD.")
# deck wall is now a plain octagonal ring (corner chamfers, not pillar
# notches -- see the deck's own note). Ring connectivity is no longer
# at risk the way the notched version's was, but both chamfers still
# have to be genuine corner cuts: a chamfer sum at or below the
# octagon's own half-width would slice the flat edges off instead and
# leave four disconnected strips.
for _nm, _half, _sum in (
        ("deck", DECK_W / 2, CORNER_CHAMF),
        ("deck wall outer", DECK_W / 2, CORNER_CHAMF),
        ("deck wall inner", DECK_W / 2 - DECK_WALL_T,
         CORNER_CHAMF - math.sqrt(2) * DECK_WALL_T)):
    _req(_half + 1.0 < _sum < 2 * _half,
         f"{_nm} corner chamfer is degenerate: it must cut the corner "
         f"without reaching the flat edges. Check CORNER_CHAMF, "
         f"DECK_W and DECK_WALL_T.")

# battery cradle fits its zone on the sled back; the rib channels
# govern its lateral clearance now the ledges live on the front. Check
# the CRADLE's outer footprint, not just the bare battery -- the
# cradle walls make it bigger in all 3 directions.
_req(CRADLE_V0 >= 0,
     "Cradle's open end runs off the top of the sled. Reduce "
     "CRADLE_CLR_L or increase BAT_TOP_OFF.")
_req(CRADLE_V1 <= SLED_H - 5.0,
     "Cradle overruns the sled bottom. Lengthen the sled rows or "
     "reduce BAT_TOP_OFF.")
_req(CRADLE_OUT_W / 2 <= RIB_IN_X - 2.0,
     "Battery cradle too wide for the back bay: less than 2 mm to the "
     "rib channels. Reduce BAT_W, CRADLE_CLR or CRADLE_WALL.")
_req(CRADLE_RAIL_LEN > 10.0,
     "Rail collapsed to a stub or inverted. Reduce "
     "CRADLE_RAIL_END_MARGIN or lengthen the cradle.")
_req(CRADLE_RAIL_H + 1.5 <= SLED_T,
     "Rail groove too deep for the sled -- less than 1.5 mm of "
     "material would remain toward the front face. Reduce CRADLE_RAIL_H.")
_req(CRADLE_RAIL_X + CRADLE_RAIL_W / 2 + CRADLE_RAIL_CLR + 1.5
     <= CRADLE_OUT_W / 2,
     "Rail runs outside the cradle's own base. Reduce "
     "CRADLE_RAIL_X, CRADLE_RAIL_W or increase CRADLE_OUT_W.")
_req(CRADLE_RAIL_TOP >= _row0 + QT_MOUNT_L + 2.0,
     "Rail groove runs up into the QT mount row. Reduce "
     "CRADLE_RAIL_END_MARGIN.")
_req(CRADLE_SLOT_W <= CRADLE_OUT_W - 2 * CRADLE_WALL - 4.0,
     "Top-wall slot leaves no rail to tie the side walls together. "
     "Reduce CRADLE_SLOT_W or increase CRADLE_OUT_W.")
_req(CRADLE_SLOT_MARGIN < CRADLE_OUT_L,
     "Slot margin longer than the cradle itself. Reduce "
     "CRADLE_SLOT_MARGIN.")

_req(abs(GLAND_POS[0] - VENT_POS[0]) >= (GLAND_D + VENT_D) / 2 + 6.0,
     "Gland and vent bosses too close together on the bottom face.")
for _p, _d in ((GLAND_POS, GLAND_D), (VENT_POS, VENT_D)):
    _req(max(abs(_p[0]), abs(_p[1])) + _d / 2 <= EXT_W / 2 - WALL - 3.0,
         "A bottom fitting is too close to a wall for its locknut.")

# on/off switch, -Y wall. Not cut yet -- SWITCH_D is the eventual
# hand-drilled hole size, checked here so the *spot* stays valid even
# though no hole exists. The dimple footprint (X, top/bottom rim)
# mirrors the bottom-fitting locknut-clearance pattern above; the far
# side (sled_refs/cradle keepouts) is a real 3D interference question
# these symbolic checks can't cover -- verified separately when this
# spot was first chosen (2026-07-23). No interior boss (see the
# parameter comment above): Paul is handling guaranteed-solid material
# here via a slicer modifier, not CAD.
_req(1.0 <= WALL <= 13.0,
     "Switch panel-thickness spec is 1-13mm; WALL falls outside it.")
_req(abs(SWITCH_X) + SWITCH_D / 2 + 3.0 <= PIL_POS - PIL_R,
     "The eventual switch locknut would reach a corner pillar. Reduce "
     "SWITCH_D or move SWITCH_X toward the wall centre.")
_req(SWITCH_Z - SWITCH_D / 2 - 3.0 >= BOTTOM_T,
     "The eventual switch locknut would reach the bottom face. Raise "
     "SWITCH_Z.")
_req(SWITCH_Z + SWITCH_D / 2 + 3.0 <= H_BOX - RIM_BAND,
     "The eventual switch locknut would reach the thickened rim band. "
     "Lower SWITCH_Z.")
_req(SWITCH_DIMPLE_DEPTH + 1.0 <= WALL,
     "Drill-guide dimple leaves under 1mm before it would penetrate "
     "the wall. Reduce SWITCH_DIMPLE_DEPTH.")

# antenna bulkhead, +X wall
_ant_rib_y_lo = SLED_PLANE_Y - CH_GAP / 2 - RIB_W
_ant_rib_y_hi = SLED_PLANE_Y + CH_GAP / 2 + RIB_W
_req(ANT_HOLE_Y + ANT_HOLE_D / 2 + 3.0 <= _ant_rib_y_lo
     or ANT_HOLE_Y - ANT_HOLE_D / 2 - 3.0 >= _ant_rib_y_hi,
     "Antenna bulkhead hole fouls the sled rib channel/guide fence on "
     f"the +/-X wall ({_ant_rib_y_lo:.1f} to {_ant_rib_y_hi:.1f}). Move "
     "ANT_HOLE_Y further from that band.")
_req(ANT_HOLE_Z - ANT_HOLE_D / 2 - 3.0 >= BOTTOM_T,
     "Antenna bulkhead hole would reach the bottom face. Raise "
     "ANT_HOLE_Z.")
_req(ANT_HOLE_Z + ANT_HOLE_D / 2 + 3.0 <= DECK_SEAT_Z - LEDGE_H,
     "Antenna bulkhead hole would reach the deck ledge/corbel band. "
     "Lower ANT_HOLE_Z.")
# Corner-pillar clearance in Y isn't re-checked here: ANT_HOLE_Y is
# pinned to LEDGE_CY, and the ledge already sits at that Y position
# clear of the pillars (it's a proven, working feature) -- so the hole
# inherits that clearance for free as long as ANT_HOLE_Y == LEDGE_CY.

_req(RAIL_TAPER > 0,
     "Rail taper must be positive (wide end up) or the cleat logic "
     "inverts and the box will not seat.")
_req(RAIL_MARGIN >= 0,
     "RAIL_MARGIN must be >= 0 -- the printed rail can't be shorter "
     "than the bracket's own engagement depth.")
_req(RAIL_LEN <= H_BOX,
     "Rail segment is longer than the box itself. Reduce RAIL_MARGIN "
     "or BRK_H, or the rail will poke out past the box top/bottom.")

# pole bracket clamp tunnels: stay clear of the block's top/bottom faces
# and each other
for _zc in TUN_ZC:
    _req(_zc - TUN_H / 2 >= 6.0,
         f"Tunnel at z={_zc} leaves under 6mm to the bracket's bottom "
         f"face. Reduce TUN_H or raise TUN_ZC.")
    _req(_zc + TUN_H / 2 <= BRK_H - 6.0,
         f"Tunnel at z={_zc} leaves under 6mm to the bracket's top face. "
         f"Reduce TUN_H or lower TUN_ZC.")
_req(min(TUN_ZC) + TUN_H <= max(TUN_ZC),
     "The two clamp tunnels overlap or run too close together. Reduce "
     "TUN_H or space TUN_ZC further apart.")

# pole bracket stress-relief chamfers: both must be genuine corner cuts,
# not reach past the feature they're relieving
_req(BRK_CHAMF < BRK_W / 2 - VG_HALF,
     "Front corner chamfer reaches the V-groove mouth. Reduce BRK_CHAMF "
     "or VG_HALF, or widen BRK_W.")
_req(TUN_Y[1] + BRK_CHAMF <= BRK_D - VG_DEPTH - 2.0,
     "Tunnel-mouth chamfer reaches the V-groove apex. Reduce BRK_CHAMF "
     "or lower TUN_Y[1].")

# wall-mount bracket: screw holes must stay clear of the block's own
# top/bottom faces and each other, and the countersink + clearance hole
# must fit within the block's depth behind the slot channel's floor
for _zc in WMT_HOLE_ZC:
    _req(_zc - WMT_CS_D / 2 >= 6.0,
         f"Wall-mount screw hole at z={_zc} leaves under 6mm to the "
         f"bracket's bottom face. Raise the z value or lower WMT_CS_D.")
    _req(_zc + WMT_CS_D / 2 <= BRK_H - 6.0,
         f"Wall-mount screw hole at z={_zc} leaves under 6mm to the "
         f"bracket's top face. Lower the z value or reduce WMT_CS_D.")
_req(min(WMT_HOLE_ZC) + WMT_CS_D <= max(WMT_HOLE_ZC),
     "The two wall-mount screw holes overlap or run too close together. "
     "Space WMT_HOLE_ZC further apart or reduce WMT_CS_D.")
_req(WMT_CS_Y0 + WMT_CS_DEPTH < BRK_D,
     "Wall-mount countersink + depth reaches past the block's back "
     "face -- no clearance-hole length left. Reduce WMT_CS_D/WMT_CS_ANGLE "
     "or widen BRK_D.")
_req(WMT_CS_D / 2 + 1.0 <= BRK_W / 2,
     "Wall-mount countersink is wider than the block itself. Reduce "
     "WMT_CS_D or widen BRK_W.")

# lid skirt must stay well clear of the pole-mount rail lower down the
# +Y wall -- RAIL_Z0 is the rail's own bottom, and the rail is centred
# on H_BOX by construction, so by that same symmetry the gap from the
# rim down to the rail's TOP is also exactly RAIL_Z0; the skirt only
# needs to eat into a small fraction of that
_req(SKIRT_H <= RAIL_Z0 - 5.0,
     "Lid skirt reaches down far enough to risk the pole-mount rail. "
     "Reduce SKIRT_H.")

# the screws have moved out to the corners, so their heads now sit
# close to the skirt's inner face -- a driver has to get onto them
LID_SCREW_HEAD_D = 5.5      # M3 pan head across flats/dia
_req(EXT_W / 2 + SKIRT_CLR - PIL_POS - LID_SCREW_HEAD_D / 2 >= 1.0,
     "Lid screw heads foul the weather skirt now the screws sit out at "
     "the corners. Reduce PIL_POS (at the cost of SEAL_SCREW_WALL), or "
     "increase SKIRT_CLR.")

# =====================================================================
# 4. HELPERS
# =====================================================================

def _rbox(w, l, h, z0=0.0, r=0.0):
    wp = cq.Workplane("XY").workplane(offset=z0).rect(w, l).extrude(h)
    if r > 0:
        wp = wp.edges("|Z").fillet(r)
    return wp

def _cyl(d, h, z0=0.0, x=0.0, y=0.0):
    return (cq.Workplane("XY").workplane(offset=z0)
            .center(x, y).circle(d / 2).extrude(h))

def _loft_rect(z0, w0, l0, z1, w1, l1, c0=(0, 0), c1=(0, 0)):
    """Loft between two rectangles at z0 and z1 with independent
    centres, returned as a free solid."""
    wp = (cq.Workplane("XY").workplane(offset=z0)
          .center(*c0).rect(w0, l0)
          .workplane(offset=z1 - z0)
          .center(c1[0] - c0[0], c1[1] - c0[1]).rect(w1, l1)
          .loft(combine=False))
    return wp

def _chamf_prism(chamf_sum, h, z0=0.0):
    """A 45-degree-rotated square prism whose four faces are the lines
    x +/- y = +/-chamf_sum. Intersect a part with this to chamfer all
    four of its corners at once; the rotated square's own corners point
    along the axes, far outside anything here, so they never
    participate. Every corner boundary in the seal rework is expressed
    this way, which is what makes the margins between them constant
    rather than worst-case-at-45-degrees."""
    d = chamf_sum * math.sqrt(2)     # full width of the rotated square
    return (cq.Workplane("XY").workplane(offset=z0)
            .rect(d, d).extrude(h)
            .rotate((0, 0, 0), (0, 0, 1), 45))

def _chamf_loft(sum0, z0, sum1, z1):
    """The same rotated square, lofted between two chamfer sums, so its
    faces recede at a printable angle instead of standing vertical."""
    d0, d1 = sum0 * math.sqrt(2), sum1 * math.sqrt(2)
    return (_loft_rect(z0, d0, d0, z1, d1, d1)
            .rotate((0, 0, 0), (0, 0, 1), 45))

def _tri_prism(pts, z0, h):
    return (cq.Workplane("XY").workplane(offset=z0)
            .polyline(pts).close().extrude(h))

def _dovetail_prism(w0, w1, h, length, cx=0.0, y0=0.0, z0=0.0):
    """Trapezoid cross-section (width w0 at z=z0, w1 at z=z0+h -- h may
    be negative to build the taper the other way), swept along Y from
    y0 to y0+length, centred at x=cx. Degenerates to a plain
    right-angle rectangular prism when w0==w1 -- used that way for the
    battery cradle's rails (h negative, projecting out of the cradle's
    base) and the sled's matching grooves (h positive, cut into the
    sled's thickness); the name is a holdover from when this was a
    true tapered dovetail undercut, since replaced by plain rails now
    that glue provides the retention instead."""
    profile = (cq.Workplane("XZ")
               .polyline([(-w0 / 2, z0), (w0 / 2, z0),
                         (w1 / 2, z0 + h), (-w1 / 2, z0 + h)])
               .close().extrude(-length))
    return profile.translate((cx, y0, 0))

# =====================================================================
# 5. BOX
# =====================================================================

box = _rbox(EXT_W, EXT_W, H_BOX, 0, BOX_R)

# cavity: plain lower section, 45 degree taper, rim band section
z_tap0 = H_BOX - RIM_BAND - RIM_TAPER
z_tap1 = H_BOX - RIM_BAND
cav = _rbox(EXT_W - 2 * WALL, EXT_W - 2 * WALL, z_tap0 - BOTTOM_T,
            BOTTOM_T)
cav = cav.union(_loft_rect(z_tap0, EXT_W - 2 * WALL, EXT_W - 2 * WALL,
                           z_tap1, RIM_IN, RIM_IN))
cav = cav.union(_rbox(RIM_IN, RIM_IN, H_BOX - z_tap1 + 1, z_tap1))
box = box.cut(cav)

# corner pillars, welded into both walls, running flush to the true
# rim top (not stopping below the groove as an earlier revision did --
# that left an open sliver between the pillar top and the rim surface
# wherever the pillar was the sole backing for the groove's inner wall,
# i.e. at every corner, breaking the O-ring channel open into the
# insert pocket. The groove cut below correctly slices through the top
# of the pillar where the two overlap in plan view; that's a normal
# groove-through-material cut, not a gap, since the insert hole's own
# footprint stays clear of the groove (checked below).
#
# The posts now sit far enough out (PIL_POS is derived against the
# exterior, see section 1) that a free cylinder of PIL_R would break
# out through the wall and the corner radius, so each one is clipped to
# the box's own exterior profile: at this position the post IS the
# corner solid rather than a tower standing next to it.
_ext_profile = _rbox(EXT_W, EXT_W, H_BOX, 0, BOX_R)
for sx in (1, -1):
    for sy in (1, -1):
        box = box.union(
            _cyl(2 * PIL_R, PIL_TOP_Z - BOTTOM_T, BOTTOM_T,
                 sx * PIL_POS, sy * PIL_POS).intersect(_ext_profile))

# corner gussets: the seal groove dips inboard of the screws at each
# corner (see the SEAL_CHAMF chain), which takes it off the rim band
# and out over the opening. These fill each corner of the rim band back
# in so the groove's inner wall is backed by solid material the whole
# way round -- the same requirement that the 2026-07-19 pillar-height
# fix was about, at a feature that didn't exist then.
#
# Built as the rim-band opening minus a chamfer solid, in two zones:
# straight down to GUSSET_STRAIGHT (which has to clear the groove's
# whole depth -- see the note on the derived chain), then a 45 degree
# taper receding back into the corner. The box prints bottom-down, so
# the taper is what stops the gusset's underside being an unsupported
# bridge across the corner. The taper's bottom sum is deliberately past
# the opening's own corner, so the wedge runs out to nothing just above
# the bottom of the band rather than ending in a knife edge exactly on
# the boundary.
_gus_band = _rbox(RIM_IN, RIM_IN, GUSSET_H, H_BOX - GUSSET_H)
_gus_void = _chamf_prism(GUSSET_SUM, GUSSET_STRAIGHT + 0.1,
                         H_BOX - GUSSET_STRAIGHT).union(
    _chamf_loft(GUSSET_SUM + GUSSET_TAPER * math.sqrt(2),
                H_BOX - GUSSET_H, GUSSET_SUM, H_BOX - GUSSET_STRAIGHT))
box = box.union(_gus_band.cut(_gus_void))

# Lid-screw insert pockets are cut AFTER the gussets, and the order is
# load-bearing (fixed 2026-07-23, spotted in Fusion as a small notch in
# each pocket). The screws sit at the box's corner radius centre, so a
# pocket spans PIL_POS +/- M3_INS_D/2 = 27 to 31 in each axis, and its
# inboard corner pokes past the rim opening at 28 -- straight into the
# gusset band's own footprint. Cut first and unioned after, the gusset
# filled that corner of the pocket back in with a wedge of plastic
# running the pocket's full depth, which an insert would foul on going
# in. Nothing else in this file cares about the pocket's own footprint,
# so cutting last is the whole fix.
for sx in (1, -1):
    for sy in (1, -1):
        box = box.cut(_cyl(M3_INS_D, M3_INS_L + 0.1,
                           PIL_TOP_Z - M3_INS_L,
                           sx * PIL_POS, sy * PIL_POS))

# Face seal groove: an octagonal ring -- four flats at GROOVE_OFF, four
# corner chamfers at SEAL_CHAMF passing inboard of the lid screws -- with
# every vertex rounded off at GROOVE_RC so the O-ring never has to turn a
# sharp corner.
#
# Built as a sharp octagon then filleted, rather than the earlier
# "rounded square intersected with a chamfer prism". That earlier form
# left two hard kinks per corner where the square's corner arc ran into
# the chamfer plane: only about 20 degrees each, but a kink is a kink,
# and a cord seated over one is being asked to take the bend on a line
# rather than over an arc's length. Filleting the octagon's own vertices
# gives a genuinely tangent flat -> arc -> chamfer transition instead.
# GROOVE_RC keeps the same value it had as the old corner radius; the
# outer and inner rings take it +/- the half-width, which is what keeps
# the channel a constant GROOVE_W wide around the rounded corners too.
def _groove_ring(half, chamf_sum, fillet_r, h, z0):
    oct_ = _rbox(2 * half, 2 * half, h, z0).intersect(
        _chamf_prism(chamf_sum, h + 0.4, z0 - 0.2))
    return oct_.edges("|Z").fillet(fillet_r)

g_out = _groove_ring(GROOVE_OFF + GROOVE_W / 2,
                     SEAL_CHAMF + math.sqrt(2) * GROOVE_W / 2,
                     GROOVE_RC + GROOVE_W / 2,
                     GROOVE_D + 0.1, H_BOX - GROOVE_D)
g_in = _groove_ring(GROOVE_OFF - GROOVE_W / 2,
                    SEAL_CHAMF - math.sqrt(2) * GROOVE_W / 2,
                    GROOVE_RC - GROOVE_W / 2,
                    GROOVE_D + 0.3, H_BOX - GROOVE_D - 0.1)
box = box.cut(g_out.cut(g_in))

# sled rib channels on the +/-X walls
RIB_LEN_X = EXT_W / 2 - WALL + 0.2 - RIB_IN_X    # welded 0.2 in
for sx in (1, -1):
    for yc in (SLED_PLANE_Y - CH_GAP / 2 - RIB_W / 2,
               SLED_PLANE_Y + CH_GAP / 2 + RIB_W / 2):
        box = box.union(
            cq.Workplane("XY").workplane(offset=BOTTOM_T)
            .center(sx * (RIB_IN_X + RIB_LEN_X / 2), yc)
            .rect(RIB_LEN_X, RIB_W).extrude(DECK_SEAT_Z - BOTTOM_T))

# sled X-retention guide fences: CH_GAP above was open across the
# rib's ENTIRE width (RIB_IN_X to the wall), but the sled's own plate
# is what occupies the span from RIB_IN_X out to its own edge (SLED_W/2)
# -- that's not wasted space, it's exactly where the sled slides
# (_req above guarantees SLED_W/2 is always at least 2mm past RIB_IN_X,
# i.e. always inside this span). The genuinely wasted, unconstrained
# space that let the sled rattle side-to-side (first full print,
# 2026-07-20) is only OUTSIDE the sled's edge, out to the rib's outer
# limit near the wall. Fence only that outer strip solid (small
# FENCE_CLR clearance off the sled's true edge), leaving the inner
# span (RIB_IN_X to the sled's edge) fully open as before. Welds
# directly onto the existing ribs at the CH_GAP boundary, so nothing
# floats disconnected.
for sx in (1, -1):
    edge_x = sx * SLED_W / 2
    rib_out = sx * (RIB_IN_X + RIB_LEN_X)
    outer_slot_edge = edge_x + sx * FENCE_CLR
    x_lo, x_hi = min(outer_slot_edge, rib_out), max(outer_slot_edge, rib_out)
    length = x_hi - x_lo
    if length > 0.1:
        box = box.union(
            cq.Workplane("XY").workplane(offset=BOTTOM_T)
            .center((x_lo + x_hi) / 2, SLED_PLANE_Y)
            .rect(length, CH_GAP)
            .extrude(DECK_SEAT_Z - BOTTOM_T))

# deck ledges on the +/-X walls + 45 degree corbels beneath them
LEDGE_IN_X = EXT_W / 2 - LEDGE_P
for sx in (1, -1):
    box = box.union(
        cq.Workplane("XY").workplane(offset=DECK_SEAT_Z - LEDGE_H)
        .center(sx * (LEDGE_IN_X + LEDGE_P / 2), LEDGE_CY)
        .rect(LEDGE_P, LEDGE_WY).extrude(LEDGE_H))
    # corbel: lofted from a thin sliver at the wall up to the full
    # ledge footprint, giving a 45 degree printable underside.
    # No "+0.2 weld margin" on the outer (ledge-side) cross-section:
    # LEDGE_IN_X + LEDGE_P lands exactly on the true exterior face by
    # construction, so a fudge there pokes a sliver through the outside
    # of the box instead of welding into wall material (there is none
    # left to weld into). The inner (wall-side) sliver below still
    # needs its own overlap into the wall, which wall_x already gives it.
    wall_x = EXT_W / 2 - WALL
    box = box.union(_loft_rect(
        DECK_SEAT_Z - LEDGE_H - LEDGE_P,
        0.4, LEDGE_WY,
        DECK_SEAT_Z - LEDGE_H,
        LEDGE_P, LEDGE_WY,
        c0=(sx * (wall_x + 0.0), LEDGE_CY),
        c1=(sx * (LEDGE_IN_X + LEDGE_P / 2), LEDGE_CY)))
    box = box.cut(_cyl(M25_INS_D, M25_INS_L + 0.1,
                       DECK_SEAT_Z - M25_INS_L,
                       sx * DECK_SCREW_X, LEDGE_CY))

# dovetail rail on the +Y wall, lofted for the taper. Centred segment,
# not full height -- see RAIL_LEN/RAIL_Z0 above.
tip0, neck0 = _rail_halves(0)
tip1, neck1 = _rail_halves(RAIL_LEN)
y_root = EXT_W / 2 - 0.2
y_tip = EXT_W / 2 + RAIL_DEPTH
rail = (cq.Workplane("XY").workplane(offset=RAIL_Z0)
        .polyline([(-neck0, y_root), (-tip0, y_tip),
                   (tip0, y_tip), (neck0, y_root)]).close()
        .workplane(offset=RAIL_LEN)
        .polyline([(-neck1, y_root), (-tip1, y_tip),
                   (tip1, y_tip), (neck1, y_root)]).close()
        .loft(combine=False))
box = box.union(rail)

# bottom fittings
box = box.cut(_cyl(GLAND_D, BOTTOM_T + 2, -1, *GLAND_POS))
box = box.cut(_cyl(VENT_D, BOTTOM_T + 2, -1, *VENT_POS))

# external antenna bulkhead, +X wall -- cut for real (unlike the switch
# below): at ANT_HOLE_D=6.5mm this is well under the ~16mm scale where
# the switch hole's horizontal-bridging problem actually bit, so it's
# expected to print fine in ASA without support. Still worth a look in
# the slicer before committing to a full box print, same spirit as the
# gland/vent coupon.
ant_hole = cq.Workplane(obj=cq.Solid.makeCylinder(
    ANT_HOLE_D / 2, WALL + 2,
    cq.Vector(EXT_W / 2 + 1, ANT_HOLE_Y, ANT_HOLE_Z), cq.Vector(-1, 0, 0)))
box = box.cut(ant_hole)

# on/off switch, -Y wall -- NOT cut yet. A printed hole on this axis
# (horizontal, through a vertical wall) either sags on its own top half
# (plain circle) or seals badly against the switch's round gasket
# (teardrop). Solved by not printing the hole at all: the box stays
# fully sealed, and Paul hand-drills the true 16mm hole later if/when
# the switch actually goes in -- a drilled hole has no overhang to sag
# in the first place. A shallow conical dimple on the EXTERIOR face
# marks the spot -- a centre-punch mark to stop a drill bit walking,
# well short of breaking through (SWITCH_DIMPLE_DEPTH << WALL). Left
# small and shallow deliberately: it's the only feature touching the
# surface the switch's gasket will eventually seat against, and a tiny
# dimple is well within what a compressed gasket shrugs off. NO boss
# on the interior face -- see the parameter comment above, this is
# Paul's explicit call, requested twice now. He's guaranteeing solid
# material at this spot himself via a slicer modifier, not CAD.
switch_dimple = cq.Workplane(obj=cq.Solid.makeCone(
    SWITCH_DIMPLE_D / 2, 0, SWITCH_DIMPLE_DEPTH,
    cq.Vector(SWITCH_X, -EXT_W / 2, SWITCH_Z), cq.Vector(0, 1, 0)))
box = box.cut(switch_dimple)

# gland/vent test plate: same two holes, real centre-to-centre spacing
# (GLAND_POS to VENT_POS, 24mm), at the box's own BOTTOM_T thickness --
# a small print to confirm both fittings actually thread through
# before committing to a full box print
if BUILD_GLAND_COUPON:
    _gland_mid = ((GLAND_POS[0] + VENT_POS[0]) / 2,
                 (GLAND_POS[1] + VENT_POS[1]) / 2)
    gland_coupon = _rbox(50, 50, BOTTOM_T, 0, 3)
    gland_coupon = gland_coupon.cut(_cyl(
        GLAND_D, BOTTOM_T + 2, -1,
        GLAND_POS[0] - _gland_mid[0], GLAND_POS[1] - _gland_mid[1]))
    gland_coupon = gland_coupon.cut(_cyl(
        VENT_D, BOTTOM_T + 2, -1,
        VENT_POS[0] - _gland_mid[0], VENT_POS[1] - _gland_mid[1]))
else:
    gland_coupon = None

# clocking index notch on the rim top face, -Y side
box = box.cut(_tri_prism([(-2.5, -EXT_W / 2 + 0.6),
                          (2.5, -EXT_W / 2 + 0.6),
                          (0, -EXT_W / 2 + 3.6)],
                         H_BOX - 0.6, 0.8))

# =====================================================================
# 6. LID  (built interior-face-at-z0; flip in the slicer)
# =====================================================================

def _apply_port_cuts(plate, t):
    plate = plate.cut(_cyl(APERTURE_D, t - NECK_L + 0.1, -0.1))
    plate = plate.cut(_cyl(NECK_D, NECK_L + 0.2, t - NECK_L))
    plate = plate.cut(_cyl(RECESS_DIA, RECESS_D + 0.1, -0.1))
    return plate

def _apply_port_bosses(plate):
    for a in P_BOSS_ANGS:
        x = P_BOSS_BCD / 2 * math.cos(math.radians(a))
        y = P_BOSS_BCD / 2 * math.sin(math.radians(a))
        plate = plate.union(_cyl(P_BOSS_D, CLAMP_FACE_DROP,
                                 -CLAMP_FACE_DROP, x, y))
        plate = plate.cut(_cyl(M25_INS_D, M25_INS_L,
                               -CLAMP_FACE_DROP - 0.05, x, y))
    return plate

lid = _rbox(LID_W, LID_W, LID_T, 0, BOX_R)
for sx in (1, -1):
    for sy in (1, -1):
        lid = lid.cut(_cyl(LID_SCREW_D, LID_T + 2, -1,
                           sx * PIL_POS, sy * PIL_POS))
lid = _apply_port_cuts(lid, LID_T)
lid = _apply_port_bosses(lid)
# clocking notch stays anchored to the box's own true rim edge
# (EXT_W), not the lid's new, bigger outer edge (LID_W) -- the two
# still have to line up with each other and with the matching notch
# already cut into the box's rim (section 5, "clocking index notch"),
# which is likewise still referenced to EXT_W
lid = lid.cut(_tri_prism([(-2.5, -EXT_W / 2 + 0.6),
                          (2.5, -EXT_W / 2 + 0.6),
                          (0, -EXT_W / 2 + 3.6)],
                         LID_T - 0.6, 0.8))

# weather skirt (added 2026-07-21): a downward lip wrapping past the
# box's exterior wall, outside SKIRT_CLR clearance, dropping SKIRT_H
# below the seal line to shed wind-driven rain off the seal and the
# proud lid screw heads before it reaches them. Sits flush with the
# lid's own new outer edge (both at LID_W/2) so the disc-to-skirt
# transition is a single continuous wall, not a stepped profile.
# Prints in the same orientation as the rest of the lid: the model is
# built interior-face-at-z0 and flipped for printing, so this skirt
# (which hangs down in the model, below z=0) becomes a wall rising up
# from solid material once flipped -- the same class of feature as the
# box's own vertical walls, not a bridge over a void.
_skirt_outer = _rbox(LID_W, LID_W, SKIRT_H, -SKIRT_H, BOX_R)
_skirt_inner = _rbox(EXT_W + 2 * SKIRT_CLR, EXT_W + 2 * SKIRT_CLR,
                     SKIRT_H + 0.2, -SKIRT_H - 0.1, BOX_R)
lid = lid.union(_skirt_outer.cut(_skirt_inner))

# port test coupon: same seal stack on a pocket-sized plate
if BUILD_COUPON:
    coupon = _rbox(50, 50, LID_T, 0, 3)
    coupon = _apply_port_cuts(coupon, LID_T)
    coupon = _apply_port_bosses(coupon)
else:
    coupon = None

# =====================================================================
# 7. CLAMP RING  (built plate-top-at-z0, tube down; flip in slicer)
# =====================================================================

clamp = _cyl(CLAMP_OD, CLAMP_T, -CLAMP_T)
clamp = clamp.union(_cyl(TUBE_OD, TUBE_L, -CLAMP_T - TUBE_L))
clamp = clamp.cut(_cyl(TUBE_ID, CLAMP_T + TUBE_L + 0.2,
                       -CLAMP_T - TUBE_L - 0.1))
for a in P_BOSS_ANGS:
    x = P_BOSS_BCD / 2 * math.cos(math.radians(a))
    y = P_BOSS_BCD / 2 * math.sin(math.radians(a))
    clamp = clamp.cut(_cyl(CLAMP_SCREW_D, CLAMP_T + 0.2,
                           -CLAMP_T - 0.1, x, y))
    clamp = clamp.cut(_cyl(CLAMP_CB_D, CLAMP_CB_DEPTH + 0.1,
                           -CLAMP_T - 0.1, x, y))
for sx in (1, -1):
    notch = (cq.Workplane("XY")
             .workplane(offset=-CLAMP_T - TUBE_L - 0.1)
             .center(sx * (TUBE_OD / 2 - 1.6), 0)
             .rect(4.4, NOTCH_W).extrude(NOTCH_H + 0.1))
    clamp = clamp.cut(notch)

# =====================================================================
# 8. SPACER SHIM  (the squeeze tuning knob; reprint at other heights)
# =====================================================================

spacer = _cyl(SPACER_OD, SPACER_T)
spacer = spacer.cut(_cyl(SPACER_ID, SPACER_T + 0.2, -0.1))
grv_o = _cyl(SPACER_GRV_C + SPACER_GRV_W, SPACER_GRV_D + 0.1,
             SPACER_T - SPACER_GRV_D)
grv_i = _cyl(SPACER_GRV_C - SPACER_GRV_W, SPACER_GRV_D + 0.3,
             SPACER_T - SPACER_GRV_D - 0.1)
spacer = spacer.cut(grv_o.cut(grv_i))

# retention ears: one per port boss, so the spacer clips loosely in
# place during assembly instead of sliding around free in the stack
def _spacer_ear(angle_deg):
    r_in = SPACER_OD / 2 - 0.5     # overlaps into the ring for a clean weld
    r_out = P_BOSS_BCD / 2 + P_BOSS_D / 2 + EAR_REACH
    tab = (cq.Workplane("XY")
           .center((r_in + r_out) / 2, 0)
           .rect(r_out - r_in, EAR_W)
           .extrude(SPACER_T)
           .rotate((0, 0, 0), (0, 0, 1), angle_deg))
    bx = P_BOSS_BCD / 2 * math.cos(math.radians(angle_deg))
    by = P_BOSS_BCD / 2 * math.sin(math.radians(angle_deg))
    notch = _cyl(P_BOSS_D + 2 * EAR_CLR, SPACER_T + 0.2, -0.1, bx, by)
    return tab.cut(notch)

for _a in P_BOSS_ANGS:
    spacer = spacer.union(_spacer_ear(_a))

# =====================================================================
# 9. SENSOR DECK  (prints as modelled, standoffs up)
# =====================================================================

# Corner relief is a 45 degree chamfer, not the circular pillar notches
# it used to be (2026-07-23): the corner gussets that back the dipped
# seal groove reach further inboard than the corner posts do, and a
# circle centred on a post would need ~9.7mm of radius to clear one --
# far more of the deck edge than the chamfer costs.
deck = _rbox(DECK_W, DECK_W, DECK_T).intersect(
    _chamf_prism(CORNER_CHAMF, DECK_T + 2, -1))
for sx in (1, -1):
    deck = deck.cut(_cyl(DECK_HOLE_D, DECK_T + 2, -1,
                         sx * DECK_SCREW_X, LEDGE_CY))
for sx in (1, -1):
    for sy in (1, -1):
        x = sx * HOLE_PX / 2 + DIE_OFFSET[0]
        y = sy * HOLE_PY / 2 + DIE_OFFSET[1]
        deck = deck.union(_cyl(STAND_D, STAND_H, DECK_T, x, y))
        deck = deck.cut(_cyl(M25_INS_D, M25_INS_L,
                             DECK_T + STAND_H - M25_INS_L, x, y))

# STEMMA cable pass-through, centred on the dome axis (DIE_OFFSET),
# hidden under the OPT4048 board
deck = deck.cut(_cyl(DECK_CABLE_D, DECK_T + 2, -1,
                     DIE_OFFSET[0], DIE_OFFSET[1]))

# =====================================================================
# 10. DECK PERIMETER WALL  (separate printed part; drops onto the deck
#     after it's screwed down. Prints flat, either face -- a single
#     continuous octagonal ring, no overhangs.)
# =====================================================================

# History worth keeping, because this part has been round the houses:
# it started as 4 loose straight segments (which toppled over), then a
# continuous ring with wide corner chamfers, then a ring hugging each
# pillar with a circular notch matching the deck's own -- that last one
# was the shipped version, after establishing that offsetting a notch
# inward means GROWING its radius, not shrinking it.
#
# Back to chamfered corners now (2026-07-23), not as a simplification
# but because the corners changed underneath it: the seal groove dips
# inboard of the lid screws, the corner gussets that back it reach
# further inboard than the posts do, and this part has to be lowered
# past those gussets. A pillar-hugging notch no longer describes the
# obstacle. Both boundaries are the same 45 degree chamfer offset by
# DECK_WALL_T (a convex corner, so the chamfer line simply moves in by
# the wall thickness), giving a uniform-thickness octagonal ring --
# trivially one connected loop, unlike the notched version whose
# connectivity had to be argued for.
def _deck_wall_octagon(w, chamf_sum, z0, h):
    return _rbox(w, w, h, z0).intersect(
        _chamf_prism(chamf_sum, h + 2, z0 - 1))

_outer = _deck_wall_octagon(DECK_W, CORNER_CHAMF, 0.0, DECK_WALL_H)
_inner = _deck_wall_octagon(DECK_W - 2 * DECK_WALL_T,
                            CORNER_CHAMF - math.sqrt(2) * DECK_WALL_T,
                            -0.1, DECK_WALL_H + 0.2)
deck_wall = _outer.cut(_inner)

# screw-head clearance notches, centred on the same deck screw
# positions (DECK_SCREW_X, LEDGE_CY) -- only needs to clear the screw
# head itself, not provide ongoing screwdriver access, since the deck
# is already screwed down before this part goes on
for sx in (1, -1):
    deck_wall = deck_wall.cut(
        cq.Workplane("XY").workplane(offset=0)
        .center(sx * DECK_SCREW_X, LEDGE_CY)
        .rect(DECK_WALL_CUT_W, DECK_WALL_CUT_W)
        .extrude(DECK_WALL_CUT_H))

# =====================================================================
# 11. SLED  (prints as modelled, bosses up; back face plain)
#     Local frame: origin at plate centre, +Y towards the sled TOP.
# =====================================================================

def _row_y(offset_from_top):
    return SLED_H / 2 - offset_from_top

sled = _rbox(SLED_W, SLED_H, SLED_T)
sled = sled.edges("|Z").chamfer(2.5)
# finger notch, top edge centre (kept clear of the QT Py mount footprint)
sled = sled.cut(_cyl(7.0, SLED_T + 2, -1, 0, SLED_H / 2))

def _bosses(part, cx, cy, offsets, boss_d=BOSS_D, boss_h=BOSS_H,
            ins_d=M25_INS_D, ins_l=M25_INS_L, back=False):
    """back=True builds the boss protruding from the sled's back face
    (z=0, growing towards -Z) instead of the front (z=SLED_T)."""
    for dx, dy in offsets:
        x, y = cx + dx, cy + dy
        if back:
            part = part.union(_cyl(boss_d, boss_h, -boss_h, x, y))
            part = part.cut(_cyl(ins_d, ins_l, -boss_h, x, y))
        else:
            part = part.union(_cyl(boss_d, boss_h, SLED_T, x, y))
            part = part.cut(_cyl(ins_d, ins_l, SLED_T + boss_h - ins_l, x, y))
    return part

def _rect_offsets(px, py):
    return [(sx * px / 2, sy * py / 2) for sx in (1, -1) for sy in (1, -1)]

qt_c = _row_y(QT_CTR)
sled = _bosses(sled, 0, qt_c, _rect_offsets(QT_MOUNT_PX, QT_MOUNT_PY))
sled = _bosses(sled, 0, _row_y(MAX_CTR),
               [(-MAX_PX / 2, MAX_HOLE_DY), (MAX_PX / 2, MAX_HOLE_DY)])
sled = _bosses(sled, 0, _row_y(BQ_CTR), _rect_offsets(BQ_PX, BQ_PY))

# battery cradle rail grooves, back face (see CRADLE_RAIL_* above).
# Cut, not a boss, so the back face stays flat for printing. Plain
# right-angle (constant-width) groove, no taper and no separate entry
# zone: since there's no undercut any more, the rail can be pressed
# straight into the groove from outside the sled at any point along
# its length, so there's no assembly-path problem left to solve with
# an oversized entry pocket the way the old tapered version needed.
for sx in (1, -1):
    cx = sx * CRADLE_RAIL_X
    sled = sled.cut(_dovetail_prism(
        CRADLE_RAIL_W + 2 * CRADLE_RAIL_CLR,
        CRADLE_RAIL_W + 2 * CRADLE_RAIL_CLR,
        CRADLE_RAIL_H + CRADLE_RAIL_CLR, CRADLE_RAIL_LEN,
        cx=cx, y0=_row_y(CRADLE_RAIL_BOT)))

# JST-PH pass-through, back face to front face (see PH_HOLE_D/X above)
sled = sled.cut(_cyl(PH_HOLE_D, SLED_T + 2, -1, PH_HOLE_X, _row_y(PH_HOLE_OFF)))

# ---- legibility: labels -----------------------------------------
# Embossed row labels on the front face in the row gaps (QT Py's mount
# covers its own footprint, so its label sits in the gap below it,
# same as the other two), mirrored BATT engraved on the back face
# (the cradle covers this once fitted, but it's still a useful
# assembly-stage label). Cosmetic only, so a missing font degrades
# gracefully. No more engraved battery outline -- the cradle now
# defines placement physically, so a witness outline underneath it
# would just be a mismatched, hidden leftover.
BAT_CTR_Y = _row_y(BAT_TOP_OFF + BAT_L / 2)

def _txt(s, size, th):
    for f in ("DejaVu Sans", "Liberation Sans", "Arial"):
        try:
            return (cq.Workplane("XY")
                    .text(s, size, th, font=f, combine=False))
        except Exception:
            continue
    return None

try:
    # all labels engraved now, not embossed (2026-07-20): the embossed
    # front-face labels (0.4mm raised, small font) didn't print well --
    # thin isolated raised ridges at that scale have poor bed/layer
    # adhesion and can be under a nozzle-width in stroke thickness,
    # while the engraved BATT label on the back printed cleanly (it's
    # a plain subtraction from an otherwise-solid first layer, which
    # the slicer resolves reliably even at small scale). th=0.6 with a
    # 0.1mm overcut past the true surface nets ~0.5mm actual engraved
    # depth, matching the BATT label that's already proven to print.
    _l1 = _txt("QT PY", 3.6, 0.6)
    _l2 = _txt("MAX17048", 3.6, 0.6)
    _l3 = _txt("BQ24074", 3.6, 0.6)
    _l4 = _txt("BATT", 6.0, 0.6)
    if all(v is not None for v in (_l1, _l2, _l3, _l4)):
        sled = sled.cut(_l1.translate(
            (0, (_row_y(_row0 + QT_MOUNT_L) + _row_y(_row1)) / 2,
             SLED_T - 0.5)))
        sled = sled.cut(_l2.translate(
            (0, (_row_y(_row1 + MAX_L) + _row_y(_row2)) / 2,
             SLED_T - 0.5)))
        sled = sled.cut(_l3.translate(
            (0, (_row_y(_row2 + BQ_L) + _row_y(SLED_H)) / 2,
             SLED_T - 0.5)))
        # mirrored so it reads correctly looking AT the back face
        sled = sled.cut(_l4.mirror("YZ").translate(
            (0, BAT_CTR_Y, -0.1)))
    else:
        print("note: no usable font found, sled labels skipped")
except Exception as e:
    print(f"note: sled labels skipped ({e})")

# ---- reference bodies (visualisation only, NOT for print) -----------
# Boards, battery and the BQ's DC barrel jack keep-out, so occupancy
# is visible in Fusion. Excluded from the individual part STEPs.

def _ref_box(w, l, h, z0, cx, cy):
    return (cq.Workplane("XY").workplane(offset=z0)
            .center(cx, cy).rect(w, l).extrude(h))

sled_refs = _ref_box(BQ_W, BQ_L, 1.6, SLED_T + BOSS_H,
                     0, _row_y(BQ_CTR))
sled_refs = sled_refs.union(_ref_box(
    9.5, 11.9, 11.0, SLED_T + BOSS_H + 1.6,
    5.35, _row_y(BQ_CTR) - 16.17))      # DC/barrel jack keep-out,
                                        # measured off the STEP connector
                                        # solid, board rotated 90 deg so
                                        # the jack overhangs toward the
                                        # sled bottom (see BQ_W/BQ_L note)
sled_refs = sled_refs.union(_ref_box(
    QT_W, QT_L, 1.2, SLED_T + BOSS_H + 2.4, 0, qt_c))   # bare PCB,
    # under the snap mount -- the +2.4 is the mount's own lift above
    # the boss face, tied to BOSS_H so this can't go stale again if
    # the boss height changes
sled_refs = sled_refs.union(_ref_box(
    MAX_W, MAX_L, 1.6, SLED_T + BOSS_H, 0, _row_y(MAX_CTR)))
sled_refs = sled_refs.union(_ref_box(
    BAT_W, BAT_L, BAT_T, -BAT_T, 0, BAT_CTR_Y))

opt_ref = _ref_box(BOARD_L, BOARD_W, BOARD_T, DECK_T + STAND_H,
                   DIE_OFFSET[0], DIE_OFFSET[1])

# =====================================================================
# 12. BATTERY CRADLE  (separate part; rail-and-groove slides onto the
#     sled's back face -- no screws, no bosses on the sled)
#     Local frame: closed (hard-stop) end at y=0, open (slide-in)
#     mouth at y=CRADLE_OUT_L. z=0 is the mounting face against the
#     sled, growing away from the sled through the battery cavity to
#     the top wall. Encloses the battery on 4 sides (doesn't need to
#     be airtight, just needs to keep it from sliding around); open
#     at the mouth for a lengthwise slide-in, plus a wide open column
#     down the middle of the top wall for clearance for a thermistor
#     taped to the battery pack. No ties. 2 rails project from the
#     mounting face (z<0) and slide into matching grooves cut into
#     the sled, glued once seated -- see CRADLE_RAIL_* above.
#     Prints mounting face down; the rails run almost the full length
#     so first-layer contact is a long thin strip, not an isolated
#     island the way small round bosses were.
# =====================================================================

cradle = (cq.Workplane("XY")
          .center(0, CRADLE_OUT_L / 2)
          .rect(CRADLE_OUT_W, CRADLE_OUT_L)
          .extrude(CRADLE_OUT_T))
cradle = cradle.edges("|Z").fillet(1.5)

# interior cavity: stops CRADLE_WALL short of the closed end (y=0) and
# runs 2 mm past the mouth for a clean open-ended cut; floats above
# the mounting face by CRADLE_WALL and stops CRADLE_WALL below the top.
_cav_len = CRADLE_LEN + 2
cav = (cq.Workplane("XY").workplane(offset=CRADLE_WALL)
       .center(0, CRADLE_WALL + _cav_len / 2)
       .rect(CRADLE_OUT_W - 2 * CRADLE_WALL, _cav_len)
       .extrude(CRADLE_OUT_T - 2 * CRADLE_WALL))
cradle = cradle.cut(cav)

# rails, projecting from the mounting face (z=0) out toward the sled
# (z<0). Plain right-angle cross-section, matching the sled's groove.
# Same local-Y mapping as everywhere else in this part:
# local_v = CRADLE_WALL + (CRADLE_V1 - global_offset).
_rail_local_y0 = CRADLE_WALL + CRADLE_RAIL_END_MARGIN
for sx in (1, -1):
    cradle = cradle.union(_dovetail_prism(
        CRADLE_RAIL_W, CRADLE_RAIL_W, -CRADLE_RAIL_H, CRADLE_RAIL_LEN,
        cx=sx * CRADLE_RAIL_X, y0=_rail_local_y0, z0=0))

# wide open column through the top wall: clears a thermistor taped to
# the battery (the tight top clearance elsewhere doesn't allow for
# it), and doubles as finger/tool access to help push the cradle home.
# Runs from CRADLE_SLOT_MARGIN short of the closed end out through the
# (already-open) mouth.
_slot_len = CRADLE_OUT_L + 2 - CRADLE_SLOT_MARGIN
slot = (cq.Workplane("XY").workplane(offset=CRADLE_OUT_T - CRADLE_WALL - 0.1)
        .center(0, CRADLE_SLOT_MARGIN + _slot_len / 2)
        .rect(CRADLE_SLOT_W, _slot_len)
        .extrude(CRADLE_WALL + 0.3))
cradle = cradle.cut(slot)

# =====================================================================
# 13. SLED FIT WEDGE  (retrofit shim, hand-fitted -- see the note at
#     SLED_W above. Not a precision assembly part: print, test-fit,
#     sand/trim to taste, secure with a dab of glue once seated.
#     Prints flat, either face.)
# =====================================================================

WEDGE_GAP = (EXT_W / 2 - WALL) - SLED_W / 2   # current sled-to-wall
                                              # play, per side (3.0mm
                                              # as printed -- this is
                                              # what rattles)
WEDGE_T0 = 1.0                # thin end, easy to start by hand
WEDGE_T1 = WEDGE_GAP - 0.2    # thick end, kept a hair under the gap
                              # so it's guaranteed to go in; taper
                              # lets you choose how far to drive it
                              # for a snug fit rather than binding
WEDGE_W = 6.0                 # width (Y) -- bigger than SLED_T so
                              # it's easy to handle and print
WEDGE_L = 25.0                # length (Z) -- a "small" wedge per
                              # side, not a full-height rail; print 2
                              # and place wherever the rattle is worst

wedge = (cq.Workplane("XZ")
         .polyline([(0, 0), (WEDGE_T0, 0),
                    (WEDGE_T1, WEDGE_L), (0, WEDGE_L)])
         .close().extrude(-WEDGE_W))

# =====================================================================
# 14. POLE BRACKET
#     Local frame: front (box-mating) face at y=0, body towards +Y,
#     z up. Prints standing on its bottom face.
# =====================================================================

bracket = (cq.Workplane("XY")
           .center(0, BRK_D / 2).rect(BRK_W, BRK_D).extrude(BRK_H))

# female receiver: lofted to match the rail taper over the engagement
tipA, neckA = _rail_halves(0)
tipB, neckB = _rail_halves(RAIL_ENGAGE)
slot = (cq.Workplane("XY").workplane(offset=BRK_FLOOR)
        .polyline([(-neckA - BRK_CLR_SIDE_BOT, -0.5),
                   (-tipA - BRK_CLR_SIDE_BOT,
                    RAIL_DEPTH + BRK_CLR_DEPTH_BOT),
                   (tipA + BRK_CLR_SIDE_BOT,
                    RAIL_DEPTH + BRK_CLR_DEPTH_BOT),
                   (neckA + BRK_CLR_SIDE_BOT, -0.5)]).close()
        .workplane(offset=BRK_H - BRK_FLOOR + 0.5)
        .polyline([(-neckB - BRK_CLR_SIDE_TOP, -0.5),
                   (-tipB - BRK_CLR_SIDE_TOP,
                    RAIL_DEPTH + BRK_CLR_DEPTH_TOP),
                   (tipB + BRK_CLR_SIDE_TOP,
                    RAIL_DEPTH + BRK_CLR_DEPTH_TOP),
                   (neckB + BRK_CLR_SIDE_TOP, -0.5)]).close()
        .loft(combine=False))
bracket = bracket.cut(slot)

# 120 degree pole V-groove on the back face, full height
vg = _tri_prism([(-VG_HALF, BRK_D + 0.5), (0, BRK_D - VG_DEPTH),
                 (VG_HALF, BRK_D + 0.5)], -1, BRK_H + 2)
bracket = bracket.cut(vg)

# hose clamp tunnels
for zc in TUN_ZC:
    bracket = bracket.cut(
        cq.Workplane("XY").workplane(offset=zc - TUN_H / 2)
        .center(0, (TUN_Y[0] + TUN_Y[1]) / 2)
        .rect(BRK_W + 2, TUN_Y[1] - TUN_Y[0]).extrude(TUN_H))

# stress-relief chamfers: the clamp band bends sharply round two edges
# on its way from the buried tunnel to the pole, and a sharp printed
# edge there would cut into the band under tension. Front corner (side
# face meets the V-groove/back face), both sides, full block height:
for sx in (1, -1):
    bracket = bracket.cut(
        _tri_prism([(sx * BRK_W / 2, BRK_D),
                    (sx * (BRK_W / 2 - BRK_CHAMF), BRK_D),
                    (sx * BRK_W / 2, BRK_D - BRK_CHAMF)], -1, BRK_H + 2))

# Tunnel mouths: the edge where each tunnel's own front wall (nearest
# the V-groove, TUN_Y[1]) meets the side face -- the tightest bend, all
# 4 mouths (2 tunnels x 2 sides), each over its own tunnel's full TUN_H.
# The chamfer's Y-leg must go to TUN_Y[1] + BRK_CHAMF (up into the SOLID
# side-face material above the tunnel), not TUN_Y[1] - BRK_CHAMF (that
# was a bug: it cut into the tunnel's own pre-existing hollow, a no-op
# that removed nothing -- caught 2026-07-24 because the corresponding
# point-probe was itself inside that same hollow, so it read "hollow"
# whether or not the chamfer cut anything real. Fixed by probing the
# solid side of the y=17 boundary instead.)
for zc in TUN_ZC:
    for sx in (1, -1):
        bracket = bracket.cut(
            _tri_prism([(sx * BRK_W / 2, TUN_Y[1]),
                        (sx * (BRK_W / 2 - BRK_CHAMF), TUN_Y[1]),
                        (sx * BRK_W / 2, TUN_Y[1] + BRK_CHAMF)],
                       zc - TUN_H / 2, TUN_H))

# No separate lock: the dovetail taper is self-seating and, printed to
# spec, holds on friction alone -- confirmed by Paul on a good print.
# The thumbscrew catch this bracket used to have was removed 2026-07-24
# after two failed redesigns chasing head clearance against the box's
# own wall (see CLAUDE.md); simplest fix was dropping it entirely.

# =====================================================================
# 14b. WALL-MOUNT BRACKET
#      Alternative to the pole bracket, not a replacement -- screws to
#      a flat surface instead of clamping a pole. Same local frame and
#      same box-mating dovetail receiver as the pole bracket (built
#      from the same block size and the same `slot` cut).
# =====================================================================

wall_bracket = (cq.Workplane("XY")
                .center(0, BRK_D / 2).rect(BRK_W, BRK_D).extrude(BRK_H))
wall_bracket = wall_bracket.cut(slot)

# Two countersunk screw holes, centred in X (inside the dovetail
# channel's own footprint, not beside it -- the channel is ~23mm wide
# at most, well clear of a 9mm countersink), one near the block's
# bottom and one near its top. Each is a countersink cut (wide end
# open into the channel, narrowing back into the material) followed by
# a clearance shank hole running the rest of the way through to the
# back (wall-facing) face.
for _zc in WMT_HOLE_ZC:
    wall_bracket = wall_bracket.cut(
        cq.Workplane(obj=cq.Solid.makeCone(
            WMT_CS_D / 2, WMT_HOLE_D / 2, WMT_CS_DEPTH,
            pnt=cq.Vector(0, WMT_CS_Y0, _zc), dir=cq.Vector(0, 1, 0))))
    wall_bracket = wall_bracket.cut(
        cq.Workplane(obj=cq.Solid.makeCylinder(
            WMT_HOLE_D / 2, BRK_D + 1.0 - (WMT_CS_Y0 + WMT_CS_DEPTH),
            pnt=cq.Vector(0, WMT_CS_Y0 + WMT_CS_DEPTH, _zc),
            dir=cq.Vector(0, 1, 0))))

# No separate lock here either -- same friction-fit dovetail engagement
# as the pole bracket, retained by the same taper.

# =====================================================================
# 15. REFERENCE DOME  (assembly visualisation only, not for print)
# =====================================================================

dome_ref = _cyl(FLANGE_OD, FLANGE_T)
dome_ref = dome_ref.union(
    cq.Workplane("XY").workplane(offset=FLANGE_T)
    .circle(DOME_OD / 2).extrude(DOME_H - FLANGE_T - DOME_OD / 2))
dome_ref = dome_ref.union(
    cq.Workplane("XY").transformed(
        offset=(0, 0, DOME_H - DOME_OD / 2)).sphere(DOME_OD / 2))
dome_ref = dome_ref.cut(_rbox(40, 40, 20, -20))   # keep upper half

# =====================================================================
# 16. ASSEMBLY + EXPORT
# =====================================================================

lid_asm = lid.translate((0, 0, H_BOX))
clamp_asm = clamp.translate((0, 0, H_BOX - CLAMP_FACE_DROP))
spacer_asm = spacer.translate((0, 0, H_BOX - CLAMP_FACE_DROP))
deck_asm = deck.translate((0, 0, DECK_SEAT_Z))
deck_wall_asm = deck_wall.translate((0, 0, DECK_SEAT_Z + DECK_T))
sled_asm = (sled.rotate((0, 0, 0), (1, 0, 0), 90)
            .translate((0, SLED_PLANE_Y + SLED_T / 2,
                        SLED_TOP_Z - SLED_H / 2)))
sled_refs_asm = (sled_refs.rotate((0, 0, 0), (1, 0, 0), 90)
                 .translate((0, SLED_PLANE_Y + SLED_T / 2,
                             SLED_TOP_Z - SLED_H / 2)))
opt_ref_asm = opt_ref.translate((0, 0, DECK_SEAT_Z))
# cradle: mounting face (local w=0) flush against the sled's back face
# (same world Y as the sled's own local Z=0), closed end (local v=
# CRADLE_WALL, the hard stop) at world Z = SLED_TOP_Z - CRADLE_V1. The
# 180 deg pre-flip about the local v-axis only mirrors the (symmetric)
# width, so it's a no-op cosmetically -- it's there so the following
# 90 deg rotation (matching the sled's own) sends the depth axis
# outward (+Y, away from the sled) instead of inward.
cradle_asm = (cradle.rotate((0, 0, 0), (0, 1, 0), 180)
              .rotate((0, 0, 0), (1, 0, 0), 90)
              .translate((0, SLED_PLANE_Y + SLED_T / 2,
                          SLED_TOP_Z - CRADLE_V1 - CRADLE_WALL)))
bracket_asm = bracket.translate((0, EXT_W / 2, RAIL_Z0 - BRK_FLOOR))
dome_asm = dome_ref.translate((0, 0, H_BOX - (FLANGE_T - RECESS_D)))

if EXPORT:
    COMPONENTS_DIR = os.path.join(OUT_DIR, "components")
    ASSEMBLY_DIR = os.path.join(OUT_DIR, "assembly")
    os.makedirs(COMPONENTS_DIR, exist_ok=True)
    os.makedirs(ASSEMBLY_DIR, exist_ok=True)
    parts = {
        "box": box, "lid": lid, "clamp_ring": clamp, "spacer": spacer,
        "sensor_deck": deck, "deck_wall": deck_wall, "sled": sled,
        "pole_bracket": bracket, "wall_mount_bracket": wall_bracket,
        "battery_cradle": cradle, "sled_fit_wedge": wedge,
    }
    if BUILD_COUPON:
        parts["port_test_coupon"] = coupon
    if BUILD_GLAND_COUPON:
        parts["gland_vent_test_plate"] = gland_coupon
    for name, part in parts.items():
        cq.exporters.export(part, os.path.join(COMPONENTS_DIR, name + ".step"))
    assembly = cq.Assembly()
    assembly.add(box, name="box", color=cq.Color(0.9, 0.9, 0.88))
    assembly.add(lid_asm, name="lid", color=cq.Color(0.85, 0.85, 0.82))
    assembly.add(clamp_asm, name="clamp", color=cq.Color(0.3, 0.3, 0.3))
    assembly.add(spacer_asm, name="spacer",
                 color=cq.Color(0.6, 0.6, 0.6))
    assembly.add(deck_asm, name="deck", color=cq.Color(0.2, 0.2, 0.2))
    assembly.add(deck_wall_asm, name="deck_wall",
                 color=cq.Color(0.15, 0.15, 0.15))
    assembly.add(sled_asm, name="sled", color=cq.Color(0.5, 0.6, 0.7))
    assembly.add(cradle_asm, name="battery_cradle",
                 color=cq.Color(0.25, 0.25, 0.28))
    assembly.add(bracket_asm, name="bracket",
                 color=cq.Color(0.7, 0.5, 0.3))
    assembly.add(dome_asm, name="dome",
                 color=cq.Color(1.0, 1.0, 1.0))
    assembly.add(sled_refs_asm, name="refs_boards_battery",
                 color=cq.Color(0.2, 0.7, 0.3, 0.45))
    assembly.add(opt_ref_asm, name="ref_opt4048",
                 color=cq.Color(0.2, 0.7, 0.3, 0.45))
    assembly.save(os.path.join(ASSEMBLY_DIR, "column_assembly.step"))

if "show_object" in globals():
    show_object(box, name="box")
    show_object(lid_asm, name="lid")
    show_object(clamp_asm, name="clamp")
    show_object(deck_asm, name="deck")
    show_object(sled_asm, name="sled")
    show_object(cradle_asm, name="battery_cradle")
    show_object(bracket_asm, name="bracket")

print("column enclosure: all assertions passed")
print(f"  exterior          {EXT_W:.1f} x {EXT_W:.1f} x {H_BOX:.2f}"
      f"  (+{LID_T:.0f} lid, dome proud above)")
print(f"  interior depth    {INT_D:.2f}")
print(f"  rim opening       {RIM_IN:.1f}, port envelope R "
      f"{PORT_ENV_R:.1f}")
print(f"  deck seat z       {DECK_SEAT_Z:.2f}   sled top z "
      f"{SLED_TOP_Z:.2f}")
print(f"  sled              {SLED_W:.1f} x {SLED_H:.1f} x {SLED_T:.1f}")
print(f"  drops below lid   boss face {CLAMP_FACE_DROP:.2f}, "
      f"tube end {TUBE_END_DROP:.2f}, board top {BOARD_TOP_DROP:.2f}, "
      f"deck top {DECK_TOP_DROP:.2f}")
print(f"  rail                {RAIL_TIP_TOP:.1f} top -> "
      f"{RAIL_TIP_TOP - RAIL_TAPER_SEG:.1f} bottom over {RAIL_LEN:.1f}, "
      f"z {RAIL_Z0:.1f} to {RAIL_Z0 + RAIL_LEN:.1f} (box centre "
      f"{H_BOX / 2:.1f})")
