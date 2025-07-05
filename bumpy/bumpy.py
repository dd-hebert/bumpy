"""
Bump or change semantic version numbers.

@author: David Hebert
"""

import re
from fileinput import FileInput
from pathlib import Path

import tomllib


class VersionNumber:
    def __init__(self, filename: str, version_number: str, quote: str):
        self.filename = filename
        self.number = version_number
        self.quote = quote
        self.major, self.minor, self.patch = self.parse_version_number()

    def parse_version_number(self) -> tuple[int, int, int]:
        major, minor, patch = map(int, self.number.strip("\"'").split("."))
        return major, minor, patch

    def __str__(self):
        return f"\033[36m{self.number} \033[33m{self.filename}\033[37m"


class Bumper:
    def __init__(self):
        if self._find_bumpy_toml():
            self.files_to_bump = self.read_bumpy_toml()
            self.current_versions = self.read_version_numbers()
        else:
            raise FileNotFoundError(
                "\033[31mbumpy.toml not found in "
                + "current working directory.\033[37m"
            )

    def _find_bumpy_toml(self) -> bool:
        bumpy_toml = Path.cwd() / "bumpy.toml"
        return bumpy_toml.exists()

    def read_bumpy_toml(self) -> list[str]:
        with open("bumpy.toml", "rb") as f:
            files_to_bump = tomllib.load(f)["files_to_bump"]
        return files_to_bump

    def _match_regex(self, content):
        pattern = r"(['\"])(\d+\.\d+\.\d+)\1"
        return re.search(pattern, content)

    def read_version_numbers(self) -> list[VersionNumber]:
        version_numbers = []
        for file_path in self.files_to_bump:
            file = Path(file_path)
            if file.exists() and file.is_file():
                regex_match = self._match_regex(file.read_text())
                if regex_match:
                    version_numbers.append(
                        VersionNumber(
                            filename=file_path,
                            version_number=regex_match.group(2),
                            quote=regex_match.group(1),
                        ),
                    )
            else:
                print(
                    "\n\033[31mWarning: "
                    + f"\033[37m File \033[36m{file_path}"
                    + "\033[37m not found. Double-check path."
                )
        if not version_numbers:
            raise Exception(
                "No version numbers founds. "
                + "Check bumpy.toml is in current working "
                + "directory and paths are correct."
            )
        return version_numbers

    def input_new_version_number(self) -> list[VersionNumber] | None:
        self.print_current_version_numbers()

        while True:
            new_version_number = input(
                'Enter a new version number or "q" to quit: \033[32m'
            )
            print("\033[37m")
            if new_version_number.strip().lower() == "q":
                return None
            if regex_match := self._match_regex(f"'{new_version_number}'"):
                return [
                    VersionNumber(
                        filename=current.filename,
                        version_number=regex_match.group(2),
                        quote=regex_match.group(1),
                    )
                    for current in self.current_versions
                ]
            else:
                print(
                    "Incorrect version number format. "
                    + "Enter three sets of digits separated by periods."
                )
                print("Example: 0.1.3 or 1.2.12")

    def write_version_numbers(self, version_numbers: list[VersionNumber]) -> None:
        for current, new in zip(self.current_versions, version_numbers):
            with FileInput(current.filename, inplace=True) as f:
                for line in f:
                    print(line.replace(current.number, new.number), end="")
        self._print_bumped_version(version_numbers)

    def bump_version_numbers(
        self, major: int = 0, minor: int = 0, patch: int = 0
    ) -> None:
        new_versions: list[str] = []

        for current in self.current_versions:
            new_major = current.major + major
            new_minor = current.minor
            new_patch = current.patch

            if major != 0:
                new_minor = 0
                new_patch = 0
            elif minor != 0:
                new_minor += minor
                new_patch = 0
            else:
                new_patch += patch

            new_number = f"{new_major}.{new_minor}.{new_patch}"

            if self._match_regex(current.quote + new_number + current.quote):
                new_versions.append(
                    VersionNumber(
                        filename=current.filename,
                        version_number=new_number,
                        quote=current.quote,
                    )
                )

        self.write_version_numbers(new_versions)

    def _print_list_heading(
        self, heading: str, length_offset: int, version_numbers: list[VersionNumber]
    ) -> None:
        longest_line = len(max(map(str, version_numbers)))
        if longest_line % 2 == 1:
            longest_line += 1
        line_length = max(len(heading) + 8, longest_line - length_offset)
        spacing = (line_length - (len(heading) + 2)) // 2
        print("")
        print("╔" + "═" * (line_length - 2) + "╗")
        print("║" + " " * spacing + heading + " " * spacing + "║")
        print("╚" + "═" * (line_length - 2) + "╝")

    def print_current_version_numbers(self) -> None:
        self._print_list_heading(
            heading="Current Version Numbers",
            length_offset=15,
            version_numbers=self.current_versions,
        )
        for version in self.current_versions:
            print(version)
        print("")

    def _print_bumped_version(self, new_version_numbers: list[VersionNumber]) -> None:
        self._print_list_heading(
            heading="New Version Numbers",
            length_offset=-1,
            version_numbers=new_version_numbers,
        )
        for old, new in zip(self.current_versions, new_version_numbers):
            print(
                f"\033[36m{old.number}"
                + "  \033[37m--->  "
                + f"\033[32m{new.number} \033[33m{old.filename}\033[37m"
            )
        print("")


# if __name__ == '__main__':
#     bumpy = Bumper()
#     new_version = bumpy.input_new_version_number()
#     if new_version:
#         bumpy.write_version_numbers(new_version)
