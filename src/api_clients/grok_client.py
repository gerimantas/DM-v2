"""
Client for interacting with the Grok API.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

from .base_client import BaseAPIClient

class GrokAPIClient(BaseAPIClient):
    """
    Client for interacting with the Grok API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Grok API client.
        
        Args:
            api_key: Grok API key. If not provided, it will be read from
                    the environment variable or .env file.
        """
        super().__init__(api_key)
        
        # Try to load from .env file explicitly
        project_root = Path(__file__).resolve().parent.parent.parent
        env_path = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_path)
        
        # Try to get the API key
        if not self.api_key:
            self.api_key = os.getenv('GROK_API_KEY')
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "Grok API key not found. Please provide an API key or set the GROK_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('GROK_MODEL', 'grok-1')
        
        # API endpoint
        self.api_endpoint = "https://api.grok.x/v1/chat/completions"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the Grok model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from Grok based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Grok.
        """
        try:
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens
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
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Grok API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from Grok based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Grok.
        """
        try:
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Prepare message list with system prompt if provided
            grok_messages = []
            if system_prompt:
                grok_messages.append({"role": "system", "content": system_prompt})
            
            # Add the conversation history
            grok_messages.extend(messages)
            
            data = {
                "model": self.model,
                "messages": grok_messages,
                "max_tokens": max_tokens
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
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Grok API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."