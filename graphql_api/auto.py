import os
import importlib
import logging
from inspect import getmembers, isclass

logger = logging.getLogger(__name__)


def schema_operations_builder(
    operation_name, operation_module, operation_base, cls_name, **properties
):
    op_base_classes = build_base_classes(
        operation_name, operation_module, operation_base, cls_name
    )

    if not op_base_classes:
        raise ValueError(
            f"Found no '{operation_base}' classes in '{operation_module}' module of subdirectories."
        )

    for base_class in op_base_classes:
        properties.update(base_class.__dict__["_meta"].fields)
    return type(operation_name, tuple(op_base_classes), properties)


def build_base_classes(operation_name, operation_module, operation_base, cls_name):
    current_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "schema"
    )
    subdirectories = [
        x
        for x in os.listdir(current_directory)
        if os.path.isdir(os.path.join(current_directory, x))
        and x not in ["__pycache__", "root"]
    ]
    op_base_classes = []

    for directory in subdirectories:
        try:
            module = importlib.import_module(
                f"graphql_api.schema.{directory}.{operation_module}"
            )
            if module:
                classes = [x for x in getmembers(module, isclass)]
                opers = [
                    x[1] for x in classes if cls_name in x[0] and x[0] != operation_base
                ]
                op_base_classes += opers
            else:
                logger.info("wat?")
                logger.debug(current_directory)

        except ModuleNotFoundError:
            pass

    op_base_classes = op_base_classes[::-1]
    return op_base_classes
