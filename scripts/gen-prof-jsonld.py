import yaml
import json
from pprint import pprint


PROF_YAML = "target/prof/DiagramLayout-AP-2.1.yml"
PROF_JSON = "target/prof/DiagramLayout-AP-2.1.jsonld"

PROF_CONTEXT_JSON = "target/prof/context.jsonld"


if __name__ == "__main__":
    with open(PROF_CONTEXT_JSON) as ctx, open(PROF_YAML) as data:
        prof_dict = yaml.safe_load(data)
        prof_dict["@context"] = json.load(ctx)

    with open(PROF_JSON, "w") as g:
        json.dump(prof_dict, g, indent=2)

    # NOTE: https://json-ld.org/playground/next/