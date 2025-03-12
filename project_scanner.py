"""
Enhanced Project Structure Scanner

This script scans the project directory and generates a detailed visualization 
of the project structure including file sizes and last modified dates.
It excludes common system directories and files, and saves the output to a text file.
"""

import os
import argparse
import datetime
from pathlib import Path

# Directories and files to exclude from visualization
EXCLUDE_DIRS = {
    '__pycache__', '.git', '.idea', '.vscode', '.pytest_cache',
    'venv', 'env', '.env', 'node_modules', 'build', 'dist', 'site-packages'
}

EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db', '.gitignore', '*.pyc', '*.pyo', 
    '*.pyd', '*~', '.directory', '*.so', '*.exe'
}

def format_size(size_bytes):
    """Format file size in a human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def format_timestamp(timestamp):
    """Format timestamp as a readable date and time."""
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def should_exclude(path):
    """Check if a path should be excluded from the visualization."""
    path_obj = Path(path)
    
    # Check if any part of the path is in EXCLUDE_DIRS
    for part in path_obj.parts:
        if part in EXCLUDE_DIRS:
            return True
    
    # Check for excluded files
    for pattern in EXCLUDE_FILES:
        if pattern.startswith('*') and path_obj.name.endswith(pattern[1:]):
            return True
        elif pattern == path_obj.name:
            return True
            
    return False

def dir_tree_generator(root_dir, prefix="", is_last=True, max_depth=None, current_depth=0):
    """Generate the directory tree structure as strings."""
    if max_depth is not None and current_depth > max_depth:
        return
        
    # Skip excluded directories
    if should_exclude(root_dir):
        return
        
    # Prepare the prefix for the current item
    if is_last:
        branch = "└── "
        new_prefix = prefix + "    "
    else:
        branch = "├── "
        new_prefix = prefix + "│   "
        
    # Get path information
    path = Path(root_dir)
    
    # Get file information if it's a file
    if path.is_file():
        stats = path.stat()
        size = format_size(stats.st_size)
        modified = format_timestamp(stats.st_mtime)
        yield f"{prefix}{branch}{path.name} - {size}, Last modified: {modified}"
    else:
        # For directories, just show the name
        yield f"{prefix}{branch}{path.name}/"
    
    # If it's a directory, recursively process its contents
    if path.is_dir():
        # Get all items in the directory
        items = sorted([p for p in path.iterdir() 
                       if not should_exclude(p)], 
                       key=lambda p: (p.is_file(), p.name))
        
        # Process each item
        for i, item in enumerate(items):
            is_last_item = (i == len(items) - 1)
            yield from dir_tree_generator(item, new_prefix, is_last_item, max_depth, current_depth + 1)

def main():
    """Main function to scan and visualize project structure."""
    parser = argparse.ArgumentParser(description="Visualize project directory structure with file details")
    parser.add_argument('--path', '-p', default=".", 
                        help="Path to the project directory (default: current directory)")
    parser.add_argument('--depth', '-d', type=int, default=None,
                        help="Maximum depth to display (default: no limit)")
    parser.add_argument('--output', '-o', default="project_structure.txt",
                        help="Output file path (default: project_structure.txt)")
    
    args = parser.parse_args()
    
    # Get absolute path to project directory
    project_dir = os.path.abspath(args.path)
    project_name = os.path.basename(project_dir)
    
    # Generate the project structure
    lines = []
    
    lines.append(f"Project Structure: {project_name}")
    lines.append("=" * (len(project_name) + 18))
    lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Root directory: {project_dir}")
    lines.append("")
    
    # Add each line from the generator
    for line in dir_tree_generator(project_dir, max_depth=args.depth):
        lines.append(line)
    
    # Print to console
    for line in lines:
        print(line)
    
    # Save to file
    with open(args.output, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")
    
    print(f"\nProject structure saved to {args.output}")
    
if __name__ == "__main__":
    main()