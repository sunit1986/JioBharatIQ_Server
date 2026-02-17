"""Entry point for `uvx jiobharatiq-server` and `python -m jiobharatiq_server`."""

import sys
from .server import main as _main, SERVER_VERSION


def main():
    print(f"JioBharatIQ Knowledge Server v{SERVER_VERSION} ready", file=sys.stderr, flush=True)
    _main()


if __name__ == "__main__":
    main()
