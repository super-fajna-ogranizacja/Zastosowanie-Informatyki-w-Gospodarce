import argparse
import json

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type: ignore


def main(args):
    projects = {}

    for path in args.input:
        with open(path) as fd:
            projects |= yaml.load(fd, Loader=Loader)

    js_src = "export const projects = "
    js_src += json.dumps(projects, indent=2)
    js_src += ";\n"

    with open(args.output, "w") as fd:
        fd.write(js_src)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="path to generated projects.js")
    parser.add_argument("input", nargs="+", help="input yaml files")
    args = parser.parse_args()

    main(args)
