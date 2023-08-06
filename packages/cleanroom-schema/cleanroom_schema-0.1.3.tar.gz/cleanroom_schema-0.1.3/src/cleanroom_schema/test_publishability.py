from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from pkg_resources import resource_string

schema_contents = resource_string(__name__, 'schema/cleanroom_schema.yaml').decode('utf-8')


def print_nt():
    schema_view = SchemaView(schema_contents)

    nt = schema_view.get_class("NamedThing")

    print(yaml_dumper.dumps(nt))
