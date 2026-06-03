"""python -m pycommonist"""

import logging
import sys

from pycommonist.framework.application import run


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    sys.exit(run())


if __name__ == "__main__":
    main()
