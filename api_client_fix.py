"""
Fix for the API client to ensure it correctly reads the API key from .env
This is a patch that you can apply to your api_client.py file
"""

# Here's a corrected version of the init method that should fix the API key issue.
# Replace the __init__ method in your src/api_client.py file with this:

def __init__(self, api_key=None):
    """
    Initialize the Claude API client.
    
    Args:
        api_key (str, optional): Claude API key. If not provided, it will be read from
                                 the environment variable or .env file.
    """
    # Try to load from .env file explicitly
    from dotenv import load_dotenv
    import os
    from pathlib import Path
    
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / '.env'
    
    # Load the .env file
    load_dotenv(dotenv_path=env_path)
    
    # Try different ways to get the API key
    if api_key:
        self.api_key = api_key
    else:
        # Try various environment variable names that might contain the API key
        self.api_key = (os.getenv('CLAUDE_API_KEY') or 
                        os.getenv('ANTHROPIC_API_KEY'))
    
    # Verify that we have an API key
    if not self.api_key:
        raise ValueError(
            "API key not found. Please provide an API key or set the CLAUDE_API_KEY "
            "environment variable in your .env file."
        )
    
    # Initialize the Anthropic client
    self.client = Anthropic(api_key=self.api_key)
    self.model = os.getenv('CLAUDE_MODEL', 'claude-3-7-sonnet-20250219')