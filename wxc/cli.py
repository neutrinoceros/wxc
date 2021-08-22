import sys
from argparse import ArgumentParser
from typing import List, Optional

from wxc.api import get_full_data, get_obj, is_builtin, is_builtin_func

builtin_print = print
try:
    from rich import print
except ImportError:
    pass


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

    try:
        get_obj(args.name)
    except ImportError:
        print(
            f"Error: did not resolve any data for {args.name!r}",
            file=sys.stderr,
        )
        return 1
    except AttributeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        data = get_full_data(args.name)
    except TypeError:
        msg = "Error: failed to locate source data."
        if is_builtin(args.name):
            msg += f" {args.name!r} is a builtin object."
        elif is_builtin_func(args.name):
            msg += f" {args.name!r} is a builtin function."
        print(
            msg,
            file=sys.stderr,
        )
        return 1

    if args.full:
        data["name"] = args.name
        ver = f"version = {data.pop('version')}"
        print("\n".join(f"{k} = {v}" for k, v in data.items()))
        builtin_print(ver)
        return 0

    if args.version:
        if not data["version"]:
            print(
                f"Error: did not find version metadata for {args.name!r}",
                file=sys.stderr,
            )
            return 1
        builtin_print(data["version"])
        return 0

    if not data["source"]:
        print(
            f"Error: did not resolve source file for {args.name!r}",
            file=sys.stderr,
        )
        return 1
    print(data["source"])
    return 0
