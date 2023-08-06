import os
import os.path
import logging
import pathlib
import sys
import re

from urllib.parse import urlparse
from typing import List, Optional, Tuple, Union
from drb.core.node import DrbNode
from drb.core.factory import DrbFactory
from drb.core.item_class import ItemClass, ItemClassType, ItemClassLoader
from drb.exceptions.core import DrbFactoryException, DrbException
from drb.nodes.url_node import UrlNode


logger = logging.getLogger('DrbResolver')


def _is_remote_url(parsed_path):
    """
    Checks if the given parsed URL is a remote URL
    """
    return parsed_path.scheme != '' and parsed_path.scheme != 'file'


class _DrbFactoryResolver(DrbFactory):
    """ The factory resolver

    The factory resolver aims to parametrize the selection of the factory
    able to resolves the nodes according to its physical input.
    """

    __instance = None
    __item_classes = None
    __overridden: List[ItemClass] = None
    __protocols: List[ItemClass] = None
    __containers: List[ItemClass] = None
    __highest_containers: List[ItemClass] = None
    __formats: List[ItemClass] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(_DrbFactoryResolver, cls).__new__(cls)
            cls.__item_classes = ItemClassLoader().get_all_item_classes()
            cls.__overridden = []
            cls.__protocols = []
            cls.__containers = []
            cls.__formats = []
            for ic in cls.__item_classes:
                if ic.is_override_super_class():
                    cls.__overridden.append(ic)
                if ItemClassType.PROTOCOL == ic.category:
                    cls.__protocols.append(ic)
                elif ItemClassType.CONTAINER == ic.category:
                    cls.__containers.append(ic)
                elif ItemClassType.FORMATTING == ic.category:
                    cls.__formats.append(ic)
                else:
                    logger.warning('DRB resolver does not support item type: '
                                   f'{ic.category.name}')
            cls.__highest_containers = [x for x in cls.__containers
                                        if x.parent_class_id is None]
        return cls.__instance

    def _create(self, node: DrbNode) -> DrbNode:
        item_class, n = self.resolve(node)
        return n

    def __retrieve_protocol(self, node: DrbNode) -> Optional[ItemClass]:
        """
        Retrieves the protocol item class associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            DrbNode: a protocol item class associated to the given node or
                     ``None`` if no protocol item class is found.
        """
        for protocol in self.__protocols:
            if protocol.matches(node):
                return protocol
        return None

    def __retrieve_container(self, node: DrbNode) -> Tuple[ItemClass, DrbNode]:
        """
        Retrieves the container signature associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            ItemClass, DrbNode: A item class matching the given node and the
                                associated node
        """
        for s in self.__highest_containers:
            if s.matches(node):
                return self.__finest_item_class(node, s)
        return None, node

    def __finest_item_class(self, node: DrbNode, finest: ItemClass) \
            -> Tuple[ItemClass, DrbNode]:
        """
        Retrieves the finest item class associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
            finest (ItemClass): current finest item class matching the given
                                node
        Returns:
            ItemClass: the finest item class matching the given node
        """
        subclasses = [x for x in self.__item_classes
                      if x.parent_class_id == finest.id]
        for item_class in subclasses:
            if item_class.matches(node):
                n = node
                if item_class.factory is not None:
                    n = item_class.factory.create(node)
                return self.__finest_item_class(n, item_class)
        return finest, node

    def __retrieve_formatting(self, node) -> Optional[ItemClass]:
        """
        Retrieves the formatting item class associated to the given node.

        Parameters:
            node (DrbNode): node which need to be resolved
        Returns:
            ItemClass: A formatting item class matching the given node,
                       otherwise ``None``
        """
        for item_class in self.__formats:
            if item_class.matches(node):
                return item_class
        return None

    def __create_from_url(self, url: str, curl: str = None,
                          path: List[str] = None) -> DrbNode:
        """
        Parses the given url to retrieve the targeted resource to open as node
        This method allows to target an inner resource (e.g. a XML file in a
        zipped data from a HTTP URL)

        Parameters:
            url (str): targeted resource URL
            curl (str): current URL (internal processing)
            path (list): remaining path of the given URL (internal processing)
        Returns:
            DrbNode: A DrbNode representing the requested URL resource.
        Raises:
            DrbFactoryException: if an error appear
        """

        # Full Windows path like c:/foo are not parsed correctly with urlparse
        # so we make it into a uri that can be parsed
        if (sys.platform == "win32"
                and re.match(r"^[a-zA-Z]:", url)):
            url = pathlib.Path(url).as_uri().replace('%20', ' ')
        pp = urlparse(url)

        if curl is None and path is None:
            try:
                return self.create(UrlNode(url))
            except (DrbFactoryException, DrbException,
                    IndexError, KeyError, TypeError):
                pass

            if _is_remote_url(pp):
                curl = f'{pp.scheme}://{pp.netloc}'

            # Uri of Windows path parsed with urlparse returns a path like
            # /c:/foo/bar which is incorrect, so we take out the firt '/'
            if (sys.platform == "win32"
                    and re.match(r"^/[a-zA-Z]:", pp.path)):
                path = list(pathlib.Path(pp.path[1:]).parts)
            else:
                path = list(pathlib.Path(pp.path).parts)
            if curl is None:
                seg = path.pop(0)
                curl = seg if os.path.isabs(pp.path) else f'{os.sep}{seg}'

        # try to create node from curl
        try:
            node = self.create(UrlNode(curl))
            for child in path:
                if child != '':
                    node = node[child]
            return node
        except (DrbFactoryException, DrbException,
                IndexError, KeyError, TypeError):
            if curl == url or len(path) == 0:
                raise DrbFactoryException(f'Cannot resolve URL: {url}')
            if _is_remote_url(pp):
                seg = path.pop(0)
                # skip empty string (e.g. /path/to//data)
                if seg == '':
                    seg = path.pop(0)
                curl += f'/{seg}'
            else:
                curl = os.path.join(curl, path.pop(0))
            return self.__create_from_url(url, curl, path)

    def _resolve_overridden(self, source: DrbNode) -> \
            Optional[Tuple[ItemClass, Optional[DrbNode]]]:
        for ic in self.__overridden:
            if ic.matches(source):
                return self.__finest_item_class(source, ic)
        return None

    def _basic_resolve(self, source: DrbNode) -> \
            Tuple[ItemClass, Optional[DrbNode]]:
        if isinstance(source, str):
            node = UrlNode(source)
        else:
            node = source
        protocol = None

        if node.parent is None:
            protocol = self.__retrieve_protocol(node)
            if protocol is None:
                raise DrbFactoryException(f'Cannot resolve: {source}')
            node = protocol.factory.create(node)

        container, node = self.__retrieve_container(node)
        if container is not None and container.factory is not None:
            node = container.factory.create(node)

        formatting = self.__retrieve_formatting(node)
        if formatting is not None:
            if formatting.factory is not None:
                node = formatting.factory.create(node)
            return self.__finest_item_class(node, formatting)

        if container is None:
            if protocol is None:
                raise DrbFactoryException(f'Cannot resolve: {source}')
            return protocol, node

        return container, node

    def resolve(self, source: Union[str, DrbNode]) \
            -> Tuple[ItemClass, Optional[DrbNode]]:
        """
        Retrieves the item class related to the given source.

        Parameters:
            source: source to be resolved
        Returns:
            tuple: A tuple containing an ItemClass corresponding to the given
                   source and the last DrbNode allowing to resolve the given
                   source (maybe to ``None``)
        Raises:
            DrbFactoryException: if the given source cannot be resolved.
        """
        if isinstance(source, str):
            node = UrlNode(source)
        else:
            node = source

        result = self._resolve_overridden(node)
        if result is not None:
            return result
        return self._basic_resolve(node)

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        if isinstance(source, str):
            return self.__create_from_url(source)
        if isinstance(source, DrbNode):
            return self._basic_resolve(source)[1]
        raise DrbFactoryException(f'Invalid source type: {type(source)}')


