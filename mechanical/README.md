# Enclosure

STEP exports of the IP65 sensor enclosure, in millimetres. These are the
published geometry: the parts are generated from a parametric CadQuery model,
and what is exported here is what gets printed.

This is the current revision, built around the LIT Systems dome diffuser — the
UV-stable, brightener-free optic that replaced the earlier fluorescing dome. It
supersedes the flanged-dome enclosure the first prototypes used.

    assembly/
      column_assembly.step    The whole unit as it goes together, including
                              reference bodies for the dome, filter, foam ring,
                              boards and battery — for context and fit-checking,
                              not for printing.

    components/
      box.step                Open-top cup, 66 mm square, 171 mm deep. PG7
                              gland and breather vent in the bottom face;
                              moulded ledges carry the sensor deck, guide
                              fences locate the sled.
      lid.step                Screw-down lid, and the optical head. The dome
                              presses into a 20.5 mm port bore from outside and
                              beds in neutral-cure silicone; a rotation lock
                              catches one of the dome's barrel slots. Everything
                              optical stays with the lid when it lifts off.
      sensor_deck.step        Sits on the box's wall ledges and carries a riser
                              that lifts the OPT4048 up to meet the dome, die up
                              on the dome axis. Riser height is the tuning knob
                              for foam compression — reprint the deck alone to
                              adjust it.
      sled.step               Carries the QT Py, fuel gauge and charge
                              controller, and slides out of the box as one
                              piece.
      battery_cradle.step     Holds the 2000 mAh LiPo against the sled.
      pole_bracket.step       Friction clamp for a pole, dovetailed to the box.
      wall_mount_bracket.step Screws to a flat surface, same dovetail.

## Orientation

TOP is the end carrying the dome port and the screw-down lid; deployed, it faces
the sky. BOTTOM carries the gland and vent and points down, so water drains away
from both.

## Printing

Printed in ASA for UV stability, lid exterior-face down. No white plastic
anywhere in the light path: white ASA yellows over time, which would quietly
drift a calibration fit out from under you.
