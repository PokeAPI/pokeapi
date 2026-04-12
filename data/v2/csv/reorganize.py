import csv


def reorganize_mechanics():
    print("Loading CSV files...")

    # --- 1. READ ALL DATA ---
    with open("item_mechanic.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        mechanics = list(reader)
        mechanics_fields = reader.fieldnames

    with open("item_mechanic_condition.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        conditions = list(reader)
        conditions_fields = reader.fieldnames

    with open("item_mechanic_effect.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        effects = list(reader)
        effects_fields = reader.fieldnames

    print("Sorting Mechanics and Generating New IDs...")

    # --- 2. SORT MECHANICS ---
    # Sort by: item_id -> version_group_id -> operation_order
    mechanics.sort(
        key=lambda x: (
            int(x["item_id"]),
            int(x["version_group_id"]),
            int(x["operation_order"]),
        )
    )

    # --- 3. MAP NEW IDs ---
    id_mapping = {}
    for new_id, row in enumerate(mechanics, start=1):
        old_id = row["id"]
        id_mapping[old_id] = str(new_id)
        row["id"] = str(new_id)  # Assign the new ID to the mechanic

    print("Updating and Sorting Child Tables...")

    # --- 4. UPDATE & SORT CONDITIONS ---
    valid_conditions = []
    for row in conditions:
        old_mech_id = row["mechanic_id"]
        if old_mech_id in id_mapping:
            row["mechanic_id"] = id_mapping[old_mech_id]
            valid_conditions.append(row)

    # Sort conditions by new mechanic_id, then condition_group
    valid_conditions.sort(
        key=lambda x: (int(x["mechanic_id"]), int(x.get("condition_group", 1)))
    )

    # --- 5. UPDATE & SORT EFFECTS ---
    valid_effects = []
    for row in effects:
        old_mech_id = row["mechanic_id"]
        if old_mech_id in id_mapping:
            row["mechanic_id"] = id_mapping[old_mech_id]
            valid_effects.append(row)

    # Sort effects by new mechanic_id
    valid_effects.sort(key=lambda x: int(x["mechanic_id"]))

    print("Saving beautiful, clean CSVs...")

    # --- 6. SAVE FILES ---
    with open("item_mechanic.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=mechanics_fields)
        writer.writeheader()
        writer.writerows(mechanics)

    with open("item_mechanic_condition.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=conditions_fields)
        writer.writeheader()
        writer.writerows(valid_conditions)

    with open("item_mechanic_effect.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=effects_fields)
        writer.writeheader()
        writer.writerows(valid_effects)

    print(
        f"Success! Reorganized {len(mechanics)} mechanics from ID 1 to {len(mechanics)}."
    )


if __name__ == "__main__":
    reorganize_mechanics()
