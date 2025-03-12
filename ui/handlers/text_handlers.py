"""
Text formatting handlers for the AI Programming Assistant GUI.
"""
import re


class TextHandler:
    """
    Handler for processing and formatting text for display.
    """
    
    def __init__(self, output_text):
        """
        Initialize with reference to the output text component.
        
        Args:
            output_text: Text widget where output is displayed
        """
        self.output_text = output_text
    
    def format_output(self, text):
        """
        Format the output text with code blocks highlighted.
        
        Args:
            text: The text to format.
        """
        # Split text into regular text and code blocks
        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # Code block
                code_text = part[3:-3]  # Remove the backticks
                
                # Check if language is specified
                first_line_end = code_text.find('\n')
                if first_line_end > 0:
                    first_line = code_text[:first_line_end].strip()
                    if first_line in ['python', 'py']:
                        code_text = code_text[first_line_end+1:]
                
                # Create a frame for the code block
                self.output_text.insert("end", "\n")
                
                # Insert the code block with different styling
                self.output_text.insert("end", "```\n", "code_block_marker")
                self.output_text.insert("end", code_text, "code_block")
                self.output_text.insert("end", "\n```\n", "code_block_marker")
            else:
                # Regular text
                self.output_text.insert("end", part)
        
        # Scroll to the beginning
        self.output_text.see("1.0")
    
    def clear_output(self):
        """Clear the output text."""
        self.output_text.delete("1.0", "end")


def extract_code_from_response(response):
    """
    Extract code blocks from a response text.
    
    Args:
        response: Text response that may contain code blocks
        
    Returns:
        Extracted code or None if no code found
    """
    # Find code blocks using regex
    code_blocks = re.findall(r'```(?:python)?\s*(.*?)```', response, re.DOTALL)
    
    if code_blocks:
        # Join multiple code blocks with newlines
        return '\n\n'.join(code_blocks)
    
    return None