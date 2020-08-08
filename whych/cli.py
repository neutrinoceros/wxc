from argparse import ArgumentParser

from .api import query


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("module", nargs="+", help="target Python module(s)")
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-v", "--version", action="store_true", help="print module version"
    )
    command_group.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="print module name, path, and version",
    )
    args = parser.parse_args()
    joiner = "\n"
    if args.info:
        field = "info"
        joiner = "\n" * 2
    elif args.version:
        field = "version"
    else:
        field = "path_and_line"
    res = query(importable_names=args.module, field=field, fill_value="unknown")

    if isinstance(res, list):
        res = joiner.join(res)
    print(res)
