#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pathlib


def main():
    path = pathlib.Path.cwd() / 'test.md'
    with open(path, mode='r') as fid:
        headers = [line.strip() for line in fid if line.startswith('#')]
    print('\n'.join(headers))


if __name__ == '__main__':
    main()
