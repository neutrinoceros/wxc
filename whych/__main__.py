from argparse import ArgumentParser

from .api import whych


def cli() -> None:
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
        query = "info"
        joiner = "\n" * 2
    elif args.version:
        query = "version"
    else:
        query = "path"
    res = whych(module_name=args.module, query=query)
    if isinstance(res, list):
        res = joiner.join(res)
    print(res)


if __name__ == "__main__":
    cli()
