import json
import sys
from argparse import ArgumentParser
from typing import List, Optional

from .api import Scope


def main(argv: Optional[List[str]] = None) -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "scope_name",
        help="target Python scope (package.module.submodule.class.method)",
    )
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-v", "--version", action="store_true", help="print module version"
    )
    command_group.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="print a full report in a human readable fashion",
    )
    command_group.add_argument(
        "--json",
        action="store_true",
        help="print a full json report",
    )
    args = parser.parse_args(argv)

    data = Scope(args.scope_name)
    if not data["is_available"]:
        print("unknown", file=sys.stderr)
        return 1

    if args.json:
        ret = json.dumps(data, indent=2)
    elif args.info:
        ret = str(data)
    else:
        try:
            if args.version:
                ret = data["version"]
            else:
                ret = data["path"]
                if "line" in data and not data["is_module"]:
                    ret = ":".join([ret, str(data["line"])])
        except KeyError:
            print("unknown", file=sys.stderr)
            return 1

    print(ret)
    return 0
