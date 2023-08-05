from abc import ABC
from functools import wraps
from typing import Any, Union

from pydantic import BaseModel

from .data_store import DataStore
from .normalmodel import NormalModel

"""
This is the class for OBJECTS that arrive in from the services
Therefore the mapping to normal form must be declared as a class variable
Rather than an instance variable
"""


def default_translation(x, data):
    return x


class Normalizer(ABC):
    """
    An intermediary for the normal form of all data returned by services.

    This class contains a mapping and conversion methods for creating NormalModel objects

    CLASS VARIABLES DECLARED BY USER
    TRANSFORM

    NORMALMODEL CLASS
    """

    # TODO declare a normal_model attribute so that the ide doesn't complain
    TRANSLATE = False
    id_key = "uuid"

    def __init__(self, data_store: DataStore = None):
        if data_store is None:
            self.data_store = DataStore()
        else:
            self.data_store = data_store
        # TODO how do i run these assertions if i'm never initializing the class?
        # so far i'm using just classmethods
        # TODO assert that the class has the 3(?) attributes listed above
        assert hasattr(self, "id_path"), (
            "Normalizer must have an id_path attribute declared in "
            "order to store ids of item records."
        )
        assert hasattr(self, "transform"), (
            "Normalizer must have a transform attribute declared in the form "
            "of {'normalfield': 'servicefield' | ['servicefields'...]}."
        )
        assert hasattr(self, "normal_model"), (
            "Normalizer must have a normal_model attribute declared "
            "in order to return the data in the appropriate class."
        )

    def normalize_data(self, data) -> BaseModel:
        result = {}
        if hasattr(self, "Translator"):
            self.TRANSLATE = True

        for key, value in self.transform.items():
            if type(value) is list:
                field = data
                for name in value:
                    # TODO throw a really good clear exception here!
                    # tell the user that their transformer didn't work with the data
                    if type(name) is int and type(field) is list:
                        field = field[name]
                    else:
                        field = field.get(name)
            else:
                field = data.get(value)

            if self.TRANSLATE:
                # if there's no translator method for the field, return the field value
                translator_method = getattr(
                    self.Translator, "_".join(("normalize", key)), default_translation
                )
                result[key] = translator_method(field, data)
            else:
                result[key] = field

        return self.normal_model(**result)

    def normalize_id(self, data, func):
        # get the name of func's class for the data_store
        source_item_name = func.__qualname__.split(".")[-2]

        # make a query
        # field name is source item name
        # value is id from the data
        id_path = self.id_path
        if isinstance(id_path, list):
            item_id = data
            for name in id_path:
                item_id = item_id.get(name)
        else:
            item_id = data.get(id_path)

        normal_id = self.data_store.get_normal_id(
            source_item_name, item_id, self.normal_model
        )

        return normal_id

    def normalize(self, func, *args, **kwargs):
        data = func(*args, **kwargs)

        # TODO make this the init for the model (maybe?)
        model = self.normalize_data(data)
        uuid = self.normalize_id(data, func)
        model.uuid = uuid

        return model

    def norm_deco(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model = self.normalize(func, *args, **kwargs)

            return model

        return wrapper

    def normalize_many(self, func, *args, **kwargs):
        data = func(*args, **kwargs)

        results = []
        try:
            for item in data:
                model = self.normalize_data(item)
                uuid = self.normalize_id(item, func)
                model.uuid = uuid
                results.append(model)
        except TypeError as e:
            print(e)
            print("typeerror in normalize_many")
            print(func)
            raise e

        return results

    def norm_many_deco(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            models = self.normalize_many(func, *args, **kwargs)

            return models

        return wrapper

    def denormalize_data(self, model: NormalModel) -> dict:
        result = None
        model_dict = model.dict()
        # If you get AttributeError: 'NoneType' object has no attribute 'dict' here,
        # it's because the users methods didn't return anything. Help the user out!

        if hasattr(self, "Translator"):
            self.TRANSLATE = True

        for key, path in self.transform.items():
            # TODO fix this, create a read-only list the user may extend
            if key == "last_modified":
                continue
            result = self._insert_value_by_path(
                result, model_dict[key], key, path, model
            )

        return result

    def denormalize_id(self, data, func, model):
        destination_item_name = func.__qualname__.split(".")[-2]

        item_id = self.data_store.get_item_id(model, destination_item_name)

        result = self._insert_value_by_path(data, item_id, self.id_key, self.id_path)

        return result

    def denormalize(self, func, include_id, model):
        # TODO create appropriate exception here
        if not issubclass(type(model), NormalModel):
            raise Exception

        data = self.denormalize_data(model)

        if include_id:
            # TODO this may raise an exception if we're trying to do an update
            # but don't have the record's id
            data = self.denormalize_id(data, func, model)

        return data

    def denorm_deco(self, func, include_id: bool = True):
        # include_id basically means we're doing update instead of create
        # i might rename that variable to reflect that, but for now
        @wraps(func)
        def wrapper(*args, **kwargs):
            model = args[1]
            data = self.denormalize(func, include_id, model)
            rebuilt_args = (args[0], data, *args[2:])
            result = func(*rebuilt_args, **kwargs)

            # we need the resulting record's id
            # then we store or create it in the database
            # we need the current timestamp to be stored in the database
            # if create was run, we need to create the id
            destination_item_name = func.__qualname__.split(".")[-2]
            # id_record = self.data_store.create_id_record(
            #     destination_item_name, result, model
            # )
            # TODO write the time to mongo!
            # self.data_store.set_item_last_modified_time(
            #     model, id_record, destination_item_name, datetime.now()
            # )
            return result

        return wrapper

    def _insert_value_by_path(
        self,
        data,
        value: Any,
        key: str,
        path: Union[str, list],
        model: NormalModel = None,
    ):
        """
        Adds a value to a specific path in the data dictionary from the model.
        Model can be None if there's no translator for the field, such as uuid.
        """

        def build_list_around_data(path_index, list_index, prev_field=None):
            new_list = [None] * (list_index + 1)
            if path_index == 0:
                new_list[list_index] = self.translate_value(key, value, model)
            else:
                new_list[list_index] = prev_field
            return new_list

        def build_dict_around_data(path_index, dict_key, prev_field=None):
            if path_index == 0:
                new_dict = {dict_key: self.translate_value(key, value, model)}
            else:
                new_dict = {dict_key: prev_field}
            return new_dict

        def insert_data_to_list(arr, elem, arr_index):
            """
            Extends list with None elements if index out of range, then inserts the element
            """
            if arr_index < len(arr):
                arr[arr_index] = elem
            else:
                arr.extend([None] * (arr_index - len(arr) + 1))
                arr[arr_index] = elem
            return arr

        # Initialize data if necessary
        if data is None:
            if type(path) is list and type(path[0]) is int:
                data = []
            else:
                data = {}

        if type(path) is list:
            field = None
            root_index = 0

            # Find how far to the value the result has already been defined
            traverse_result = data
            for index, name in enumerate(path):
                if (
                    type(traverse_result) is list
                    and len(traverse_result) > name
                    and traverse_result[name] is not None
                ) or (type(traverse_result) is dict and name in traverse_result.keys()):
                    traverse_result = traverse_result[name]

                else:
                    root_index = index
                    break

            # build UP TO but NOT INCLUDING the root_index
            for index, name in enumerate(path[:root_index:-1]):
                if type(name) is int:
                    field = build_list_around_data(index, name, field)
                else:
                    field = build_dict_around_data(index, name, field)

            # Merge field and traverse_result at root_index
            if type(traverse_result) is list:
                insert_data_to_list(traverse_result, field, path[root_index])
            else:
                traverse_result[path[root_index]] = field

        else:
            data[path] = self.translate_value(key, value, model)

        return data

    def translate_value(self, key, value, model):

        # do not call translator methods for ids
        if self.TRANSLATE and key != self.id_key:
            # if there's no translator method for the field, return the field value
            translator_method = getattr(
                self.Translator, "_".join(("denormalize", key)), default_translation
            )
        else:
            translator_method = default_translation

        return translator_method(value, model)


"""
TODO the user then needs an opportunity to declare relationships to other objects
This may be handled by the normal form instead?
Or its just the ids, and we keep a DB of ids of objects in all services
special conversion method for this?
"""
