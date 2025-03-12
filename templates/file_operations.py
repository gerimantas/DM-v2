"""
File operation templates for the AI Programming Assistant.
Provides common code patterns for file manipulation tasks.
"""

# Template for reading a text file
READ_TEXT_FILE = '''
# Read a text file and print its contents
def read_text_file(file_path):
    """
    Read the contents of a text file and return it as a string.
    
    Args:
        file_path: The path to the file to read.
        
    Returns:
        The contents of the file as a string.
    """
    try:
        # Open the file in read mode with proper encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all contents into a string
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    file_path = "your_file.txt"  # Change this to your file path
    content = read_text_file(file_path)
    if content:
        print("File content:")
        print(content)
'''

# Template for writing a text file
WRITE_TEXT_FILE = '''
# Write text to a file
def write_text_file(file_path, content):
    """
    Write content to a text file.
    
    Args:
        file_path: The path to the file to write to.
        content: The text content to write to the file.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        # Open the file in write mode with proper encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write the content to the file
            file.write(content)
        print(f"Content successfully written to '{file_path}'.")
        return True
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

# Example usage
if __name__ == "__main__":
    file_path = "output.txt"  # Change this to your desired file path
    content = "This is some example text.\nIt has multiple lines.\nThird line."
    write_text_file(file_path, content)
'''

# Template for listing files in a directory
LIST_FILES = '''
# List all files in a directory
import os

def list_files_in_directory(directory_path, file_extension=None):
    """
    List all files in a directory, optionally filtering by file extension.
    
    Args:
        directory_path: The path to the directory to list files from.
        file_extension: Optional file extension to filter by (e.g. '.txt', '.py')
        
    Returns:
        A list of file names.
    """
    try:
        # Check if the directory exists
        if not os.path.exists(directory_path):
            print(f"Error: The directory '{directory_path}' was not found.")
            return []
            
        # Get all items in the directory
        all_items = os.listdir(directory_path)
        
        # Filter for files only (not directories)
        files = [item for item in all_items if os.path.isfile(os.path.join(directory_path, item))]
        
        # Filter by extension if specified
        if file_extension:
            files = [file for file in files if file.endswith(file_extension)]
            
        return files
        
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

# Example usage
if __name__ == "__main__":
    directory_path = "."  # Current directory, change as needed
    
    # List all files
    all_files = list_files_in_directory(directory_path)
    print(f"All files in directory: {all_files}")
    
    # List only Python files
    python_files = list_files_in_directory(directory_path, '.py')
    print(f"Python files in directory: {python_files}")
'''

# Template for copying files
COPY_FILE = '''
# Copy a file from one location to another
import shutil
import os

def copy_file(source_path, destination_path, overwrite=False):
    """
    Copy a file from source to destination.
    
    Args:
        source_path: The path to the source file.
        destination_path: The destination path for the copy.
        overwrite: Whether to overwrite the destination file if it exists.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"Error: Source file '{source_path}' does not exist.")
            return False
            
        # Check if destination file exists and overwrite is False
        if os.path.exists(destination_path) and not overwrite:
            print(f"Error: Destination file '{destination_path}' already exists.")
            return False
            
        # Create the destination directory if it doesn't exist
        destination_dir = os.path.dirname(destination_path)
        if destination_dir and not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            
        # Copy the file
        shutil.copy2(source_path, destination_path)
        print(f"File copied from '{source_path}' to '{destination_path}'.")
        return True
        
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")
        return False

# Example usage
if __name__ == "__main__":
    source_file = "original.txt"  # Change to your source file
    destination_file = "backup/copy.txt"  # Change to your destination
    
    copy_file(source_file, destination_file, overwrite=True)
'''
