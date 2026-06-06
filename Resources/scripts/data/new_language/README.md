# New language CSV helpers

These scripts bootstrap a new language in `data/v2/csv` by copying an existing
language's rows as the initial translation source.

Run a dry run:

```sh
python3 Resources/scripts/data/new_language/apply_new_language.py \
  --config Resources/scripts/data/new_language/es_419.json
```

Apply the changes:

```sh
python3 Resources/scripts/data/new_language/apply_new_language.py \
  --config Resources/scripts/data/new_language/es_419.json \
  --write
```

Validate:

```sh
python3 Resources/scripts/data/new_language/validate_new_language.py \
  --config Resources/scripts/data/new_language/es_419.json
```

The config file defines:

- `source_language_id`: existing language ID to copy translation rows from.
- `target_language`: the row to upsert in `languages.csv`.
- `target_language_names`: names for the new language in each local language.
- `source_language_names`: optional exact names to upsert for the source local
  language in `language_names.csv`.
- `target_local_language_names`: optional exact names to upsert for existing
  languages in the new target local language.
