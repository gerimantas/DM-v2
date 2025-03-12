"""
Client for interacting with the Claude API.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

from .base_client import BaseAPIClient

class ClaudeAPIClient(BaseAPIClient):
    """
    Client for interacting with the Claude API using direct HTTP requests.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude API client.
        
        Args:
            api_key: Claude API key. If not provided, it will be read from
                    the environment variable or .env file.
        """
        super().__init__(api_key)
        
        # Try to load from .env file explicitly
        # Get the project root directory
        project_root = Path(__file__).resolve().parent.parent.parent
        env_path = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_path)
        
        # Try different ways to get the API key
        if not self.api_key:
            # Try various environment variable names that might contain the API key
            self.api_key = (os.getenv('CLAUDE_API_KEY') or 
                          os.getenv('ANTHROPIC_API_KEY'))
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "Claude API key not found. Please provide an API key or set the CLAUDE_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
        
        # API endpoint
        self.api_endpoint = "https://api.anthropic.com/v1/messages"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the Claude model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from Claude based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide Claude's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Claude.
        """
        try:
            # Default system prompt for programming assistance if none provided
            default_system_prompt = """
            You are an AI programming assistant. Your goal is to help with programming tasks
            by providing clear, correct, and well-explained code and technical information.
            When writing code, include helpful comments. For beginners, explain concepts
            thoroughly and avoid jargon. Focus on Python programming best practices.
            """
            
            # Use provided system prompt or default
            system_instruction = system_prompt or default_system_prompt
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "system": system_instruction,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            # Make the API call
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract and return the response text
            return result["content"][0]["text"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Claude API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                      messages: List[Dict[str, str]], 
                                      system_prompt: Optional[str] = None,
                                      max_tokens: int = 4000) -> str:
        """
        Generate a response from Claude based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide Claude's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Claude.
        """
        try:
            # Default system prompt for programming assistance if none provided
            default_system_prompt = """
            You are an AI programming assistant. Your goal is to help with programming tasks
            by providing clear, correct, and well-explained code and technical information.
            When writing code, include helpful comments. For beginners, explain concepts
            thoroughly and avoid jargon. Focus on Python programming best practices.
            """
            
            # Use provided system prompt or default
            system_instruction = system_prompt or default_system_prompt
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "system": system_instruction,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            # Make the API call
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract and return the response text
            return result["content"][0]["text"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Claude API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."