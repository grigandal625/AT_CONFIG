import io
import os
import json
from xml.etree.ElementTree import Element, fromstring
import yaml
from typing import Union

class ATConfigItem:
    parameter: str
    data: Union[dict, str, Element]

    def __init__(self, parameter: str, *args, **kwargs) -> None:
        self.parameter = parameter
    
    @property
    def item_type(self):
        return 'abstract'

    @property
    def __dict__(self):
        return {
            'parameter': self.parameter,
            'item_type': self.item_type
        }
    

class RawDataConfigItem(ATConfigItem):
    data: dict

    def __init__(self, parameter: str, data: dict, *args, **kwargs) -> None:
        super().__init__(parameter, *args, **kwargs)
        self.data = data

    @property
    def item_type(self):
        return 'raw_data'

    @property
    def __dict__(self):
        return {
            'data': self.data,
            **super().__dict__
        }


class FileConfigItem(ATConfigItem):

    @property
    def item_type(self):
        return 'file'

    def get_readable(self, mode: str = 'rb') -> io.TextIOBase:
        raise NotImplementedError()
    
    @property
    def content(self) -> bytes:
        return self.get_readable('rb').read()
    

class LocalFileConfigItem(FileConfigItem):
    path: str

    def __init__(self, parameter: str, path: str, *args, **kwargs) -> None:
        super().__init__(parameter, *args, **kwargs)
        self.path = path

    @property
    def item_type(self):
        return 'local_file'
    
    def get_readable(self, mode: str = 'rb') -> io.TextIOBase:
        return open(self.path, mode)
    
    @property
    def __dict__(self):
        return {
            'path': self.path,
            **super().__dict__
        }

    @property
    def ext(self) -> str:
        return os.path.splitext(self.path)[1]
    
    @staticmethod
    def build(parameter: str, path: str, *args, **kwargs) -> 'LocalFileConfigItem':
        try:
            ext_to_class = {
                '.json': JSONFileItem,
                '.yaml': YAMLFileItem,
                '.xml': XMLFileItem
            }
            file_ext = os.path.splitext(path)[1]
            if file_ext in ext_to_class:
                result = ext_to_class[file_ext](parameter, path, *args, **kwargs)
                data = result.data
                return result
        except:
            return RawFileItem(parameter, path, *args, **kwargs)
        return RawFileItem(parameter, path, *args, **kwargs)


class JSONFileItemMixin:

    @property
    def data(self) -> dict:
        return json.load(self.get_readable())
    

class YAMLFileItemMixin:

    @property
    def data(self) -> dict:
        return yaml.safe_load(self.get_readable())
    

class XMLFileItemMixin:

    @property
    def data(self) -> Element:
        return fromstring(self.get_readable().read())
    

class RawFileItemMixin:
    
    @property
    def data(self) -> str:
        return self.content.decode()


class JSONFileItem(LocalFileConfigItem, JSONFileItemMixin):
    pass


class YAMLFileItem(LocalFileConfigItem, YAMLFileItemMixin):
    pass


class XMLFileItem(LocalFileConfigItem, XMLFileItemMixin):
    pass


class RawFileItem(LocalFileConfigItem, RawFileItemMixin):
    pass