class DrbNodeList(list):
    def __init__(self, children: List[DrbNode]):
        super(DrbNodeList, self).__init__()
        self._list: List[DrbNode] = children

    @staticmethod
    def __resolve_node(node: DrbNode):
        try:
            return create(node)
        except DrbFactoryException:
            return node

    def __getitem__(self, item):
        result = self._list[item]
        if isinstance(result, DrbNode):
            return self.__resolve_node(result)
        else:
            return [self.__resolve_node(node) for node in result]

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return DrbNodeListIterator(self._list.__iter__())

    def append(self, obj) -> None:
        raise DrbFactoryException

    def clear(self) -> None:
        raise DrbFactoryException

    def copy(self) -> List:
        raise DrbFactoryException

    def count(self, value) -> int:
        raise DrbFactoryException

    def insert(self, index: int, obj) -> None:
        raise DrbFactoryException

    def extend(self, iterable) -> None:
        raise DrbFactoryException

    def index(self, value, start: int = ..., __stop: int = ...) -> int:
        raise DrbFactoryException

    def pop(self, index: int = ...):
        raise DrbFactoryException

    def remove(self, value) -> None:
        raise DrbFactoryException

    def reverse(self) -> None:
        raise DrbFactoryException

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        raise DrbFactoryException

    def __eq__(self, other):
        raise DrbFactoryException

    def __ne__(self, other):
        raise DrbFactoryException

    def __add__(self, other):
        raise DrbFactoryException

    def __iadd__(self, other):
        raise DrbFactoryException

    def __radd__(self, other):
        raise DrbFactoryException

    def __setitem__(self, key, value):
        raise DrbFactoryException


class DrbNodeListIterator:
    def __init__(self, iterator):
        self.base_itr = iterator

    def __iter__(self):
        return self

    def __next__(self):
        node = next(self.base_itr)
        try:
            return create(node)
        except DrbFactoryException:
            return node


def resolve_children(func):
    def inner(ref):
        if isinstance(ref, DrbNode) and func.__name__ == 'children':
            return DrbNodeList(func(ref))
        raise TypeError('@resolve_children decorator must be only apply on '
                        'children methods of a DrbNode')
    return inner


def resolve(source: Union[str, DrbNode]) -> Tuple[ItemClass, DrbNode]:
    return _DrbFactoryResolver().resolve(source)


def create(source: Union[str, DrbNode]) -> DrbNode:
    return _DrbFactoryResolver().create(source)
