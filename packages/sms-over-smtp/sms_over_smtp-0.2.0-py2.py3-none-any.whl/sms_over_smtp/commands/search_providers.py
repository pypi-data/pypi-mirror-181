from __future__ import annotations

import argparse

from sms_over_smtp.provider import PROVIDERS
from sms_over_smtp.util import pretty_print_providers

COMMAND_NAME = 'search-providers'


def create_parser(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = parser.add_parser(
        COMMAND_NAME,
        help='search for a supported provider',
    )
    p.add_argument('term', nargs='?', default='', help='term to searh for')
    p.add_argument('--country', nargs='?', help='filter by specified country')
    p.add_argument('--region', nargs='?', help='filter by specified region')
    p.add_argument(
        '--sms', action='store_true', default=None,
        help='filter by providers that support sms',
    )
    p.add_argument(
        '--mms', action='store_true', default=None,
        help='filter by providers that support mms',
    )


def search(args: argparse.Namespace) -> int:
    providers = [p for p in PROVIDERS if p.contains_term(args.term)]

    if args.country is not None:
        providers = [
            p for p in providers if p.has_location_support(
                args.country, args.region,
            )
        ]

    if args.sms is not None:
        providers = [p for p in providers if p.sms is not None]

    if args.mms is not None:
        providers = [p for p in providers if p.mms is not None]

    if len(providers) == 0:
        print('No results.')
    else:
        pretty_print_providers(providers)
    return 0
