import yaml
import json
from pprint import pprint



if __name__ == "__main__":
    prof_yaml = "target/prof/ttl/DiagramLayout-CIM-AP.yml"
    prof_json = "target/prof/ttl/DiagramLayout-CIM-AP.jsonld"

    with open(prof_yaml) as f:
        prof_dict = yaml.safe_load(f)
    
    with open(prof_json, "w") as g:
        json.dump(prof_dict, g, indent=2)