import sys
from argparse import ArgumentParser
from typing import List, Optional

from wxc.api import get_full_data


def main(argv: Optional[List[str]] = None) -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "name",
        help="target Python scope (package.module.submodule.class.method)",
    )
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-v", "--version", action="store_true", help="print module version"
    )
    command_group.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="print a full report",
    )
    args = parser.parse_args(argv)

    data = get_full_data(args.name)

    if not any(list(data.values())):
        print(
            f"Error: did not resolve any data for '{args.name}'",
            file=sys.stderr,
        )
        return 1

    if args.full:
        data["name"] = args.name
        print("\n".join(f"{k} = {v}" for k, v in data.items()))
        return 0

    if args.version:
        if not data["version"]:
            print(
                f"Error: did not find version metadata for '{args.name}'",
                file=sys.stderr,
            )
            return 1
        print(data["version"])
        return 0

    if not data["source"]:
        print(f"Error: did not manage to find source file for '{args.name}'")
        return 1
    print(data["source"])
    return 0
