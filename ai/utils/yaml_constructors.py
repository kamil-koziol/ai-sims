import uuid
import yaml


def register_uuid_yaml_constructor():
    # Custom constructor for UUID objects
    def uuid_constructor(loader, node):
        value = loader.construct_mapping(node)
        return uuid.UUID(int=value['int'])

    # Register the constructor for UUID objects
    yaml.add_constructor('tag:yaml.org,2002:python/object:uuid.UUID', uuid_constructor)
