from __future__ import annotations

import argparse

from sms_over_smtp.provider import PROVIDERS
from sms_over_smtp.util import pretty_print_providers

COMMAND_NAME = 'list-providers'


def create_parser(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    parser.add_parser(
        COMMAND_NAME,
        help='list all providers',
    )


def list_all() -> int:
    pretty_print_providers(PROVIDERS)
    return 0
