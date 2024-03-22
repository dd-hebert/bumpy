"""
Default entry point if running the package using ``python -m bumpy``.

@author: David Hebert
"""
import sys
import bumpy.cli


def main():
    """Run bumpy from cli script entry point."""
    cli = bumpy.cli.CLI()
    return 0


if __name__ == '__main__':
    sys.exit(main())
