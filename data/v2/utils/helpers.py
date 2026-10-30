import csv
from collections.abc import Callable, Generator, Iterable
from contextlib import closing
from pathlib import Path

from django.db import connection
from django.db.models import Model

DATA_LOCATION = Path(__file__).resolve().parents[1] / "csv"
BATCH_SIZE: int = 1_000


def load_data(file_name: str) -> Generator[list[str], None, None]:
    with open(DATA_LOCATION / file_name, encoding="utf8") as file:
        yield from csv.reader(file, delimiter=",")


def clear_table(model: type[Model]) -> None:
    table_name = model._meta.db_table
    model.objects.all().delete()
    print("building " + table_name)
    with connection.cursor() as cursor:
        if connection.vendor == "sqlite":
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'")
        else:
            # Reset DB auto increments to start at 1
            cursor.execute("SELECT setval(pg_get_serial_sequence(" + "'" + table_name + "'" + ",'id'), 1, false);")


def build_generic(
    model_classes: tuple[type[Model], ...],
    file_name: str,
    csv_record_to_objects: Callable[[list[str]], Iterable[Model]],
    *,
    batch_size: int = BATCH_SIZE,
) -> None:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")

    batches: dict[type[Model], list[Model]] = {}

    for model_class in model_classes:
        clear_table(model_class)
        batches[model_class] = []

    with closing(load_data(file_name)) as csv_data:
        next(csv_data, None)  # skip header

        for csv_record in csv_data:
            for obj in csv_record_to_objects(csv_record):
                model_class = type(obj)
                batch = batches[model_class]
                batch.append(obj)

                if len(batch) >= batch_size:
                    model_class.objects.bulk_create(batch)
                    batches[model_class] = []

    for model_class, batch in batches.items():
        if batch:
            model_class.objects.bulk_create(batch)
