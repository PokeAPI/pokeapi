import os
import importlib
import logging
from inspect import getmembers, isclass
from graphene import ObjectType

logger = logging.getLogger(__name__)


def schema_operations_builder(operationName, operationModule, operationBase, clsName):

    op_base_classes = build_base_classes(
        operationName, operationModule, operationBase, clsName
    )

    if len(op_base_classes) <= 1:
        raise ValueError(
            f"Found no '{operationBase}' classes in '{operationModule}' module of subdirectories."
        )

    properties = {}
    # filter on scopes before this
    for base_class in op_base_classes:
        properties.update(base_class.__dict__["_meta"].fields)
    ALL = type(operationName, tuple(op_base_classes), properties)
    return ALL


def build_base_classes(operationName, operationModule, operationBase, clsName):
    class OperationAbstract(ObjectType):
        scopes = ["unauthorized"]
        pass

    current_directory = os.path.dirname(os.path.abspath(__file__))
    # current_module = current_directory.split("/")[-1]
    subdirectories = [
        x
        for x in os.listdir(current_directory)
        if os.path.isdir(os.path.join(current_directory, x))
        and x != "__pycache__"
        and x != "root"
    ]
    op_base_classes = [OperationAbstract]

    for directory in subdirectories:
        try:
            module = importlib.import_module(
                f"graphql_api.{directory}.{operationModule}"
            )
            if module:
                classes = [x for x in getmembers(module, isclass)]
                opers = [
                    x[1] for x in classes if clsName in x[0] and x[0] != operationBase
                ]
                op_base_classes += opers
            else:
                logger.info("wat?")
                logger.debug(current_directory)

        except ModuleNotFoundError as e:
            pass

    op_base_classes = op_base_classes[::-1]
    return op_base_classes
