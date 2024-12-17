# concat-tool

A CLI tool that concatenates multiple files into one output, separated by filename headers.

## Prerequisites

1. Python 3.8 or higher
2. uv package manager (installation instructions below)

### Installing UV

On Unix-like systems (Linux, macOS):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other installation methods, see [UV Installation Guide](https://github.com/astral-sh/uv#installation).

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd concat-tool
```

2. Install the tool:
```bash
uv tool install .
```

That's it! The tool is now available as `concat-files` in your terminal.

## Usage

Print concatenated files to terminal:
```bash
concat-files file1.txt file2.md file3.log
```

Save concatenated output to a file:
```bash
concat-files file1.txt file2.md file3.log --output combined.txt
```

Show version information:
```bash
concat-files --version
```

## Development

If you want to modify the tool:

1. Clone the repository as above

2. Make your changes to the code

3. The changes will take effect immediately - no rebuild or reinstall needed!

### Building for Distribution

If you want to distribute the tool:

1. Build the package:
```bash
uv build
```

2. Install from the built wheel:
```bash
uv tool install dist/*.whl
```

## Uninstallation

To remove the tool:
```bash
uv tool uninstall concat-tool
```

## License

MIT License 