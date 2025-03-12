"""
Utility functions for the AI Programming Assistant.
"""
import re
import os
from typing import List, Optional, Dict, Any


def extract_code(text: str) -> Optional[str]:
    """
    Extract code blocks from text.
    
    Args:
        text: The text containing code blocks.
        
    Returns:
        Extracted code or None if no code found.
    """
    # Look for code blocks with triple backticks
    code_blocks = re.findall(r'```(?:python)?\n(.*?)```', text, re.DOTALL)
    
    if code_blocks:
        # Return the first code block found
        return code_blocks[0].strip()
    
    # If no code blocks with triple backticks, try to find indented code
    lines = text.split('\n')
    indented_lines = []
    in_indented_block = False
    
    for line in lines:
        if line.startswith('    ') or line.startswith('\t'):
            indented_lines.append(line)
            in_indented_block = True
        elif line.strip() == '' and in_indented_block:
            # Empty lines within indented blocks are preserved
            indented_lines.append('')
        elif in_indented_block:
            # End of indented block
            break
    
    if indented_lines:
        return '\n'.join(indented_lines)
    
    return None


def format_code(code: str) -> str:
    """
    Format code for display (add syntax highlighting markers).
    
    Args:
        code: The code to format.
        
    Returns:
        Formatted code with markdown syntax highlighting.
    """
    return f"```python\n{code}\n```"


def save_code_to_file(code: str, filename: str) -> str:
    """
    Save code to a file.
    
    Args:
        code: The code to save.
        filename: The name of the file to save to.
        
    Returns:
        Path to the saved file.
    """
    try:
        # Make sure the directory exists
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write code to file
        with open(filename, 'w') as f:
            f.write(code)
        
        return f"Code saved to {os.path.abspath(filename)}"
    except Exception as e:
        return f"Error saving code: {str(e)}"


def load_code_from_file(filename: str) -> Optional[str]:
    """
    Load code from a file.
    
    Args:
        filename: The name of the file to load from.
        
    Returns:
        The loaded code or None if file not found.
    """
    try:
        if not os.path.exists(filename):
            return None
        
        with open(filename, 'r') as f:
            return f.read()
    except Exception:
        return None


def parse_imports(code: str) -> List[str]:
    """
    Parse import statements from code.
    
    Args:
        code: The code to parse.
        
    Returns:
        List of imported modules.
    """
    imports = []
    
    # Match 'import module' and 'from module import'
    import_patterns = [
        r'import\s+([\w\.]+)',  # import module
        r'from\s+([\w\.]+)\s+import'  # from module import
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, code)
        imports.extend(matches)
    
    return imports


def suggest_docstring(function_def: str) -> str:
    """
    Generate a suggested docstring for a function.
    
    Args:
        function_def: The function definition as a string.
        
    Returns:
        A suggested docstring.
    """
    # Extract function name
    name_match = re.search(r'def\s+(\w+)\s*\(', function_def)
    if not name_match:
        return "\"\"\"Function docstring.\"\"\""
    
    function_name = name_match.group(1)
    
    # Extract parameters
    params_match = re.search(r'def\s+\w+\s*\((.*?)\):', function_def, re.DOTALL)
    if not params_match:
        return f"\"\"\"{function_name} function.\n\"\"\""
    
    params_str = params_match.group(1).strip()
    
    if not params_str or params_str == 'self':
        return f"\"\"\"{function_name} function.\n\"\"\""
    
    # Split parameters
    params = []
    for param in params_str.split(','):
        param = param.strip()
        if param and param != 'self':
            # Extract parameter name (without type hints or default values)
            param_name = param.split(':')[0].split('=')[0].strip()
            params.append(param_name)
    
    # Build docstring
    docstring = f"\"\"\"{function_name} function.\n\n"
    
    if params:
        docstring += "Args:\n"
        for param in params:
            docstring += f"    {param}: Description of {param}.\n"
    
    docstring += "\nReturns:\n    Description of return value.\n\"\"\""
    
    return docstring
