#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib


def get_reys(re, pynkt, numb, samolet):
    """
    Запросить данные о рейсе.
    """
    re.append(
        {
            'pynkt': pynkt,
            'numb': numb,
            'samolet': samolet,
        }
    )
    return re


def display_reys(re):
    """
    Отобразить список рейсов.
    """
    # Проверить, что список работников не пуст.
    if re:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,

            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип"
            )
        )
        print(line)

        # Вывести данные о всех рейсах.
        for idx, rey in enumerate(re, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    rey.get('pynkt', ''),
                    rey.get('numb', ''),
                    rey.get('samolet', 0)
                )
            )
            print(line)

    else:
        print("Список рейсов пуст.")


def select_reys(re, pynkt_pr):
    """
    Выбрать рейс с нужным пунктом.
    """
    # Сформировать список работников.
    result = []
    for employee in re:
        if employee.get('pynkt') == pynkt_pr:
            result.append(employee)
        else:
            print("Нет рейсов в указаный пункт")

    # Возвратить список выбранных работников.
    return result


def save_reys(file_name, staff):
    """
    Сохранить все рейсы в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))


def load_reys(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
        return json.load(fin)


def main(command_line=None):
    """
    Главная функция программы.
    """
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("reys")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления рейса.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new reys"
    )
    add.add_argument(
        "-p",
        "--pynkt",
        action="store",
        required=True,
        help="The pynkt name."
    )
    add.add_argument(
        "-n",
        "--numb",
        action="store",
        type=int,
        required=True,
        help="The number reys."
    )
    add.add_argument(
        "-s",
        "--samolet",
        action="store",
        help="The samolet."
    )

    # Создать субпарсер для отображения всех рейсов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all reys"
    )

    # Создать субпарсер для выбора рейса.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the reys"
    )
    select.add_argument(
        "-p",
        "--pynkt",
        action="store",
        required=True,
        help="The pynkt name."
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все рейсы из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        reys = load_reys(args.filename)
    else:
        reys = []

    # Добавить рейс.
    if args.command == "add":
        reys = get_reys(
            reys,
            args.pynkt,
            args.numb,
            args.samolet
        )
        is_dirty = True

    # Отобразить всех рейсов.
    elif args.command == "display":
        display_reys(reys)

    # Выбрать требуемые самолеты.
    elif args.command == "select":
        selected = select_reys(reys, args.samolet)
        display_reys(selected)

    # Сохранить данные в файл, если список рейсов был изменен.
    if is_dirty:
        save_reys(args.filename, reys)


if __name__ == '__main__':
    main()
