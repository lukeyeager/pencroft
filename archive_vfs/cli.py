from __future__ import absolute_import

import argparse

from . import benchmark


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    benchmark_parser = subparsers.add_parser('benchmark')
    benchmark_parser.add_argument('path')
    benchmark_parser.set_defaults(func=benchmark.main)

    args = parser.parse_args()
    args.func(args)
