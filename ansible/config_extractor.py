import os
from subprocess import PIPE, run
import sys
import yaml
from collections import defaultdict

REMOVE_KEYS = [
    "annotations", "managedFields", "status", "selfLink", "generation",
    "resourceVersion"
]
NONE_KEYS = ["creationTimestamp"]
ANSIBLE_JINJA_REMAP = {}
DEST_PATH = "roles/ocp4/templates/"


def fetch_from_ocp4(namespace, config_type, config_name, o_format="yaml"):
    cmd = [
        "oc",
        "-n",
        namespace,
        "get",
        config_type,
        config_name,
        "-o",
        o_format,
    ]
    output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True).stdout
    return output


def format_template(data):
    yaml_data = yaml.safe_load(data)
    rec_clean_dict(yaml_data)
    return yaml_data


def rec_clean_dict(data_dict):
    # simple, does not account for keys occuring at differing levels in dict
    for k in list(data_dict.keys()):
        if k in ANSIBLE_JINJA_REMAP.keys():
            data_dict[k] = ANSIBLE_JINJA_REMAP[k]
        elif k in REMOVE_KEYS:
            data_dict.pop(k)
        elif k in NONE_KEYS:
            data_dict[k] = None
        elif isinstance(data_dict[k], dict):
            rec_clean_dict(data_dict[k])
        else:
            pass


def main():
    config_data = ""
    arguments = sys.argv[1:]
    if len(arguments) < 3:
        print(
            "Usage: ./config_extractor <namespace> deploymentconfigs|buildconfigs <config_name>"
        )
        exit(1)

    ns = arguments[0]
    config_type = arguments[1]
    config_name = arguments[2]
    config_data = fetch_from_ocp4(ns, config_type, config_name)
    template = format_template(config_data)
    with open(f'{DEST_PATH}{config_name}.j2', 'w') as fh:
        yaml.dump(template, fh)


if __name__ == "__main__":
    main()