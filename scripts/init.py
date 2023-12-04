import argparse
import os
import pathlib
import shutil

from aoc import lib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)

    args = parser.parse_args()

    path = lib.day_dir(args.day) / "__init__.py"
    if path.exists():
        raise ValueError(
            f"not overwriting {path.relative_to(os.getcwd(), walk_up=True)}"
        )

    path.parent.mkdir(exist_ok=True)
    shutil.copy(pathlib.Path(__file__).parent / "__init__.py.tmpl", path)

    print(f"created {path.relative_to(os.getcwd(), walk_up=True)}")


if __name__ == "__main__":
    main()
