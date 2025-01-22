import sys
import argparse
import os
from pathlib import Path

def get_template():
    template_path = Path(__file__).parent / 'template.txt'
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback template if file is not found
        return "\n\n=== START: {filepath} ===\n\n{content}\n\n=== END: {filepath} ===\n\n"

def get_files_from_directory(directory: Path, extensions: list[str] = None) -> list[Path]:
    """Get all files from a directory, optionally filtered by extensions."""
    files = []
    
    # If no extensions specified, get all files
    if not extensions:
        files = [f for f in directory.rglob('*') if f.is_file()]
    else:
        # Normalize extensions to start with dot
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        files = [f for f in directory.rglob('*') if f.is_file() and f.suffix in extensions]
    
    # Sort files for consistent output
    return sorted(files)

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate multiple files into one output with filepath headers."
    )
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("files", nargs="*", help="List of files to concatenate.")
    parser.add_argument("-o", "--output", help="Output file path. If not provided, prints to stdout.")
    parser.add_argument("-d", "--directory", nargs="+", help="One or more directories to read files from.")
    parser.add_argument("-e", "--extensions", nargs="+", help="When using -d, only include files with these extensions (e.g., .py .md)")

    args = parser.parse_args()

    if args.version:
        print("concat-files version TEST-1")
        return

    # Get the template
    template = get_template()

    # Handle directory mode
    if args.directory:
        file_paths = []
        for dir_path in args.directory:
            directory = Path(dir_path)
            if not directory.exists() or not directory.is_dir():
                parser.error(f"Directory does not exist or is not a directory: {dir_path}")
            dir_files = get_files_from_directory(directory, args.extensions)
            file_paths.extend(dir_files)
        if not file_paths:
            parser.error(f"No matching files found in directories: {', '.join(args.directory)}")
    else:
        # Handle direct file list mode
        if not args.files:
            parser.error("At least one file is required unless --version or -d is specified")
        file_paths = [Path(f) for f in args.files]
        # Validate input files
        for fp in file_paths:
            if not fp.exists() or not fp.is_file():
                parser.error(f"File does not exist or is not a file: {fp}")

    # Sort files for consistent output
    file_paths.sort()

    # Open output destination
    if args.output:
        out_path = Path(args.output)
        out_file = out_path.open("w", encoding="utf-8")
    else:
        out_file = sys.stdout

    # Concatenate files with headers
    try:
        for fp in file_paths:
            content = fp.read_text(encoding="utf-8")
            # Use os.path.relpath which is more flexible than Path.relative_to
            relative_path = os.path.relpath(fp, start=os.getcwd())
            formatted = template.format(filepath=relative_path, content=content)
            out_file.write(formatted)
            out_file.write("\n")
    finally:
        if out_file is not sys.stdout:
            out_file.close()

if __name__ == "__main__":
    main() 