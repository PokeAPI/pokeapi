#!/usr/bin/env python3
"""Add a new PokeAPI language by copying rows from an existing language.

Dry-run by default. Pass --write to update files.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CSV_DIR = REPO_ROOT / "data" / "v2" / "csv"
TRAILING_BEFORE_NEWLINE = re.compile(r"[ \t]+(?=\n)")


@dataclass(frozen=True)
class NewLanguageConfig:
    source_language_id: str
    target_language_row: list[str]
    target_language_names: dict[str, str]
    source_language_names: dict[str, str]
    target_local_language_names: dict[str, str]

    @property
    def target_language_id(self) -> str:
        return self.target_language_row[0]


@dataclass(frozen=True)
class PlannedUpdate:
    path: Path
    summary_count: int
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="JSON config describing the new language.",
    )
    parser.add_argument(
        "--csv-dir",
        default=DEFAULT_CSV_DIR,
        type=Path,
        help="Path to data/v2/csv. Defaults to this repository's CSV dir.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes. Without this flag, only print planned changes.",
    )
    return parser.parse_args()


def csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    return str(value)


def string_mapping(value: Any, field_name: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return {str(key): str(item) for key, item in value.items()}


def load_config(path: Path) -> NewLanguageConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")

    source_language_id = csv_value(data["source_language_id"])
    target_language = data["target_language"]
    if not isinstance(target_language, dict):
        raise ValueError("target_language must be an object")

    target_language_row = [
        csv_value(target_language["id"]),
        csv_value(target_language["iso639"]),
        csv_value(target_language["iso3166"]),
        csv_value(target_language["identifier"]),
        csv_value(target_language["official"]),
        csv_value(target_language["order"]),
    ]

    target_language_names = string_mapping(
        data.get("target_language_names"), "target_language_names"
    )
    if target_language_row[0] not in target_language_names:
        raise ValueError(
            "target_language_names must include the target language's own name"
        )

    return NewLanguageConfig(
        source_language_id=source_language_id,
        target_language_row=target_language_row,
        target_language_names=target_language_names,
        source_language_names=string_mapping(
            data.get("source_language_names"), "source_language_names"
        ),
        target_local_language_names=string_mapping(
            data.get("target_local_language_names"), "target_local_language_names"
        ),
    )


def read_csv(path: Path) -> tuple[list[str], list[list[str]], int]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    if not rows:
        return [], [], 0

    header = rows[0]
    blank_records = sum(1 for row in rows[1:] if not row)
    data_rows = [row for row in rows[1:] if row]
    return header, data_rows, blank_records


def render_csv(header: list[str], rows: list[list[str]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return output.getvalue()


def int_sort_key(value: str) -> tuple[int, str]:
    try:
        return int(value), value
    except ValueError:
        return 10**9, value


def clean_copied_field(value: str) -> str:
    value = TRAILING_BEFORE_NEWLINE.sub("", value)
    return value.rstrip(" \t")


def clean_target_row(row: list[str]) -> list[str]:
    return [clean_copied_field(value) for value in row]


def update_languages(
    rows: list[list[str]], config: NewLanguageConfig
) -> tuple[list[list[str]], int]:
    by_id = {row[0]: row for row in rows}
    before = dict(by_id)
    by_id[config.target_language_id] = config.target_language_row

    updated_rows = sorted(by_id.values(), key=lambda row: int_sort_key(row[0]))
    changed = sum(1 for key, row in by_id.items() if before.get(key) != row)
    changed += sum(1 for key in before if key not in by_id)
    return updated_rows, changed


def update_language_names(
    header: list[str], rows: list[list[str]], config: NewLanguageConfig
) -> tuple[list[list[str]], int]:
    language_idx = header.index("language_id")
    local_idx = header.index("local_language_id")
    name_idx = header.index("name")
    by_key = {(row[language_idx], row[local_idx]): row for row in rows}
    before = dict(by_key)

    for language_id, name in config.source_language_names.items():
        by_key[(language_id, config.source_language_id)] = [
            language_id,
            config.source_language_id,
            name,
        ]

    for row in list(by_key.values()):
        if row[local_idx] == config.source_language_id:
            new_row = row.copy()
            new_row[local_idx] = config.target_language_id
            by_key[(new_row[language_idx], config.target_language_id)] = new_row

    for language_id, name in config.target_local_language_names.items():
        by_key[(language_id, config.target_language_id)] = [
            language_id,
            config.target_language_id,
            name,
        ]

    for local_language_id, name in config.target_language_names.items():
        by_key[(config.target_language_id, local_language_id)] = [
            config.target_language_id,
            local_language_id,
            name,
        ]

    updated_rows = sorted(
        by_key.values(),
        key=lambda row: (int_sort_key(row[language_idx]), int_sort_key(row[local_idx])),
    )
    changed = sum(1 for key, row in by_key.items() if before.get(key) != row)
    changed += sum(1 for key in before if key not in by_key)

    # Avoid unused local if this function is extended and make the expected
    # schema explicit.
    assert name_idx == 2
    return updated_rows, changed


def clone_language_rows(
    rows: list[list[str]], language_idx: int, config: NewLanguageConfig
) -> tuple[list[list[str]], int]:
    output = []
    existing_target_groups = set()
    source_rows_by_group: dict[tuple[str, ...], list[list[str]]] = {}
    changed = 0

    for row in rows:
        group = tuple(row[:language_idx])
        if row[language_idx] == config.target_language_id:
            existing_target_groups.add(group)
        elif row[language_idx] == config.source_language_id:
            source_rows_by_group.setdefault(group, []).append(row)

    for index, row in enumerate(rows):
        if row[language_idx] == config.target_language_id:
            cleaned_row = clean_target_row(row)
            if cleaned_row != row:
                changed += 1
            output.append(cleaned_row)
        else:
            output.append(row)

        group = tuple(row[:language_idx])
        next_group = (
            tuple(rows[index + 1][:language_idx]) if index + 1 < len(rows) else None
        )
        if group == next_group:
            continue
        if group not in source_rows_by_group or group in existing_target_groups:
            continue

        for source_row in source_rows_by_group[group]:
            new_row = source_row.copy()
            new_row[language_idx] = config.target_language_id
            output.append(clean_target_row(new_row))
            changed += 1
        existing_target_groups.add(group)

    return output, changed


def language_column_for(path: Path, header: list[str]) -> str | None:
    if path.name in {"languages.csv", "language_names.csv"}:
        return None
    if "local_language_id" in header:
        return "local_language_id"
    if "language_id" in header:
        return "language_id"
    return None


def updated_rows_for(
    path: Path, header: list[str], rows: list[list[str]], config: NewLanguageConfig
) -> tuple[list[list[str]], int] | None:
    if path.name == "languages.csv":
        return update_languages(rows, config)
    if path.name == "language_names.csv":
        return update_language_names(header, rows, config)

    language_column = language_column_for(path, header)
    if not language_column:
        return None

    language_idx = header.index(language_column)
    if not any(row[language_idx] == config.source_language_id for row in rows):
        return None

    return clone_language_rows(rows, language_idx, config)


def plan_updates(csv_dir: Path, config: NewLanguageConfig) -> list[PlannedUpdate]:
    updates = []

    for path in sorted(csv_dir.glob("*.csv")):
        original_text = path.read_text(encoding="utf-8")
        header, rows, blank_records = read_csv(path)
        if not header:
            continue

        result = updated_rows_for(path, header, rows, config)
        if result is None:
            continue

        updated_rows, changed = result
        updated_text = render_csv(header, updated_rows)
        if updated_text != original_text:
            updates.append(
                PlannedUpdate(
                    path=path,
                    summary_count=changed + blank_records,
                    text=updated_text,
                )
            )

    return updates


def main() -> int:
    args = parse_args()
    config = load_config(args.config.resolve())
    csv_dir = args.csv_dir.resolve()
    updates = plan_updates(csv_dir, config)

    for update in updates:
        print(f"{update.path.name}: {update.summary_count} planned row update(s)")
        if args.write:
            update.path.write_text(update.text, encoding="utf-8")

    if not updates:
        print("No changes needed.")
    elif args.write:
        print(f"Wrote {len(updates)} file(s).")
    else:
        print(f"Dry run only. Pass --write to update {len(updates)} file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
