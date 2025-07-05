"""
Run ``bumpy`` from the command line.

With the ``bumpy`` package installed, this script can be called directly from
the command line with::

    bumpy <args>

Command Line Arguments
----------------------
--patch : int, optional
    Bump the patch version. Default is 0 (arg not passed),
    or 1 (arg passed, no value given). Otherwise, bump
    version by the given number. Example::

        bumpy --patch    # bump patch version by 1
        bumpy --patch 3  # bump patch version by 3

--minor : int, optional
    Bump the minor version. Default is 0 (arg not passed),
    or 1 (arg passed, no value given). Otherwise, bump
    version by the given number. Example::

        bumpy --minor    # bump minor version by 1
        bumpy --minor 2  # bump minor version by 2

    Bumping the minor version will reset the patch version to 0.

--major : int, optional
    Bump the major version. Default is 0 (arg not passed),
    or 1 (arg passed, no value given). Otherwise, bump
    version by the given number. Example::

        bumpy --major    # bump major version by 1
        bumpy --major 4  # bump major version by 4

    Bumping the major version will reset the minor and patch versions to 0.

--version : flag, optional
    Pass this arg to manually enter a new version number.

@author: David Hebert
"""

import argparse

from bumpy.bumpy import Bumper


class CLI:
    """
    A command line interface class.

    Attributes
    ----------
    args : :class:`argparse.Namespace`
        Parsed command-line arguments.
    """

    def __init__(self) -> None:
        self.args = self.get_args()
        self.main()

    def get_args(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Bump or change version numbers.')
        group = parser.add_mutually_exclusive_group()
        help_msg = {
            'patch': """Bump the patch version.""",
            'minor': """Bump the minor version.""",
            'major': """Bump the major version.""",
            'version': """Enter a new version number.""",
        }

        group.add_argument(
            '--patch',
            action='store',
            type=int,
            nargs='?',
            const=1,
            default=0,
            help=help_msg['patch'],
        )

        group.add_argument(
            '--minor',
            action='store',
            type=int,
            nargs='?',
            const=1,
            default=0,
            help=help_msg['minor'],
        )

        group.add_argument(
            '--major',
            action='store',
            type=int,
            nargs='?',
            const=1,
            default=0,
            help=help_msg['major'],
        )

        group.add_argument('--version', action='store_true', help=help_msg['version'])

        return parser.parse_args()

    def main(self) -> None:
        bumpy = Bumper()
        if self.args.version is True:
            new_version = bumpy.input_new_version_number()
            if new_version:
                bumpy.write_version_numbers(new_version)
        elif not any([self.args.major, self.args.minor, self.args.patch]):
            bumpy.print_current_version_numbers()
        else:
            bumpy.bump_version_numbers(
                major=self.args.major,
                minor=self.args.minor,
                patch=self.args.patch,
            )


def main():
    """Run the CLI."""
    CLI()
