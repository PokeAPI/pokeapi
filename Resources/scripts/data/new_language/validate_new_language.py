#!/usr/bin/env python3
"""Validate CSV additions created by apply_new_language.py."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from apply_new_language import (
    DEFAULT_CSV_DIR,
    NewLanguageConfig,
    clean_target_row,
    language_column_for,
    load_config,
)


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
        "--check-copied-values",
        action="store_true",
        help="Also require target rows to match copied source row values.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [], []
    return rows[0], rows[1:]


def check_no_blank_records(csv_dir: Path, errors: list[str]) -> None:
    for path in sorted(csv_dir.glob("*.csv")):
        _, rows = read_csv(path)
        for index, row in enumerate(rows, start=2):
            if not row:
                errors.append(f"{path.name}:{index}: blank CSV record")


def check_languages(
    csv_dir: Path, config: NewLanguageConfig, errors: list[str]
) -> None:
    header, rows = read_csv(csv_dir / "languages.csv")
    if not header:
        errors.append("languages.csv is empty")
        return

    by_id = {row[0]: row for row in rows if row}
    actual = by_id.get(config.target_language_id)
    if actual != config.target_language_row:
        errors.append(
            "languages.csv: expected "
            + ",".join(config.target_language_row)
            + f"; found {actual}"
        )


def check_exact_language_names(
    label: str,
    expected_names: dict[str, str],
    local_language_id: str,
    by_key: dict[tuple[str, str], str],
    errors: list[str],
) -> None:
    for language_id, expected_name in expected_names.items():
        actual = by_key.get((language_id, local_language_id))
        if actual != expected_name:
            errors.append(
                f"language_names.csv: {label} expected "
                f"({language_id}, {local_language_id}) to be "
                f"{expected_name!r}; found {actual!r}"
            )


def check_language_names(
    csv_dir: Path, config: NewLanguageConfig, errors: list[str]
) -> None:
    header, rows = read_csv(csv_dir / "language_names.csv")
    if not header:
        errors.append("language_names.csv is empty")
        return

    language_idx = header.index("language_id")
    local_idx = header.index("local_language_id")
    name_idx = header.index("name")
    by_key = {
        (row[language_idx], row[local_idx]): row[name_idx] for row in rows if row
    }

    for local_language_id, expected_name in config.target_language_names.items():
        actual = by_key.get((config.target_language_id, local_language_id))
        if actual != expected_name:
            errors.append(
                "language_names.csv: target_language_names expected "
                f"({config.target_language_id}, {local_language_id}) to be "
                f"{expected_name!r}; found {actual!r}"
            )

    check_exact_language_names(
        "source_language_names",
        config.source_language_names,
        config.source_language_id,
        by_key,
        errors,
    )
    check_exact_language_names(
        "target_local_language_names",
        config.target_local_language_names,
        config.target_language_id,
        by_key,
        errors,
    )

    source_language_rows = {
        row[language_idx]
        for row in rows
        if row and row[local_idx] == config.source_language_id
    }
    missing_target_language_rows = sorted(
        language_id
        for language_id in source_language_rows
        if (language_id, config.target_language_id) not in by_key
    )
    if missing_target_language_rows:
        errors.append(
            "language_names.csv: missing target local-language names for "
            + ", ".join(missing_target_language_rows)
        )


def rows_by_language_group(
    rows: list[list[str]], language_idx: int, language_id: str
) -> dict[tuple[str, ...], list[list[str]]]:
    grouped: dict[tuple[str, ...], list[list[str]]] = {}
    for row in rows:
        if row and row[language_idx] == language_id:
            grouped.setdefault(tuple(row[:language_idx]), []).append(row)
    return grouped


def check_copied_table_coverage(
    path: Path,
    header: list[str],
    rows: list[list[str]],
    config: NewLanguageConfig,
    check_values: bool,
    errors: list[str],
) -> None:
    language_column = language_column_for(path, header)
    if not language_column:
        return

    language_idx = header.index(language_column)
    source_groups = rows_by_language_group(rows, language_idx, config.source_language_id)
    target_groups = rows_by_language_group(rows, language_idx, config.target_language_id)

    missing_groups = sorted(set(source_groups) - set(target_groups))
    if missing_groups:
        examples = ", ".join("/".join(group) for group in missing_groups[:5])
        errors.append(
            f"{path.name}: missing {len(missing_groups)} target-language row(s); "
            f"examples: {examples}"
        )
        return

    if not check_values:
        return

    for group, source_rows in source_groups.items():
        target_rows = target_groups[group]
        expected_rows = []
        for source_row in source_rows:
            expected_row = source_row.copy()
            expected_row[language_idx] = config.target_language_id
            expected_rows.append(clean_target_row(expected_row))
        if sorted(expected_rows) != sorted(clean_target_row(row) for row in target_rows):
            errors.append(f"{path.name}: copied values differ for group {'/'.join(group)}")


def check_copied_tables(
    csv_dir: Path,
    config: NewLanguageConfig,
    check_values: bool,
    errors: list[str],
) -> None:
    for path in sorted(csv_dir.glob("*.csv")):
        header, rows = read_csv(path)
        if not header:
            continue
        check_copied_table_coverage(path, header, rows, config, check_values, errors)


def main() -> int:
    args = parse_args()
    config = load_config(args.config.resolve())
    csv_dir = args.csv_dir.resolve()
    errors: list[str] = []

    check_no_blank_records(csv_dir, errors)
    check_languages(csv_dir, config, errors)
    check_language_names(csv_dir, config, errors)
    check_copied_tables(csv_dir, config, args.check_copied_values, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"{config.target_language_row[3]} CSV validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
