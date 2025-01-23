import sys
import argparse
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Common directories to exclude by default
DEFAULT_EXCLUDE_DIRS = {
    # Version control
    ".git", ".svn", ".hg",
    # Python virtual environments
    ".venv", "venv", "env",
    # Python cache and build
    "__pycache__", "build", "dist", "*.egg-info",
    # Node.js
    "node_modules",
    # IDE and editor
    ".idea", ".vscode",
    # macOS
    ".DS_Store",
    # Misc build/cache
    ".cache", ".pytest_cache", ".mypy_cache", ".tox",
    # Rust
    "target",
    # Go
    "vendor",
}

def should_exclude_dir(dir_path: str, exclude_dirs: set[str]) -> bool:
    """Check if directory should be excluded based on its path or any parent directory."""
    # Convert path to parts for checking each component
    parts = os.path.normpath(dir_path).split(os.sep)
    
    # Check each directory component against exclude patterns
    return any(part in exclude_dirs for part in parts)

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
    
    for root, dirs, filenames in os.walk(directory):
        # Skip excluded directories by modifying dirs in place
        dirs[:] = [d for d in dirs if not should_exclude_dir(d, DEFAULT_EXCLUDE_DIRS)]

        # Only process files if current directory is not excluded
        if not should_exclude_dir(os.path.relpath(root, directory), DEFAULT_EXCLUDE_DIRS):
            for filename in filenames:
                if extensions:
                    # Normalize extensions to start with dot
                    exts = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
                    if any(filename.endswith(ext) for ext in exts):
                        files.append(Path(root) / filename)
                else:
                    files.append(Path(root) / filename)
    
    # Sort files for consistent output
    return sorted(files)

def check_file_path_conflicts(file_paths: List[Path], prefix_sep: str, dir_sep: str) -> Tuple[List[Path], List[Path]]:
    """
    Check file paths for separator conflicts and return valid and invalid paths.
    
    Args:
        file_paths: List of Path objects to check
        prefix_sep: Separator used between prefix and filename/path
        dir_sep: Separator used between directory components
    
    Returns:
        Tuple of (valid_paths, invalid_paths)
    """
    valid_paths = []
    invalid_paths = []
    
    for fp in file_paths:
        # Convert to string for checking
        path_str = str(fp)
        if prefix_sep in path_str:
            print(f"Warning: Skipping file '{path_str}' - contains separator '{prefix_sep}'")
            invalid_paths.append(fp)
        elif dir_sep in path_str:
            print(f"Warning: Skipping file '{path_str}' - contains separator '{dir_sep}'")
            invalid_paths.append(fp)
        else:
            valid_paths.append(fp)
    
    return valid_paths, invalid_paths

def write_content_to_file(filepath: str, content: str) -> None:
    """Write content to a file, creating directories if needed."""
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def group_files_by_directory(file_paths: List[Path]) -> Dict[str, List[Path]]:
    """Group files by their parent directory path."""
    groups: Dict[str, List[Path]] = {}
    for fp in file_paths:
        # Get the parent directory path relative to cwd
        parent_path = str(fp.parent)
        if parent_path == '.':
            parent_path = ''
        groups.setdefault(parent_path, []).append(fp)
    return groups

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate multiple files into one output with filepath headers."
    )
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("files", nargs="*", help="List of files to concatenate.")
    parser.add_argument("-o", "--output", help="Output file path. If not provided, prints to stdout.")
    parser.add_argument("-d", "--directory", nargs="+", help="One or more directories to read files from.")
    parser.add_argument("-e", "--extensions", nargs="+", help="When using -d, only include files with these extensions (e.g., .py .md)")
    parser.add_argument("-s", "--split", action="store_true", help="Split output into separate files, one per input file.")
    parser.add_argument("-g", "--group", action="store_true", help="Group split files by directory (requires -s).")
    parser.add_argument("--prefix-separator", default="___", help="Separator between output prefix and filename/path (default: '___')")
    parser.add_argument("--dir-separator", default="__", help="Separator between directory components when using -g (default: '__')")

    args = parser.parse_args()

    # Validate arguments
    if args.version:
        print("concat-files version TEST-1")
        return

    if args.group and not args.split:
        parser.error("--group can only be used with --split")

    if (args.split or args.group) and not args.output:
        parser.error("--output is required when using --split or --group")

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

    # Check for separator conflicts
    valid_paths, invalid_paths = check_file_path_conflicts(file_paths, args.prefix_separator, args.dir_separator)
    if not valid_paths:
        parser.error("No valid files to process after checking for separator conflicts")

    # Handle split/group modes
    if args.split:
        output_prefix = Path(args.output).stem
        if args.group:
            # Group files by directory
            groups = group_files_by_directory(valid_paths)
            for dir_path, group_files in groups.items():
                # Create group output filename
                if dir_path:
                    # Replace path separators with dir_separator
                    safe_dir_path = dir_path.replace(os.sep, args.dir_separator)
                    output_name = f"{output_prefix}{args.prefix_separator}{safe_dir_path}.txt"
                else:
                    # Files in root directory
                    output_name = f"{output_prefix}{args.prefix_separator}root.txt"
                
                # Concatenate files in this group
                group_content = ""
                for fp in sorted(group_files):
                    content = fp.read_text(encoding="utf-8")
                    relative_path = os.path.relpath(fp, start=os.getcwd())
                    formatted = template.format(filepath=relative_path, content=content)
                    group_content += formatted + "\n"
                
                write_content_to_file(output_name, group_content)
        else:
            # Split into individual files
            for fp in valid_paths:
                content = fp.read_text(encoding="utf-8")
                relative_path = os.path.relpath(fp, start=os.getcwd())
                formatted = template.format(filepath=relative_path, content=content)
                
                # Create output filename using the file's name
                safe_name = fp.name
                output_name = f"{output_prefix}{args.prefix_separator}{safe_name}"
                write_content_to_file(output_name, formatted)
    else:
        # Standard single output mode
        if args.output:
            out_path = Path(args.output)
            out_file = out_path.open("w", encoding="utf-8")
        else:
            out_file = sys.stdout

        try:
            for fp in valid_paths:
                content = fp.read_text(encoding="utf-8")
                relative_path = os.path.relpath(fp, start=os.getcwd())
                formatted = template.format(filepath=relative_path, content=content)
                out_file.write(formatted)
                out_file.write("\n")
        finally:
            if out_file is not sys.stdout:
                out_file.close()

    # Print summary
    total_files = len(file_paths)
    skipped_files = len(invalid_paths)
    processed_files = len(valid_paths)
    print(f"\nSummary: Processed {processed_files} files, Skipped {skipped_files} files due to separator conflicts")

if __name__ == "__main__":
    main() 