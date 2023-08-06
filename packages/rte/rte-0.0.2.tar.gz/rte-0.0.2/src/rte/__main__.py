import argparse
import sys
from rte.db import db


class ParseArgs:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='rte',
            description='Facilitate the standardization of rte utility commands.',
        )
        self.db_create = None
        self.subparsers = self.parser.add_subparsers(title='Commands')

    def db(self):
        self.parser_db = self.subparsers.add_parser(
            'db',
            help='Commands to manipulate the database.',
        )
        self.parser_db.add_argument(
            '-c',
            '--create',
            action='store_true',
            default=False,
            help='Create the db.  if it exists it will do nothing.',
        )
        self.parser_add_a.set_defaults(func=db.create)
        pass


def main():
    pa = ParseArgs()
    pa.db_create()
    if len(sys.argv) > 1:
        args = pa.parser.parse_args()
        args.func(args)
    else:
        pa.parser.print_help()
        sys.exit(2)
    pass


if __name__ == "__main__":
    main()
