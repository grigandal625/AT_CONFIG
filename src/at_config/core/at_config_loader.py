from at_config.core.at_config_handler import ATComponentConfig
from at_config.core.at_config_item import RawDataConfigItem, LocalFileConfigItem
from schema import Schema, Or, And, Use, Optional


RAW_DATA_ITEM_SCHEMA = lambda parameter: Or(
    And(
        Schema({
            Optional('item_type'): 'raw_data',
            'data': Or(str, int, float, bool, dict, list)
        }, ignore_extra_keys=True),
        Use(lambda value: RawDataConfigItem(parameter, **value))
    ),
    And(
        Or(str, int, float, bool, dict, list),
        Use(lambda value: RawDataConfigItem(parameter, data=value))
    )
)

LOCAL_FILE_ITEM_SCHEMA = lambda parameter: And(
    Schema({
        Optional('item_type'): 'local_file',
        'path': str
    }, ignore_extra_keys=True),
    Use(lambda value: LocalFileConfigItem.build(parameter, path=value.get('path')))
)

AT_CONFIG_ITEM_SCHEMA = lambda parameter: Or(
    LOCAL_FILE_ITEM_SCHEMA(parameter),
    RAW_DATA_ITEM_SCHEMA(parameter)
)

COMPONENT_CONFIG_SCHEMA = And(
    Schema({
        str: Or(str, int, float, bool, dict, list)
    }),
    Use(lambda component: ATComponentConfig({
        parameter: AT_CONFIG_ITEM_SCHEMA(parameter).validate(data)
        for parameter, data in component.items()
    }))
)

CONFIG_SCHEMA = And(
    Schema({
        str: dict
    }),
    Use(lambda config: {
        component_name: COMPONENT_CONFIG_SCHEMA.validate(component_data)
        for component_name, component_data in config.items()
    })
)

def load_config(data):
    return CONFIG_SCHEMA.validate(data)

def load_component_config(data):
    return COMPONENT_CONFIG_SCHEMA.validate(data)

