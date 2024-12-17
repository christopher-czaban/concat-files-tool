import sys
import argparse
from pathlib import Path

def get_template():
    template_path = Path(__file__).parent / 'template.txt'
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback template if file is not found
        return "\n\n=== START: {filename} ===\n\n{content}\n\n=== END: {filename} ===\n\n"

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate multiple files into one output with filename headers."
    )
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("files", nargs="*", help="List of files to concatenate.")
    parser.add_argument("-o", "--output", help="Output file path. If not provided, prints to stdout.")

    args = parser.parse_args()

    if args.version:
        print("concat-files version TEST-1")
        return

    if not args.files:
        parser.error("at least one file is required unless --version is specified")

    # Get the template
    template = get_template()

    # Validate input files
    file_paths = [Path(f) for f in args.files]
    for fp in file_paths:
        if not fp.exists() or not fp.is_file():
            print(f"Error: {fp} does not exist or is not a file.", file=sys.stderr)
            sys.exit(1)

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
            formatted = template.format(filename=fp.name, content=content)
            out_file.write(formatted)
    finally:
        if out_file is not sys.stdout:
            out_file.close()


if __name__ == "__main__":
    main() 