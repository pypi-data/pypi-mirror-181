import os

import yaml
from drb.core import DrbFactory, DrbNode, ParsedPath

from io import BufferedIOBase, BytesIO, RawIOBase
from typing import Union, Optional, Any, Dict, Tuple, IO, List

from drb.exceptions.core import DrbNotImplementationException, DrbException
from drb.nodes.abstract_node import AbstractNode


class YamlNode(AbstractNode):
    """
    This class represents a single node of a tree
    of data. When a node has one or several children he has no value.

    Parameters:
            path (str): The path to the yaml file.
            parent (DrbNode): The parent of this node (default: None).
            data : The yaml data (default: None).
    """

    supported_impl = [dict, str]

    def __init__(self, path: str,
                 parent: DrbNode = None, data=None):
        super().__init__()
        if data is not None:
            self._data = data
            self._name = os.path.basename(path)
            self._path = ParsedPath(path)
        else:
            with open(path) as yamlFile:
                data = list(yaml.safe_load_all(yamlFile))
                if len(data) == 1:
                    self._data = data[0]
                else:
                    self._data = data
                yamlFile.close()
            self._name = os.path.basename(path)
            self._path = ParsedPath(path)

        self._parent = parent
        self._children = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return self._data

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'No attribute ({name}:{namespace_uri}) found!')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        return self._path

    def has_impl(self, impl: type) -> bool:
        return impl in self.supported_impl

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            if impl == dict:
                return self._data
            else:
                return yaml.dump(self._data)

        raise DrbNotImplementationException(
            f"YamlNode doesn't implement {impl}")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace:
            return False
        if name:
            if isinstance(self._data, dict):
                for e in self._data.keys():
                    if e == name:
                        return True
                    return False
            if isinstance(self._data, list):
                for e in self._data:
                    if e == name:
                        return True
                    return False
        return isinstance(self._data, dict) or isinstance(self._data, list)

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if self.has_child():
                if isinstance(self._data, list):
                    self._children = [
                        YamlNode(path=self.path.path,
                                 parent=self,
                                 data=e)
                        for e in self._data]
                else:
                    for e in self._data.keys():
                        if isinstance(self._data[e], list):
                            for x in self._data[e]:
                                self._children.append(
                                    YamlNode(path=os.path.join(
                                        self.path.path, e),
                                        parent=self,
                                        data=x)
                                )
                        else:
                            self._children.append(
                                YamlNode(path=os.path.join(self.path.path, e),
                                         parent=self,
                                         data=self._data[e])
                            )
            else:
                self._children = []
        return self._children

    def close(self) -> None:
        pass


class YamlBaseNode(AbstractNode):
    """
        This class represents a single node of a tree
        of data. When the data came from another implementation.

        Parameters:
                node (DrbNode): The node where the yaml data came from.
                source (Union[BufferedIOBase, RawIOBase, IO]): The yaml data.
        """

    def __init__(self,
                 node: DrbNode,
                 source: Union[BufferedIOBase, RawIOBase, IO]):
        super().__init__()
        self.base_node = node
        self.source = source
        yaml_root = yaml.safe_load(source)
        self.yaml_node = YamlNode(node.path.path, parent=self, data=yaml_root)

    @property
    def name(self) -> str:
        return self.base_node.name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self.base_node.namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return self.base_node.value

    @property
    def path(self) -> ParsedPath:
        return self.base_node.path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.base_node.parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self.base_node.attributes

    @property
    def children(self) -> List[DrbNode]:
        return [self.yaml_node]

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name and self.yaml_node.name == name:
            return True
        elif namespace:
            return False
        return True

    def get_attribute(self, name: str) -> Any:
        return self.base_node.get_attribute(name)

    def has_impl(self, impl: type) -> bool:
        return self.base_node.has_impl(impl)

    def get_impl(self, impl: type, **kwargs) -> Any:
        return self.base_node.get_impl(impl)

    def close(self) -> None:
        if self.source:
            self.source.close()
        self.base_node.close()


class YamlNodeFactory(DrbFactory):
    """
    The YamlNodeFactory class allow us to build drb nodes according
     to the form of the yaml data you want to read.
    After this class is created you can call the _create method
     with the drb node created from the
    path of the Yaml file you want to read
    """

    def _create(self, node: Union[DrbNode, str]) -> DrbNode:
        if isinstance(node, YamlNode) or isinstance(node, YamlBaseNode):
            return node
        if isinstance(node, DrbNode):
            if node.has_impl(BufferedIOBase):
                return YamlBaseNode(node, node.get_impl(BufferedIOBase))
            else:
                return YamlBaseNode(node, node.get_impl(BytesIO))
        return YamlNode(node)
