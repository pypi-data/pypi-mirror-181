from __future__ import annotations

import argparse
import sys
from typing import Sequence

from sms_over_smtp import constants
from sms_over_smtp.commands import list_providers


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog='sms-over-smtp')

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {constants.VERSION}',
    )

    subparsers = parser.add_subparsers(dest='command')

    # Register command parsers
    list_providers.create_parser(subparsers)

    # Default to listing providers if no command name is supplied
    if len(argv) == 0:
        argv = [list_providers.COMMAND_NAME]

    args = parser.parse_args(argv)

    if args.command == list_providers.COMMAND_NAME:
        return list_providers.list_all()
    else:
        raise NotImplementedError(f'Command "{args.command}" not implemented.')

    raise AssertionError(
        f'Command "{args.command}" failed to exit with a returncode.',
    )


if __name__ == '__main__':
    raise SystemExit(main())
