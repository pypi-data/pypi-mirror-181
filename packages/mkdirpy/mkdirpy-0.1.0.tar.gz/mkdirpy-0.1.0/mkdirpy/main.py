import argparse
import sys
from pathlib import Path


def run() -> None:
    parser = argparse.ArgumentParser(
        prog="mkdirpy", description="mkdir and generate __init__.py files"
    )
    parser.add_argument("directory_name", type=Path, help="")
    parser.add_argument(
        "-p", action="store_true", help="create parent directories (similar to mkdir -p)"
    )
    parser.add_argument(
        "-v", action="store_true", help="be verbose when creating directories"
    )
    namespace = parser.parse_args(sys.argv[1:])

    try:
        _create_dir(namespace.directory_name, namespace.p, namespace.v)
    except FileNotFoundError as exc:
        raise SystemExit(exc)


def _create_dir(path: Path, parents: bool, verbose: bool) -> None:
    if path.exists():
        raise RuntimeError
    try:
        path.mkdir()
    except FileNotFoundError:
        if not parents:
            raise FileNotFoundError(f"mkdirpy: {path.parent}: No such file or directory")
        _create_dir(path.parent, parents, verbose)
        _create_dir(path, parents, verbose)
    else:
        init_path = path.joinpath("__init__.py")
        init_path.touch()
        if verbose:
            print(path)
            print(init_path)
