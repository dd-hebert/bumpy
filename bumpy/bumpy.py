"""
Bump or change semantic version numbers.

@author: David Hebert
"""
import os
import tomllib
import re


class VersionNumber:
    def __init__(self, filename, version_number, span):
        self.filename = filename
        self.number = version_number
        self.span = span

    def __str__(self):
        return f'{self.number}\t{self.filename}'


class Bumper:
    def __init__(self):
        if self._find_bumpy():
            self.files_to_bump = self.get_files_to_bump()
            self.current_versions = self.get_current_version_numbers()

    def _find_bumpy(self):
        return os.path.exists(os.path.join(os.getcwd(), 'bumpy.toml'))

    def get_files_to_bump(self):
        with open("bumpy.toml", "rb") as f:
            files_to_bump = tomllib.load(f)['files_to_bump']
        return files_to_bump

    def _match_regex(self, content):
        pattern = r"['\"](\d+\.\d+\.\d+)['\"]"
        return re.search(pattern, content)

    def get_current_version_numbers(self):
        version_numbers = []

        for file in self.files_to_bump:
            with open(file, 'r') as f:
                content = f.read()

            regex_match = self._match_regex(content)
            version_numbers.append(VersionNumber(filename=file,
                                                 version_number=regex_match[0],
                                                 span=regex_match.span()))
        return version_numbers

    def print_current_versions(self):
        print('\nCurrent Version Numbers:')
        print('========================')
        for version in self.current_versions:
            print(version)

    def _print_bumped_version(self, old_version, new_version):
        print(f'{old_version.number}  --->  {new_version}\t{old_version.filename}')

    def get_new_version_number(self):
        self.print_current_versions()
        while True:
            new_version = input('\nEnter a new version number or "q" to quit: ')
            if new_version.strip().lower() == 'q':
                return None
            if self._match_regex(f"'{new_version}'"):
                # print('\n')
                return new_version
            else:
                print('\n'
                      + 'Incorrect version number format. '
                      + 'Enter three sets of digits separated by periods.')
                print('Example: 0.1.3 or 1.2.12')

    def _format_version_number(self, reference, new_version):
        if reference.startswith("'"):
            formatted_new_version_number = f"'{new_version}'"
        elif reference.startswith('"'):
            formatted_new_version_number = f'"{new_version}"'
        return formatted_new_version_number

    def set_version_numbers(self, new_version):
        for version in self.current_versions:
            formatted_new_version = self._format_version_number(reference=version.number,
                                                                new_version=new_version)
            with open(version.filename, 'r+') as f:
                content = f.read()
                content = content.replace(version.number,
                                          formatted_new_version)
                f.seek(0)
                f.write(content)
                f.truncate()
            self._print_bumped_version(version, formatted_new_version)

    def bump_version_numbers(self, major=0, minor=0, patch=0):
        current_major, current_minor, current_patch = self.current_versions[0].number.strip('\"\'').split('.')
        new_major = str(int(current_major) + major)
        new_minor = str(int(current_minor) + minor)
        new_patch = str(int(current_patch) + patch)
        new_version = '.'.join([new_major, new_minor, new_patch])
        if self._match_regex(f"'{new_version}'"):
            self.set_version_numbers(new_version)


if __name__ == '__main__':
    bumpy = Bumper()
    new_version = bumpy.get_new_version_number()
    if new_version:
        bumpy.set_version_numbers(new_version)
