# `bumpy`
A simple script for bumping the version number of files in a package.

## bumpy.toml
`bumpy` looks for a file `bumpy.toml` in the current working directory to determine which files should be bumped.
The `bumpy.toml` file should contain an array called `files_to_bump`. An example of a `bumpy.toml` file looks like this:

```
files_to_bump = [
    'src\\__init__.py',
    'pyproject.toml',
    'docs\\conf.py'
]
```

## Command-line interface
Use `bumpy` from the command line. Change version numbers with a few simple args:

### `--patch <int>`
Bump the patch version by the given number.

### `--minor <int>`
Bump the minor version by the given number.

### `--major <int>`
Bump the major version by the given number.

### `--version`
Prompts the user to enter a completely new version number.

### Examples
```
bumpy --patch
```
Bump patch version by 1.
```
bumpy --major 2
```
Bump major version by 2.
```
bumpy --version
```
Get prompted for new version number.

## Future
`bumpy` only supports simple numeric version numbers (e.g., 0.1.2). In the future `bumpy` will support [PEP-440](https://peps.python.org/pep-0440/) version formats.
