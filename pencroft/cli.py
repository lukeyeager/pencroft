from __future__ import absolute_import

import argparse

from . import benchmark


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    benchmark.set_parser(subparsers.add_parser('benchmark'))

    args = parser.parse_args()
    args.func(args)
