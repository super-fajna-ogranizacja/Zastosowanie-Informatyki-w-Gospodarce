import argparse
import json
from pathlib import Path

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type: ignore


def main(args):
    output_dir = Path(args.directory)
    projects = {}

    for path in args.input:
        with open(path) as fd:
            projects |= yaml.load(fd, Loader=Loader)

    js_src = "export const projects = "
    js_src += json.dumps(projects, indent=2)
    js_src += ";\n"

    with open(output_dir / "projects.js", "w") as fd:
        fd.write(js_src)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="generated HTML directory")
    parser.add_argument("input", nargs="+", help="input yaml files")
    args = parser.parse_args()

    main(args)
