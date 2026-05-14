# from linkml_runtime.utils.schemaview import SchemaView
# sv = SchemaView("target/linkml/diagram-layout.linkml.yml")
# print(sv.schema.extensions)

import json
import yaml

DIAGRAM_LAYOUT_FILE = "target/linkml/diagram-layout.linkml.yml"

with open(DIAGRAM_LAYOUT_FILE) as f:
    schema = yaml.safe_load(f)


print(schema)