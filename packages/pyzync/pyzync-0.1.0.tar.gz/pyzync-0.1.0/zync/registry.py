# as inspired by django's apps and appconfig
import inspect
from collections import defaultdict
from importlib import import_module

from zync import Item


def build_registry(item_classes: list):
    # Mapping of all normal_models to their respective items
    all_normal_models = defaultdict(lambda: set())

    # For each item, register its model
    for item in item_classes:
        model = item.normalizer.normal_model
        all_normal_models[model].add(item)

    return dict(all_normal_models)


def import_items(item_packages):
    item_classes = []
    for item_package in item_packages:
        # TODO make the magic string "items" into a configuration
        mod = import_module(item_package + ".items")
        for member in inspect.getmembers(mod):
            if (
                inspect.isclass(member[1])
                and member[1] is not Item
                and issubclass(member[1], Item)
            ):
                item_classes.append(member[1])
    return item_classes
