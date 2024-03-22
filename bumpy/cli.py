"""
Run ``bumpy`` from the command line.

With the ``bumpy`` package installed, this script can be called directly from
the command line with::

    bumpy <args>

Command Line Arguments
----------------------
--patch : int, optional
    Bump the patch version by this number.
--minor : int, optional
    Bump the minor version by this number.
--major : int, optional
    Bump the major version by this number.
--version : flag, optional
    Pass this arg to give manually enter a new version number.

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

    def __init__(self):
        self.args = self.get_args()

        self.main()

    def get_args(self):
        """
        Create an ``ArgumentParser`` and parse command line arguments.

        Returns
        -------
        parser : :class:`argparse.ArgumentParser`
        """
        parser = argparse.ArgumentParser(description='Bump or change version numbers.')
        help_msg = {
            'patch': '''Bump the patch version by 1.''',
            'minor': '''Bump the minor version by 1.''',
            'major': '''Bump the major version by 1.''',
            'version': '''Enter a new version number.'''}

        parser.add_argument('--patch',
                            action='store',
                            type=int,
                            nargs='?',
                            const=1,
                            default=0,
                            help=help_msg['patch'])

        parser.add_argument('--minor',
                            action='store',
                            type=int,
                            nargs='?',
                            const=1,
                            default=0,
                            help=help_msg['minor'])

        parser.add_argument('--major',
                            action='store',
                            type=int,
                            nargs='?',
                            const=1,
                            default=0,
                            help=help_msg['major'])

        parser.add_argument('--version',
                            action='store_true',
                            help=help_msg['version'])

        return parser.parse_args()

    def main(self):
        bumpy = Bumper()
        if self.args.version is True:
            new_version = bumpy.get_new_version_number()
            if new_version:
                bumpy.set_version_numbers(new_version)

        else:
            major_bump = self.args.major
            minor_bump = self.args.minor
            patch_bump = self.args.patch
            bumpy.bump_version_numbers(major=major_bump,
                                       minor=minor_bump,
                                       patch=patch_bump)


def main():
    """Run the CLI."""
    CLI()
