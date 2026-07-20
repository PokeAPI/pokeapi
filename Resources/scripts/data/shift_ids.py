#!/usr/bin/env python3

# Written by @jemarq04 (37006684)
# Run shift_ids.py --help for a description of its arguments
#  Helpful script to deal with any merge conflicts for certain endpoints.
#  Currently includes endpoints relevant to encounter PRs

import os
import csv
import argparse

CSVDIR = os.path.join(os.path.dirname(__file__), "../../../data/v2/csv")


def write_shifted_entries(filename: str, key: str, args):
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Read CSV
    entries = []
    with open(os.path.join(CSVDIR, filename)) as infile:
        reader = csv.DictReader(infile)
        entries = [row for row in reader]

    # Shift IDs
    result = []
    for entry in entries:
        if int(entry[key]) >= args.start_id:
            entry[key] = str(int(entry[key]) + args.shift)
        result.append(entry)

    # Write CSV
    with open(os.path.join(CSVDIR, filename), "w") as outfile:
        writer = None
        for vals in result:
            if writer is None:
                writer = csv.DictWriter(outfile, vals.keys(), dialect="unix", quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()
            writer.writerow(vals)


def shift_encs(args):
    write_shifted_entries("encounters", "id", args)
    write_shifted_entries("encounter_condition_value_map", "encounter_id", args)


def shift_slots(args):
    write_shifted_entries("encounter_slots", "id", args)
    write_shifted_entries("encounters", "encounter_slot_id", args)


def shift_conds(args):
    write_shifted_entries("encounter_conditions", "id", args)
    write_shifted_entries("encounter_condition_prose", "encounter_condition_id", args)
    write_shifted_entries("encounter_condition_values", "encounter_condition_id", args)


def shift_cond_vals(args):
    write_shifted_entries("encounter_condition_values", "id", args)
    write_shifted_entries("encounter_condition_value_prose", "encounter_condition_value_id", args)
    write_shifted_entries("encounter_condition_value_map", "encounter_condition_value_id", args)


def shift_locs(args):
    write_shifted_entries("locations", "id", args)
    write_shifted_entries("location_names", "location_id", args)
    write_shifted_entries("location_areas", "location_id", args)
    write_shifted_entries("location_game_indices", "location_id", args)
    write_shifted_entries("pokemon_evolution", "location_id", args)


def shift_areas(args):
    write_shifted_entries("location_areas", "id", args)
    write_shifted_entries("location_area_prose", "location_area_id", args)
    write_shifted_entries("encounters", "location_area_id", args)
    write_shifted_entries("location_area_encounter_rates", "location_area_id", args)


ENDPOINT_FUNC_MAP = {
    "encounters": shift_encs,
    "encounter_slots": shift_slots,
    "encounter_conditions": shift_conds,
    "encounter_condition_values": shift_cond_vals,
    "locations": shift_locs,
    "location_areas": shift_areas,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint", choices=ENDPOINT_FUNC_MAP.keys())
    parser.add_argument("start_id", type=int, help="first ID to shift")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--shift", type=int, help="amount to shift IDs")
    group.add_argument("-S", "--end-id", type=int, help="target ID after shift")
    args = parser.parse_args()

    if args.end_id:
        args.shift = args.end_id - args.start_id

    if args.start_id <= 0:
        parser.error(f"invalid starting ID {args.start_id}")
    if args.shift <= 0:
        parser.error(f"invalid shift {args.shift}")
    if not os.path.isdir(CSVDIR):
        parser.error(f"invalid directory {CSVDIR}")

    (ENDPOINT_FUNC_MAP[args.endpoint])(args)


if __name__ == "__main__":
    main()
