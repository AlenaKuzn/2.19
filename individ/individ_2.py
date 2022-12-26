#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import pathlib
import colorama
from colorama import Fore


def tree(directory):
    print(Fore.BLUE + f'>>> {directory}')
    for path in sorted(directory.rglob('*')):
        print(Fore.YELLOW + f' >> {path.name}')
        for new_path in sorted(directory.joinpath(path).glob('*')):
            print(Fore.GREEN + f' > {new_path.name}')


def main(command_line=None):
    colorama.init()
    current = pathlib.Path.cwd()
    file_parser = argparse.ArgumentParser(add_help=False)

    # Создаем основной парсер командной строки
    parser = argparse.ArgumentParser("tree")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Субпарсер для создания папок
    create = subparsers.add_parser(
        "mkfl",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для удаления папок
    create = subparsers.add_parser(
        "rmfl",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )

    args = parser.parse_args(command_line)

    if args.command == 'mkfl':
        directory_path = current / args.filename
        directory_path.mkdir()
        tree(current)
    elif args.command == "rmfl":
        directory_path = current / args.filename
        directory_path.rmdir()
        tree(current)
    else:
        tree(current)


if __name__ == "__main__":
    main()
