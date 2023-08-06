from __future__ import annotations

import abc
from typing import List, Dict, Optional, Tuple, Any, Callable
from .item import DrbItem
from .path import ParsedPath
from .events import EventManager


class DrbNode(DrbItem, abc.ABC):
    """
    Generic node interface. This interface represents a single node of a tree
    of data. Any node can have no, one or several children. This interface
    provides the primarily operations to browse an entire data structure. All
    implementations of the "Data Request Broker" shall be able to produce such
    nodes.
    """

    def __init__(self):
        super(DrbNode, self).__init__()
        self.__namespace_aware = None
        self.__events = EventManager()

    @property
    @abc.abstractmethod
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """
        Returns attributes of the current node. This operation all attributes
        owned by the current node.
        Attributes are represented by a dict with as key the tuple
        (name, namespace_uri) of the attribute and as value the value of this
        attribute.

        Returns:
            dict: A dict of attributes of the current node
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        """
        Returns the value of the corresponding attribute, following its name,
        and its namespace URI for the matching.

        Parameters:
            name (str): attribute name to match
            namespace_uri (str, optional): attribute namespace URI to match
        Returns:
            Any: the associated value of the matched attribute
        :Raises:
            DrbException: if the given name and namespace URI not math any
            attribute of the current node
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def parent(self) -> Optional[DrbNode]:
        """
        The parent of this node. Returns a reference to the parent node of the
        current node according to the current implementation. Most of the
        nodes have a parent except root nodes or if they have just been
        removed, etc. If the node has no parent the operation returns None.

        Returns:
            DrbNode: The parent of this node or ``None``.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def path(self) -> ParsedPath:
        """ The full path of this node.
        The path is the complete location of this node. The supported format
        is URI and apache common VFS.

        Returns:
            ParsedPath: A ``ParsedPath`` representing the node location
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def children(self) -> List[DrbNode]:
        """
        The list of children of the current node. Returns a list of
        references to the children of the current node. The current node may
        have no child and the operation returns therefore a null reference.

        Returns:
            list: The list of children
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_child(self, name: str = None, namespace: str = None) -> bool:
        """
        Checks if current node has a child following name and namespace
        criteria. If `name` and `namespace` are not specified it will check if
        the current node has at least a child.

        Returns:
            bool: ``True`` if current node has a child following name and
            namespace criteria, otherwise ``False``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_impl(self, impl: type) -> bool:
        """
        Tests if a specific interface can be provided. These operation tests
        with a minimum of time and memory consumption if the current
        implementation can provide a specific interface. It is important to
        consider that ``has_impl`` provides information about the ability to
        provide such interface in general cases but not focused on the current
        instance. It may therefore be impossible to get a specific
        implementation from a node whereas ``has_impl`` operation returns true.

        Parameters:
            impl (type): the implementation type expected
        Returns:
            bool: True if an implementation of the interface can be provided
        and False otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_impl(self, impl: type, **kwargs) -> Any:
        """
        This operation returns a reference to an object implementing a
        specific interface. This method authorizes a specific and/or direct
        API instead of using the DrbNode interface. The provided object is
        independent of this node and shall be released/closed by the caller
        when interface requires such finally operations.

        Parameters:
            impl (type): the implementation type expected
        Return:
            Any: the expected implementation.
        Raises:
            DrbNotImplementedException: if `impl` is not supported by the
                                        current node
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """
        Releases all resources attached to the current node.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        """
        Returns the children number of the current node.

        Returns:
            int: children number
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, item):
        """
        Implements the item in bracket operator to access this node children.
        The brace operator is used to access the children node, according to
        the following supported items:

        * ``int``: the item-th children node will be returned

        * ``slice``: children node of the requested slice will be returned

        * ``str``: the first child node with the item as name is retrieved
          from its children

        * ``tuple``: the following tuple must be supported per each node
          implementation:

            * (name: ``str``, namespace: ``str``): retrieves first child by is
              name and namespace_uri.

            * (name: ``str``, item: ``int`` | ``slice``): retrieves a child or
              a children interval having a specific name.

            * (name: ``str``, namespace: ``str``, item: ``int`` | ``slice``):
              retrieves a child or a children interval having a specific name
              and namespace_uri

        * ``Predicate``: children nodes matching this predicate are
          returned, may return an empty list

        Returns:
            DrbNode or List[DrbNode]: expected child node(s) according to the
            case
        Raises:
            DrbException: if no child is found, except for ``Predicate`` case
                          where an empty may return.
        Examples:

        .. code-block:: python

            # get first child
            child = node[0]
            # get last child
            child = node[-1]
            # get children interval (last 3 children)
            children = node[-3:-1]

            # first child by its name
            child = node['child_name'] # == node['child_name', 0]
            # third child named name_child
            child = node['child_name', 2]
            # children interval of child named child_name (first 2 children)
            children = node['child_name', :2]

            # first child named child_name and having as namespace ns
            child = node['child_name', 'ns']
            # last child named child_name and having as namespace ns
            child = node['child_name', 'ns', -1]
            # all children named child_name and having as namespace ns
            child = node['child_name', 'ns', :]

            # get children using a Predicate
            children = node[MyPredicate()]
        """
        raise NotImplementedError

    @property
    def namespace_aware(self) -> bool:
        """
        Property flag to decide about behaviour during browsing of its
        children. This flag is transitive from a parent to its child until the
        first definition using this property setter. Default value ``False``

        * ``True``: take into account children namespace during browsing
        * ``False``: does not take into account children namespace during
          browsing

        Returns:
            bool: ``True`` if node take care of namespace during browsing of
        its children, otherwise ``False``
        """
        if self.__namespace_aware is None:
            if self.parent is None:
                return False
            return self.parent.namespace_aware
        return self.__namespace_aware

    @namespace_aware.setter
    def namespace_aware(self, value: Optional[bool]) -> None:
        """
        Update browsing behaviour. see :func:`~node.DrbNode.namespace_aware`
        Parameters:
            value (bool): new value of ``namespace_aware`` or None to retrieve
                          parent behaviour
        Raises:
            ValueError: if the given value is not a boolean
        """
        if value is not None and not isinstance(value, bool):
            raise ValueError('Only a value boolean is expected here !')
        self.__namespace_aware = value

    @property
    def _event_manager(self) -> EventManager:
        """
        Retrieves the EventManager associated to this node.

        Returns:
             EventManager: the event manager attached to this node

        """
        return self.__events

    def register(self, event_type: str, callback: Callable):
        """
        Registers a new callback on a specific event type.

        Parameters:
            event_type (str): target event type
            callback (Callable): the callback to register
        """
        self.__events.register(event_type, callback)

    def unregister(self, event_type: str, callback: Callable):
        """
        Unregisters a new callback on a specific event type.

        Parameters:
            event_type (str): target event type
            callback (Callable): the callback to unregister
        """
        self.__events.unregister(event_type, callback)

    def __hash__(self):
        return hash(self.path.name)

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            return self.has_child(item)
        if isinstance(item, tuple) and len(item) == 2:
            return self.has_child(*item)
        return False
