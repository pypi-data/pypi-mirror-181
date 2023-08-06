from __future__ import annotations

import os
import importlib
import logging
import enum
import uuid
import yaml
import jsonschema
import drb.utils.plugins
from jsonschema.exceptions import ValidationError
from typing import Dict, Iterable, List, Optional

from .factory import DrbFactory, FactoryLoader
from .signature import Signature, parse_signature
from drb.core.node import DrbNode
from drb.exceptions.core import DrbException


logger = logging.getLogger('ItemClass')


def _load_drb_item_classes() -> Dict[uuid.UUID, ItemClass]:
    """
    Loads item classes defined in the Python context
    """
    entry_point_group = 'drb.topic'
    result = {}

    for ep in drb.utils.plugins.get_entry_points(entry_point_group):
        # load module
        try:
            module = importlib.import_module(ep.value)
        except ModuleNotFoundError as ex:
            logger.warning(f'Invalid entry point {ep.name}: {ex.msg}')
            continue

        # check item class description file
        try:
            path = os.path.join(module.__path__[0], 'cortex.yml')
            ItemClass.validate(path)
        except (FileNotFoundError, ValidationError) as ex:
            logger.warning(
                f'Invalid item class description(s) from {ep.name}: {ex}')
            continue

        # load deserialize item classes
        with open(path) as file:
            data = yaml.safe_load_all(file)
            for ic_data in data:
                try:
                    ic = ItemClass(ic_data)
                except (KeyError, DrbException) as ex:
                    logger.error(f'Failed to load item class: {ic_data}')
                    logger.error(ex)
                    continue

                if ic.id in result:
                    logger.warning(
                        f'Item class definition conflict: id ({ic.id}) used '
                        f'by {result[ic.id].label} and {ic.label}')
                else:
                    result[ic.id] = ic
    return result


class ItemClassType(enum.Enum):
    SECURITY = 'SECURITY'
    PROTOCOL = 'PROTOCOL'
    CONTAINER = 'CONTAINER'
    FORMATTING = 'FORMATTING'


class ItemClass:
    """
    Defines a type of item, this type is described in each DRB topic or
    implementation.

    Parameters:
        data (dict): data of item class definition
    Raises:
        KeyError: if data content is not valid
        DrbException: if an error occurred during item class generation
    """
    __schema_path = os.path.join(os.path.dirname(__file__), 'it_schema.yml')
    __schema = None

    @classmethod
    def validate(cls, path: str):
        """
        Checks validity of an item class description file.
        Parameters:
            path (str): path of item class description file
        Raises:
            FileNotFoundError - if path does not exist
            ValidationError - if the description file is not valid
        """
        if cls.__schema is None:
            with open(cls.__schema_path) as file:
                cls.__schema = yaml.safe_load(file)

        with open(path) as file:
            for it in yaml.safe_load_all(file):
                jsonschema.validate(it, cls.__schema)

    def __init__(self, data: dict):
        self.__id = uuid.UUID(data['id'])
        self.__label = data['label']
        self.__category = ItemClassType(data['category'])
        self.__description = data.get('description', None)
        self.__signatures = []
        signatures = data.get('signatures', None)
        if signatures is not None:
            self.__signatures = [parse_signature(s) for s in signatures]
        self.__override = False
        if 'subClassOf' in data:
            value = data['subClassOf']
            if isinstance(value, dict):
                self.__parent = uuid.UUID(value['id'])
                self.__override = value.get('override', False)
            else:
                # value is an UUID string
                self.__parent = uuid.UUID(value)
        else:
            self.__parent = None

        self.__factory_name = None
        if 'factory' in data:
            self.__factory_name = data['factory']

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def parent_class_id(self) -> uuid.UUID:
        return self.__parent

    def is_override_super_class(self) -> bool:
        return self.__override

    @property
    def label(self) -> str:
        return self.__label

    @property
    def description(self) -> str:
        return self.__description

    @property
    def category(self) -> ItemClassType:
        return self.__category

    @property
    def factory(self) -> Optional[DrbFactory]:
        if self.__factory_name is not None:
            return FactoryLoader().get_factory(self.__factory_name)
        return None

    @property
    def signatures(self) -> List[Signature]:
        return self.__signatures

    def matches(self, node: DrbNode) -> bool:
        """
        Checks if the given node match one of its signatures.

        Parameters:
            node(DrbNode): node supportability to check
        Returns:
            bool: ``True`` if the given node is supported by the item class
        """
        for signature in self.__signatures:
            if signature.matches(node):
                return True
        return False

    def __repr__(self):
        return self.__label


class ItemClassLoader:
    """
    Manages loading and retrieving of item classes defined in the Python
    context.
    """
    __instance = None
    __item_classes = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ItemClassLoader, cls).__new__(cls)
            cls.__item_classes = _load_drb_item_classes()
        return cls.__instance

    def get_all_item_classes(self) -> Iterable[ItemClass]:
        """
        Returns all loaded item classes.
        Returns:
            Iterable: An iterable containing all loaded item classes.
        """
        return self.__item_classes.values()

    def get_item_class(self, identifier: uuid.UUID) -> ItemClass:
        """
        Retrieves an item class.
        Parameters:
            identifier (UUID): item class UUID
        Returns:
            ItemClass: the item class identified by the given UUID.
        Raises:
            KeyError: if no item class corresponds to the given UUID
        """
        return self.__item_classes[identifier]

    def is_subclass(self, actual: ItemClass, expected: ItemClass) -> bool:
        """
        Check if an item class is subclass of another.

        Parameters:
            actual(ItemClass): item class to check
            expected(ItemClass): expected parent class
        Returns:
            bool: ``True`` if the given actual item class is a subclass of the
                  expected one, otherwise ```False``
        """
        if actual == expected:
            return True

        if actual.parent_class_id is None:
            return False

        return self.is_subclass(self.get_item_class(actual.parent_class_id),
                                expected)
