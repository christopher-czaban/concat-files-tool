import os
import argparse

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

def get_file_paths(extensions, exclude_dirs):
    file_paths = []

    for root, dirs, files in os.walk("."):
        # Skip excluded directories by modifying dirs in place
        dirs[:] = [d for d in dirs if not should_exclude_dir(d, exclude_dirs)]

        # Only add files if the current directory is not in excluded paths
        if not should_exclude_dir(root, exclude_dirs):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    relative_path = os.path.relpath(os.path.join(root, file), start=".")
                    file_paths.append(relative_path)

    return file_paths

def main():
    parser = argparse.ArgumentParser(
        description="List file paths with specified extensions, automatically excluding common library and system directories."
    )
    parser.add_argument("-e", "--extensions", nargs="+", required=True, 
                      help="File extensions to include, e.g., .py .md .json")
    parser.add_argument("-o", "--omit_dirs", nargs="*", default=[], 
                      help="Additional directories to exclude from the search (common library directories are excluded by default)")

    args = parser.parse_args()

    # Combine default and user-specified exclude directories
    exclude_dirs = {os.path.normpath(d) for d in args.omit_dirs}
    exclude_dirs.update(DEFAULT_EXCLUDE_DIRS)

    # Get file paths
    file_paths = get_file_paths(args.extensions, exclude_dirs)

    # Sort first by extension, then alphabetically
    file_paths.sort(key=lambda x: (os.path.splitext(x)[1], x))

    # Print paths as a whitespace-separated list
    print(" ".join(file_paths))

if __name__ == "__main__":
    main()