from __future__ import annotations

import sys
from argparse import ArgumentParser

from wxc.api import (
    get_full_data,
    get_obj,
    get_sourceline,
    get_suggestions,
    is_builtin,
    is_builtin_func,
)

builtin_print = print


def print_err(msg):
    from rich import print

    print(f"[bold white on red]ERROR[/] {msg}", file=sys.stderr)


class ScopeName(str):
    def __new__(cls, content):
        return str.__new__(cls, content.replace("-", "_"))


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "name",
        type=ScopeName,
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
    parser.add_argument(
        "-s", "--source", action="store_true", help="print the source code"
    )
    parser.add_argument(
        "--lines",
        dest="show_lines",
        action="store_true",
        help="show source lines",
    )
    args = parser.parse_args(argv)

    if "." not in args.name:
        # this is a simple module request
        # let's try to get the result without actually importing it first
        if args.version:
            import importlib.metadata as md

            try:
                version = md.version(args.name)
            except md.PackageNotFoundError:
                pass  # resort to expensive search
            else:
                builtin_print(version)
                return 0
        elif args.full:
            # quick lookup not possible (or at least, not implemented)
            pass
        else:
            from importlib.util import find_spec

            spec = find_spec(args.name)
            if spec is None:
                pass  # resort to expensive search
            else:
                from rich import print

                print(spec.origin)
                return 0

    from rich.progress import Progress, SpinnerColumn, TextColumn

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("[bold]Resolving source")
        try:
            obj = get_obj(args.name)
        except ImportError:
            package_name = args.name.partition(".")[0]
            msg = f"no installed package with name {package_name!r}"
            if sys.version_info >= (3, 10):
                # the standard library in Python >= 3.10 is the only subset of available packages
                # for which we have a computationally cheap way to retrieve a list.
                suggestions = get_suggestions(
                    sys.builtin_module_names, package_name, max_dist=2
                )
                if len(suggestions) == 1:
                    msg += f". Did you mean {suggestions[0]!r} ?"
            else:
                pass
            progress.stop()
            print_err(msg)
            return 1
        except AttributeError as exc:
            progress.stop()
            print_err(exc)
            return 1

    try:
        data = get_full_data(args.name)
    except TypeError:
        msg = "failed to locate source data."
        if is_builtin(args.name):
            msg += f" {args.name!r} is a builtin object."
        elif is_builtin_func(args.name):
            msg += f" {args.name!r} is a C-compiled function."
        print_err(msg)
        return 1

    if args.full:
        from rich import print

        data["name"] = args.name
        ver = f"version = {data.pop('version', 'unknown')}"
        print("\n".join(f"{k} = {v}" for k, v in data.items()))
        builtin_print(ver)
        return 0

    if args.version:
        if not data["version"]:
            print_err(f"did not find version metadata for {args.name!r}")
            return 1
        builtin_print(data["version"])
        return 0

    if "source" not in data:
        print_err(f"did not resolve source file for {args.name!r}")
        return 1

    if args.source:
        import inspect

        from rich.syntax import Syntax

        try:
            code = inspect.getsource(obj)
        except OSError as exc:
            # inspect.getsource _can_ be the first failing call so we wrap its
            # error because it's inline with wxc's own error messages and
            # there's probably not much else we can do about it.
            print_err(exc)
            return 1

        from rich import print

        print(
            Syntax(
                code,
                "python",
                theme="monokai",
                line_numbers=args.show_lines,
                start_line=get_sourceline(obj),
                background_color="default",
            )
        )

    from rich import print

    print(data["source"])

    return 0
