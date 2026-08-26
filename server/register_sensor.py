#!/usr/bin/env python3
"""Register or update a CCT sensor's install location, then backfill solar fields.

Location is entered manually here, at install time. There is no GPS on the
hardware and the MQTT payload carries no position, so this script is the source
of truth for where each unit sits. After upserting the metadata it runs the
idempotent backfill, so any readings that arrived before registration get their
location and solar elevation filled in straight away.

Usage:
    python3 register_sensor.py \\
        --sensor-id qtpy-01 \\
        --label "Home roof, London" \\
        --latitude 51.5074 --longitude -0.1278 \\
        --timezone Europe/London \\
        [--altitude-m 35] \\
        [--exposure "open sky"]

Run with no arguments for the full option list. The IANA timezone is required
because the headline comparison is at matched local clock time, which needs the
zone (with daylight saving) and not just the longitude.
"""

import argparse
import sqlite3
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from main import DB_PATH, backfill_solar, init_db, register_sensor


def main():
    parser = argparse.ArgumentParser(
        description="Register or update a CCT sensor's install location.",
    )
    parser.add_argument("--sensor-id", required=True,
                        help="Sensor ID exactly as published over MQTT, e.g. qtpy-01")
    parser.add_argument("--label", required=True,
                        help="Human-readable name, e.g. 'Home roof, London'")
    parser.add_argument("--latitude", type=float, required=True,
                        help="Decimal degrees, north positive")
    parser.add_argument("--longitude", type=float, required=True,
                        help="Decimal degrees, east positive")
    parser.add_argument("--timezone", required=True,
                        help="IANA timezone, e.g. Europe/London or America/Los_Angeles")
    parser.add_argument("--altitude-m", type=float, default=None,
                        help="Optional, metres above sea level")
    parser.add_argument("--exposure", default=None,
                        help="Optional, e.g. 'open sky' or 'partial occlusion to east'")
    args = parser.parse_args()

    # Fail early on a bad zone rather than storing something astimezone cannot use.
    try:
        ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        print(f"Unknown IANA timezone: {args.timezone!r}", file=sys.stderr)
        sys.exit(1)

    init_db()  # make sure the sensors table and reading columns exist
    conn = sqlite3.connect(DB_PATH)
    try:
        register_sensor(
            conn,
            sensor_id=args.sensor_id,
            label=args.label,
            latitude=args.latitude,
            longitude=args.longitude,
            timezone_name=args.timezone,
            altitude_m=args.altitude_m,
            exposure=args.exposure,
        )
        print(f"Registered sensor {args.sensor_id!r} at "
              f"({args.latitude}, {args.longitude}), {args.timezone}.")

        filled = backfill_solar(conn)
        print(f"Backfill complete: {filled} earlier reading(s) updated.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
