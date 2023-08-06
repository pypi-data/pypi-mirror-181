from drb.core.path import ParsedPath
from drb.core.node import DrbNode
from drb.core.factory import DrbFactory
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbException, DrbNotImplementationException
from drb.exceptions.file import DrbFileNodeFactoryException
from urllib.parse import urlparse
from typing import Any, List, Dict, Optional, Tuple

import io
import os
import platform
import pathlib
import re
import stat
import enum
import drb.topics.resolver as resolver


class DrbFileAttributeNames(enum.Enum):
    """
    This Enum class represent different attributes of a file:
        - DIRECTORY a boolean to tell if the file is a directory.
        - SIZE total size, in bytes.
        - MODIFIED the time of last modification.
        - READABLE a boolean, to check if the file is readable.
        - WRITABLE a boolean, to check if the file is writable.
        - HIDDEN a boolean, to check if the file is hidden.
    """
    DIRECTORY = 'directory'
    SIZE = 'size'
    MODIFIED = 'modified'
    READABLE = 'readable'
    WRITABLE = 'writable'
    HIDDEN = 'hidden'


def is_hidden(path: str) -> bool:
    """
    Check if the associated file of the given path is hidden.
    :param path: file path to check
    :return: True if the file of the corresponding path is hidden
    :rtype: bool
    """
    # os_type = 'Linux' | 'Windows' | 'Java'
    os_type = platform.uname()[0]
    if os_type == 'Windows':
        return bool(os.stat(path).st_file_attributes &
                    stat.FILE_ATTRIBUTE_HIDDEN)
    return os.path.basename(path).startswith('.')


def impl_stream(path: str) -> io.FileIO:
    return io.FileIO(path, 'r+')


def impl_buffered_stream(path: str) -> io.BufferedReader:
    return io.BufferedReader(impl_stream(path))


class DrbFileNode(AbstractNode):
    """
    Parameters:
        path (Union[str, ParsedPath]): The path of the file
                                       to read with this node.
        parent (DrbNode): The parent of this node (default: None)
    """
    supported_impl = {
        io.RawIOBase: impl_stream,
        io.FileIO: impl_stream,
        io.BufferedIOBase: impl_buffered_stream,
        io.BufferedReader: impl_buffered_stream,
    }

    def __init__(self, path, parent: DrbNode = None):
        super().__init__()
        if isinstance(path, ParsedPath):
            self._path = path
        else:
            if platform.uname()[0] == 'Windows':
                path = pathlib.Path(path).as_posix()
            self._path = ParsedPath(os.path.abspath(path))
        self._parent: DrbNode = parent
        self._attributes: Dict[Tuple[str, str], Any] = None
        self._children: List[DrbNode] = None

    @property
    def name(self) -> str:
        """
        Return the name of the file.
        This name doesn't contain the path of the file.

        Returns:
            str: the file name
        """
        return self._path.filename

    @property
    def namespace_uri(self) -> Optional[str]:
        """
        Not use in this implementation.

        Returns:
            None
        """
        return None

    @property
    def value(self) -> Optional[Any]:
        """
        Not use in this implementation.

        Returns:
            None
        """
        return None

    @property
    def parent(self) -> Optional[DrbNode]:
        """
        Return the parent of this node if he has one otherwise None.
        In this implementation the parent should always be another DrbFileNode.

        Returns:
            DrbNode: The parent of this node or None.
        """
        return self._parent

    @property
    def path(self) -> ParsedPath:
        """
        Returns the path of the file.
        The supported format is URI and apache common VFS.

        Returns:
            ParsedPath: The path of the file.
        """
        return self._path

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            file_stat = os.stat(self.path.path)
            name = DrbFileAttributeNames.DIRECTORY.value
            self._attributes[(name, None)] = os.path.isdir(self.path.path)

            name = DrbFileAttributeNames.SIZE.value
            self._attributes[(name, None)] = file_stat.st_size

            name = DrbFileAttributeNames.MODIFIED.value
            self._attributes[(name, None)] = file_stat.st_mtime

            name = DrbFileAttributeNames.READABLE.value
            self._attributes[(name, None)] = os.access(self.path.path, os.R_OK)

            name = DrbFileAttributeNames.WRITABLE.value
            self._attributes[(name, None)] = os.access(self.path.path, os.W_OK)

            name = DrbFileAttributeNames.HIDDEN.value
            self._attributes[(name, None)] = is_hidden(self.path.path)

        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    @resolver.resolve_children
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if os.path.isdir(self.path.path):
                sorted_child_names = sorted(os.listdir(self.path.path))
                for filename in sorted_child_names:
                    child = DrbFileNode(self.path / filename, parent=self)
                    self._children.append(child)
        return self._children

    def has_impl(self, impl: type) -> bool:
        if impl in DrbFileNode.supported_impl.keys():
            return not self.get_attribute(
                DrbFileAttributeNames.DIRECTORY.value)

    def get_impl(self, impl: type, **kwargs) -> Any:
        try:
            return DrbFileNode.supported_impl[impl](self.path.path)
        except KeyError:
            raise DrbNotImplementationException(
                f'no {impl} implementation found')

    def close(self) -> None:
        """
        Not use in this implementation.

        Returns:
            None
        """
        pass


class DrbFileFactory(DrbFactory):

    @staticmethod
    def _create_from_uri_of_node(node: DrbNode):
        uri = node.path.name
        parsed_uri = urlparse(uri)
        if (platform.uname()[0] == "Windows"
                and re.match(r"^/[a-zA-Z]:", parsed_uri.path)):
            path = parsed_uri.path[:1].replace('%20', ' ')
        else:
            path = parsed_uri.path
        if os.path.exists(path):
            return DrbFileNode(path, node)
        raise DrbFileNodeFactoryException(f'File not found: {path}')

    def _create(self, node: DrbNode) -> DrbNode:
        return self._create_from_uri_of_node(node)
