# Manual: Creating a Python Tool with uv

This manual explains how to turn a Python application into a tool using the uv package manager. We'll go through each step in detail, explaining what each component does and why it's needed.

## Prerequisites

- Python 3.8 or higher installed
- uv installed (see [uv installation guide](https://github.com/astral-sh/uv#installation))
- Basic understanding of Python

## 1. Project Structure

First, we need to organize our code into a proper Python package structure:

```
concat-tool/                 # Root directory
├── concat_tool/            # Package directory (note the underscore)
│   ├── __init__.py        # Makes the directory a Python package
│   └── cli.py             # Main implementation
├── pyproject.toml         # Project metadata and build configuration
└── README.md             # Project documentation
```

### Why this structure?
- The root directory can have dashes (`concat-tool`), but the package directory should use underscores (`concat_tool`) as per [PEP 8](https://peps.python.org/pep-0008/#package-and-module-names)
- `__init__.py` marks the directory as a Python package (see [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages))
- `pyproject.toml` is the modern way to configure Python projects (see [PEP 621](https://peps.python.org/pep-0621/))

## 2. Configuration Files

### pyproject.toml

This is the main configuration file. Let's break down each section:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
- This section tells uv how to build the package
- We're using `hatchling` as our build backend (see [uv build backends](https://docs.astral.sh/uv/guides/build-backends/))
- Reference: [uv Publishing Guide](https://docs.astral.sh/uv/guides/publishing/)

```toml
[project]
name = "concat-tool"
version = "0.1.0"
description = "A CLI tool that concatenates multiple files into one output, separated by filename headers."
requires-python = ">=3.8"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
dependencies = []
```
- Basic metadata about your project
- `name`: The package name (used when installing)
- `requires-python`: Minimum Python version needed
- `dependencies`: List of required packages (empty in our case)
- Reference: [uv Project Metadata](https://docs.astral.sh/uv/guides/publishing/#project-metadata)

```toml
[project.scripts]
concat-files = "concat_tool.cli:main"
```
- Defines command-line entry points
- Format: `command-name = "package.module:function"`
- This makes `concat-files` available as a command after installation
- Reference: [uv Entry Points](https://docs.astral.sh/uv/guides/publishing/#entry-points)

```toml
[tool.hatch.build.targets.wheel]
packages = ["concat_tool"]
```
- Tells hatchling which packages to include in the build
- Reference: [Hatch Build Configuration](https://hatch.pypa.io/latest/config/build/)

## 3. Package Implementation

### __init__.py
```python
"""
concat-tool - A CLI tool for concatenating multiple files with headers.
"""

__version__ = "0.1.0"
```
- Minimal initialization file
- Version should match pyproject.toml

### cli.py
- Contains the main implementation
- Uses `argparse` for command-line argument handling
- Has a `main()` function that serves as the entry point

## 4. Building and Installing

### Building the Package
```bash
uv build
```
- Creates both source distribution (.tar.gz) and wheel (.whl) files in `dist/`
- Reference: [uv Build Command](https://docs.astral.sh/uv/guides/publishing/#building)

### Installing as a Tool
```bash
uv tool install dist/*.whl
```
- Installs the built wheel as a tool
- Makes the command available system-wide
- Reference: [uv Tool Installation](https://docs.astral.sh/uv/guides/tools/)

### Development Installation
```bash
uv tool install --editable .
```
- Installs the package in "editable" mode
- Changes to the source code are immediately reflected
- Reference: [uv Editable Installs](https://docs.astral.sh/uv/guides/tools/#editable-installs)

## 5. Development Workflow

1. Create virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install build dependencies:
```bash
uv pip install hatchling
```

3. Build and install:
```bash
uv build
uv tool install --editable .
```

4. Test the tool:
```bash
concat-files --help
```

## 6. Distribution

While this tool is private, you could distribute it in several ways:
1. Direct from source directory
2. From a wheel file
3. From a private Git repository
4. Through a private PyPI server

Reference: [uv Tool Installation Sources](https://docs.astral.sh/uv/guides/tools/#installation)

## Common Issues and Solutions

1. "No executables are provided":
   - Check `[project.scripts]` section in pyproject.toml
   - Ensure the referenced function exists

2. Import errors after installation:
   - Check package structure
   - Verify `packages` in `[tool.hatch.build.targets.wheel]`

3. Command not found:
   - Ensure tool installation was successful
   - Check if uv's bin directory is in your PATH

## Further Reading

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Hatch Documentation](https://hatch.pypa.io/) 