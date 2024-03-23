"""
Bump or change semantic version numbers.

@author: David Hebert
"""
from pathlib import Path
import tomllib
import re
from fileinput import FileInput


class VersionNumber:
    def __init__(self, filename, version_number, span):
        self.filename = filename
        self.number = version_number
        self.span = span

    def __str__(self):
        return f'\033[36m{self.number}\t\033[33m{self.filename}\033[37m'


class Bumper:
    def __init__(self):
        if self._find_bumpy_toml():
            self.files_to_bump = self.read_bumpy_toml()
            self.current_versions = self.read_current_version_numbers()
        else:
            raise FileNotFoundError('\033[31mbumpy.toml not found in current working directory.\033[37m')

    def _find_bumpy_toml(self):
        bumpy_toml = Path.cwd() / 'bumpy.toml'
        return bumpy_toml.exists()

    def read_bumpy_toml(self) -> list[str]:
        with open("bumpy.toml", "rb") as f:
            files_to_bump = tomllib.load(f)['files_to_bump']
        return files_to_bump

    def _match_regex(self, content):
        pattern = r"['\"](\d+\.\d+\.\d+)['\"]"
        return re.search(pattern, content)

    def read_current_version_numbers(self) -> list[VersionNumber]:
        version_numbers = []
        for file_path in self.files_to_bump:
            file = Path(file_path)
            if file.exists() and file.is_file():
                regex_match = self._match_regex(file.read_text())
                if regex_match:
                    version_numbers.append(VersionNumber(filename=file_path,
                                                         version_number=regex_match.group(),
                                                         span=regex_match.span()))
            else:
                print('\n\033[31mWarning: '
                      + f'\033[37m File \033[36m{file_path}'
                      + '\033[37m not found. Double-check path.')
        if not version_numbers:
            raise Exception('No version numbers founds. '
                            + 'Check bumpy.toml is in current working directory '
                            + 'and paths are correct.')
        return version_numbers

    def print_current_version_numbers(self):
        print('\nCurrent Version Numbers')
        print('=' * len(max(map(str, self.current_versions))))
        for version in self.current_versions:
            print(version)

    def _format_version_number(self, reference_number: str, new_number: str) -> (str | None):
        if reference_number.startswith("'"):
            return f"'{new_number}'"
        elif reference_number.startswith('"'):
            return f'"{new_number}"'

    def make_new_VersionNumbers(self, new_versions: list[str]) -> list[VersionNumber]:
        new_version_numbers: list[VersionNumber] = []
        for current, new_number in zip(self.current_versions, new_versions):
            formatted_number = self._format_version_number(reference_number=current.number,
                                                           new_number=new_number)
            new_version_numbers.append(VersionNumber(filename=current.filename,
                                                     version_number=formatted_number,
                                                     span=current.span))
        return new_version_numbers

    def get_new_version_number(self) -> (list[VersionNumber] | None):
        self.print_current_version_numbers()
        while True:
            new_version_number = input('\nEnter a new version number or "q" to quit: \033[32m')
            print('\033[37m')
            if new_version_number.strip().lower() == 'q':
                return None
            if self._match_regex(f"'{new_version_number}'"):
                return self.make_new_VersionNumbers([new_version_number] * len(self.current_versions))
            else:
                print('Incorrect version number format. '
                      + 'Enter three sets of digits separated by periods.')
                print('Example: 0.1.3 or 1.2.12')

    def _print_bumped_version(self, new_version_numbers: list[VersionNumber]) -> None:
        print('New Version Numbers')
        print('=' * len(max(map(str, self.current_versions))))
        for old, new in zip(self.current_versions, new_version_numbers):
            print(f'\033[36m{old.number}  \033[37m--->  \033[32m{new.number}\t\033[33m{old.filename}\033[37m')
        print('')

    def write_new_version_numbers(self, new_version_numbers: list[VersionNumber]) -> None:
        for current, new in zip(self.current_versions, new_version_numbers):
            with FileInput(current.filename, inplace=True) as f:
                for line in f:
                    print(line.replace(current.number, new.number), end='')
        self._print_bumped_version(new_version_numbers)

    def bump_version_numbers(self, major: int = 0, minor: int = 0, patch: int = 0) -> None:
        new_versions: list[str] = []
        for current in self.current_versions:
            current_major, current_minor, current_patch = map(int, current.number.strip('\"\'').split('.'))
            new_number = '.'.join([str(current_major + major),
                                   str(current_minor + minor),
                                   str(current_patch + patch)])
            if self._match_regex(f"'{new_number}'"):
                new_versions.append(new_number)
        self.write_new_version_numbers(self.make_new_VersionNumbers(new_versions))


if __name__ == '__main__':
    bumpy = Bumper()
    new_version = bumpy.get_new_version_number()
    if new_version:
        bumpy.write_new_version_numbers(new_version)
