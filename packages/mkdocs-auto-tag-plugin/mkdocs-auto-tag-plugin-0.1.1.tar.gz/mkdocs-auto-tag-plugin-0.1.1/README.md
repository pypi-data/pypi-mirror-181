# mkdocs-auto-tag-plugin
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-auto-tag-plugin)](https://pypi.org/project/mkdocs-auto-tag-plugin/)
![License](https://img.shields.io/pypi/l/mkdocs-auto-tag-plugin)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-auto-tag-plugin)

This plugin is designed to add tags to files based on their path (parent direcctories or file name).

!!! Warning: Pre alpha: This is currently just a PoC for myself

## Documentation

This README is just a short intro to the package.
For a quick start and detailed information please see the [documentation](https://mkdocs-auto-tag-plugin.six-two.dev/).
The documentation is also available in the `docs` folder of the source code and can be built localy with [MkDocs](https://www.mkdocs.org/).

## Tests

The files in the `docs/test/` directory implicitely work as tests.
They should be tagged correctly.


## Notable changes

### HEAD

### 0.1.1

- Added support for assigning lists of tag to globs.
- Added regex support
    - Capture groups can be used to generate dynamic tags

### 0.1.0

- Implemented working prototype that uses custom globs for the file path matching.

### 0.0.1

- Reserved name on PyPI

