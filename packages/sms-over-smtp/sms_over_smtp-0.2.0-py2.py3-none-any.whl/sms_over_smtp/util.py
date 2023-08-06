from __future__ import annotations

from sms_over_smtp.provider import Provider


def pretty_print_table(heading: list[str], rows: list[list[str]]) -> None:
    table = [heading] + rows
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = ''.join(
        ['{:<' + str(longest_col) + '}' for longest_col in longest_cols],
    )
    for row in table:
        print(row_format.format(*row))


def pretty_print_providers(providers: list[Provider]) -> None:
    pretty_print_table(
        ['NAME:', 'ALIASES:', 'COUNTRY:', 'REGION:', 'SMS:', 'MMS:'], [
            p.to_string_list() for p in providers
        ],
    )
