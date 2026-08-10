#!/usr/bin/env python3

# Written by @jemarq04 (37006684)
# Run shift_ids.py --help for a description of its arguments
#  Helpful script to deal with any merge conflicts for certain endpoints.
#  Currently includes endpoints relevant to encounter PRs

import argparse
import csv
import os

CSVDIR = os.path.join(os.path.dirname(__file__), "../data/v2/csv")


def write_shifted_entries(filename: str, args, *keys):
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
        for key in keys:
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
    write_shifted_entries("encounters", args, "id")
    write_shifted_entries("encounter_condition_value_map", args, "encounter_id")


def shift_methods(args):
    write_shifted_entries("encounter_methods", args, "id", "order")
    write_shifted_entries("encounter_method_prose", args, "encounter_method_id")
    write_shifted_entries("encounter_slots", args, "encounter_method_id")
    write_shifted_entries("location_area_encounter_rates", args, "encounter_method_id")


def shift_slots(args):
    write_shifted_entries("encounter_slots", args, "id")
    write_shifted_entries("encounters", args, "encounter_slot_id")


def shift_conds(args):
    write_shifted_entries("encounter_conditions", args, "id")
    write_shifted_entries("encounter_condition_prose", args, "encounter_condition_id")
    write_shifted_entries("encounter_condition_values", args, "encounter_condition_id")


def shift_cond_vals(args):
    write_shifted_entries("encounter_condition_values", args, "id")
    write_shifted_entries("encounter_condition_value_prose", args, "encounter_condition_value_id")
    write_shifted_entries("encounter_condition_value_map", args, "encounter_condition_value_id")


def shift_locs(args):
    write_shifted_entries("locations", args, "id")
    write_shifted_entries("location_names", args, "location_id")
    write_shifted_entries("location_areas", args, "location_id")
    write_shifted_entries("location_game_indices", args, "location_id")
    write_shifted_entries("pokemon_evolution", args, "location_id")


def shift_areas(args):
    write_shifted_entries("location_areas", args, "id")
    write_shifted_entries("location_area_prose", args, "location_area_id")
    write_shifted_entries("encounters", args, "location_area_id")
    write_shifted_entries("location_area_encounter_rates", args, "location_area_id")


ENDPOINT_FUNC_MAP = {
    "encounters": shift_encs,
    "encounter_methods": shift_methods,
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
