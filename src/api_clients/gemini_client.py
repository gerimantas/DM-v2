"""
Client for interacting with the Google Gemini API.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

from .base_client import BaseAPIClient

class GeminiAPIClient(BaseAPIClient):
    """
    Client for interacting with the Google Gemini API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini API client.
        
        Args:
            api_key: Gemini API key. If not provided, it will be read from
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
            self.api_key = os.getenv('GEMINI_API_KEY')
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please provide an API key or set the GEMINI_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro-latest')
        
        # API endpoint base
        self.api_base = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the Gemini model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from Gemini based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Gemini.
        """
        try:
            # Construct the API endpoint for the specified model
            api_endpoint = f"{self.api_base}/{self.model}:generateContent?key={self.api_key}"
            
            # Prepare the request data
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7,
                    "topP": 0.95,
                    "topK": 40
                }
            }
            
            # Add system prompt if provided
            if system_prompt:
                data["contents"][0]["parts"].insert(0, {"text": f"System: {system_prompt}"})
            
            # Make the API call
            response = requests.post(
                api_endpoint,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract and return the response text
            return result["candidates"][0]["content"]["parts"][0]["text"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Gemini API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from Gemini based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Gemini.
        """
        try:
            # Construct the API endpoint for the specified model
            api_endpoint = f"{self.api_base}/{self.model}:generateContent?key={self.api_key}"
            
            # Convert messages to Gemini format
            contents = []
            
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
            
            # Add system prompt as a special type of user message if provided
            if system_prompt:
                contents.insert(0, {
                    "role": "user",
                    "parts": [{"text": f"System: {system_prompt}"}]
                })
            
            # Prepare the request data
            data = {
                "contents": contents,
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7,
                    "topP": 0.95,
                    "topK": 40
                }
            }
            
            # Make the API call
            response = requests.post(
                api_endpoint,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract and return the response text
            return result["candidates"][0]["content"]["parts"][0]["text"]
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Gemini API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."