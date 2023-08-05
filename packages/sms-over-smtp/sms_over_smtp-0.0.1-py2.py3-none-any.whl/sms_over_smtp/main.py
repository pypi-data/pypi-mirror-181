from __future__ import annotations

import sys
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    raise NotImplementedError('Running in command line not implemented.')


if __name__ == '__main__':
    raise SystemExit(main())
