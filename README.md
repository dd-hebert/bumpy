# bumpy
A simple script for bumping the version number of files in a package.

# bumpy.toml
bumpy looks for a file `bumpy.toml` in the current working directory to determine which files should be bumped.
The `bumpy.toml` file should contain an array called `files_to_bump`. An example of a `bumpy.toml` file looks like this:

```
files_to_bump = [
    'src\\__init__.py',
    'pyproject.toml',
    'docs\\conf.py'
]
```
