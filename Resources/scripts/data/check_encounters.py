#!/usr/bin/env python3

# Written by @jemarq04 (37006684)
# Run check_encounters.py --help for a description of its arguments

import argparse
import csv
import json
import os
from typing import Iterable, Optional

CSVDIR = os.path.join(os.path.dirname(__file__), "../../../data/v2/csv")


def read_csv(
    filename: str,
    before: Optional[int] = None,
    after: Optional[int] = None,
    non_unique: bool = False,
    csvdir: str = CSVDIR,
) -> dict:
    if not filename.endswith(".csv"):
        filename += ".csv"

    result = {}
    index = 0
    with open(os.path.join(csvdir, filename)) as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            row_id = list(row.values())[0]
            if before is not None and int(row_id) > before:
                break
            if after is not None and int(row_id) < after:
                continue
            if non_unique:
                result[index] = dict(row)
                index += 1
            else:
                result[row_id] = dict(row)

    return result


def get_entry_by_identifier(entries: Iterable, identifier: str) -> Optional[dict]:
    for entry in entries:
        if "identifier" in entry and entry["identifier"] == identifier:
            return entry
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--locations",
        type=lambda x: x.split(","),
        default=[],
        help="comma-separated list of locations to check for encounters",
    )
    parser.add_argument(
        "-e",
        "--first-encounter",
        type=int,
        default=1,
        help="first encounter ID to load",
    )
    parser.add_argument("-s", "--slot", action="store_true", help="store information from encounter_slots.csv")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="write files to directory even if it exists",
    )
    parser.add_argument("-S", "--summary", action="store_true", help="just provide percentages for each pokemon")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--weather", action="store_true", help="split information by weather")
    group.add_argument(
        "-x", "--max-raid", action="store_true", help="split information by max raid rarity and difficulty"
    )
    parser.add_argument("--with-id", action="store_true", help="provide encounter ID")
    parser.add_argument("--sort-by-natdex", action="store_true", help="sort by national dex number")
    parser.add_argument("-o", "--outdir", default="json", help="output directory")
    args = parser.parse_args()

    # Error checking
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
    elif not args.force:
        parser.error(f"output directory already exists: {args.outdir}")
    if args.first_encounter is None:
        print("WARNING: argument -e/--first-encounter not provided. a LOT of files will be written!")

    # Read encounter CSV files
    encounters = read_csv("encounters", after=args.first_encounter)
    encounter_condition_value_map = read_csv(
        "encounter_condition_value_map", after=args.first_encounter, non_unique=True
    )

    # Gather CSV information for other sources
    sources = {
        "encounter_slot": read_csv("encounter_slots.csv"),
        "encounter_method": read_csv("encounter_methods.csv"),
        "encounter_condition_value": read_csv("encounter_condition_values.csv"),
        "location": read_csv("locations.csv"),
        "location_area": read_csv("location_areas.csv"),
        "version": read_csv("versions.csv"),
        "version_group": read_csv("version_groups.csv"),
        "pokemon": read_csv("pokemon.csv"),
        "pokemon_species": read_csv("pokemon_species.csv"),
    }
    weather_conditions = [
        val["identifier"]
        for val in sources["encounter_condition_value"].values()
        if val["identifier"].startswith("weather-")
    ]

    def expand_source(info: dict, maxdepth: int = 1):
        if maxdepth <= 0:
            return

        for key in info:
            if key.endswith("_id"):
                src = key.replace("_id", "")
                if src not in sources:
                    continue
                info[key] = dict(sources[src][info[key]])
                expand_source(info[key], maxdepth - 1)

    # Recursively link information from the defined sources
    for enc_id, enc in encounters.items():
        expand_source(enc, 3)

    # Link encounter conditions to relevant encounters
    for entry in encounter_condition_value_map.values():
        enc_id = entry["encounter_id"]
        cond_id = entry["encounter_condition_value_id"]
        if enc_id in encounters:
            if "encounter_conditions" in encounters[enc_id]:
                encounters[enc_id]["encounter_conditions"].append(sources["encounter_condition_value"][cond_id])
            else:
                encounters[enc_id]["encounter_conditions"] = [sources["encounter_condition_value"][cond_id]]

    # Group encounters by location area
    location_area_encounters = {}
    for enc in encounters.values():
        location_identifier = enc["location_area_id"]["location_id"]["identifier"]
        if args.locations and not any(loc == location_identifier for loc in args.locations):
            continue

        location_area_identifier = location_identifier
        if enc["location_area_id"]["identifier"]:
            location_area_identifier += f"-{enc['location_area_id']['identifier']}"

        if location_area_identifier not in location_area_encounters:
            location_area_encounters[location_area_identifier] = [enc]
        else:
            location_area_encounters[location_area_identifier].append(enc)

    # Split by weather/max raid
    weather_location_area_encounters = {"weather-none": {}} | {weather: {} for weather in weather_conditions}
    max_raid_location_area_encounters = {"none": {}} | {
        f"{rarity}-{num}-stars": {} for rarity in ["common", "rare", "special"] for num in range(1, 6)
    }

    if args.weather:
        for location_area, encounters in location_area_encounters.items():
            weather_location_area_encounters["weather-none"][location_area] = [
                enc
                for enc in encounters
                if "encounter_conditions" not in enc
                or not any(cond["identifier"].startswith("weather-") for cond in enc["encounter_conditions"])
            ]
            for weather in weather_conditions:
                weather_location_area_encounters[weather][location_area] = [
                    enc
                    for enc in encounters
                    if "encounter_conditions" in enc
                    and any(cond["identifier"] == weather for cond in enc["encounter_conditions"])
                ]
    elif args.max_raid:
        for location_area, encounters in location_area_encounters.items():
            max_raid_location_area_encounters["none"][location_area] = [
                enc
                for enc in encounters
                if "encounter_conditions" not in enc
                or not any(cond["identifier"].startswith("max-den-") for cond in enc["encounter_conditions"])
            ]
            for rarity in ["common", "rare", "special"]:
                for num in range(1, 6):
                    max_raid_location_area_encounters[f"{rarity}-{num}-stars"][location_area] = [
                        enc
                        for enc in encounters
                        if "encounter_conditions" in enc
                        and all(
                            condname in [x["identifier"] for x in enc["encounter_conditions"]]
                            for condname in [f"max-den-rarity-{rarity}", f"max-den-rating-{num}-star"]
                        )
                    ]

    # Restructure encounter information for output
    def restructure_encounters(encounters: list, write_if_empty: bool = True) -> dict:
        output = {"encounters": []}
        for enc in encounters:
            output["encounters"].append(
                {
                    "pokemon": enc["pokemon_id"]["identifier"],
                    "encounter_method": enc["encounter_slot_id"]["encounter_method_id"]["identifier"],
                    "version": enc["version_id"]["identifier"],
                    "min_level": enc["min_level"],
                    "max_level": enc["max_level"],
                }
            )

            # Add optional encounter ID
            if args.with_id:
                output["encounters"][-1]["id"] = enc["id"]

            # Add optional slot information
            if args.slot:
                slot_entry = {
                    "version_group": enc["encounter_slot_id"]["version_group_id"]["identifier"],
                    "encounter_method": enc["encounter_slot_id"]["encounter_method_id"]["identifier"],
                    "slot": enc["encounter_slot_id"]["slot"],
                    "rarity": enc["encounter_slot_id"]["rarity"],
                }
                output["encounters"][-1]["encounter_slot"] = slot_entry

            # Add encounter conditions, if they exist
            if "encounter_conditions" in enc:
                output["encounters"][-1]["encounter_conditions"] = [
                    cond["identifier"] for cond in enc["encounter_conditions"]
                ]
        if args.sort_by_natdex:
            output["encounters"] = list(
                sorted(
                    output["encounters"],
                    key=lambda item: int(
                        get_entry_by_identifier(sources["pokemon"].values(), item["pokemon"])["species_id"]
                    ),
                )
            )
            for encounter in output["encounters"]:
                pass
        return output

    # Summarize encounter information for output
    def summarize_encounters(encounters: list, write_if_empty: bool = True) -> dict:
        output = {}
        for enc in encounters:
            method = enc["encounter_slot_id"]["encounter_method_id"]["identifier"]
            version = enc["version_id"]["identifier"]
            pokemon = f"{enc['pokemon_id']['identifier']} ({enc['min_level']}-{enc['max_level']})"
            if method not in output:
                output[method] = {}
            if version not in output[method]:
                output[method][version] = {}
            if pokemon not in output[method][version]:
                output[method][version][pokemon] = int(enc["encounter_slot_id"]["rarity"])
            else:
                output[method][version][pokemon] += int(enc["encounter_slot_id"]["rarity"])
        if args.sort_by_natdex:
            for method, versions in output.items():
                for version, entries in versions.items():
                    output[method][version] = dict(
                        sorted(
                            entries.items(),
                            key=lambda item: int(
                                get_entry_by_identifier(sources["pokemon"].values(), item[0].split()[0])["species_id"]
                            ),
                        )
                    )
        return output

    def write_json(filename: str, output: dict):
        with open(os.path.join(args.outdir, filename), "w") as outfile:
            json.dump(output, outfile, indent=2)
            outfile.write("\n")

    # Write output files based on given options
    if args.weather:
        for weather, info in weather_location_area_encounters.items():
            for location_area, encounters in info.items():
                filename = f"{location_area}-{weather}.json" if weather != "weather-none" else f"{location_area}.json"
                result = summarize_encounters(encounters) if args.summary else restructure_encounters(encounters)
                if result:
                    write_json(filename, result)
    elif args.max_raid:
        total_result = {}

        for max_den, info in max_raid_location_area_encounters.items():
            for location_area, encounters in info.items():
                result = (
                    summarize_encounters(encounters)
                    if args.summary
                    else restructure_encounters(encounters)["encounters"]
                )
                if not result:
                    continue
                if args.summary:
                    if location_area not in total_result:
                        total_result[location_area] = {max_den: result}
                    else:
                        total_result[location_area][max_den] = result
                else:
                    if location_area not in total_result:
                        total_result[location_area] = {"encounters": {max_den: result}}
                    else:
                        total_result[location_area]["encounters"][max_den] = result

        for location_area, result in total_result.items():
            if result:
                write_json(f"{location_area}.json", result)
    else:
        for location_area, encounters in location_area_encounters.items():
            result = summarize_encounters(encounters) if args.summary else restructure_encounters(encounters)
            write_json(f"{location_area}.json", result)


if __name__ == "__main__":
    main()
