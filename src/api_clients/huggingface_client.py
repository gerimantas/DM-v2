"""
Client for interacting with the Hugging Face API.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

from .base_client import BaseAPIClient

class HuggingFaceAPIClient(BaseAPIClient):
    """
    Client for interacting with the Hugging Face API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Hugging Face API client.
        
        Args:
            api_key: Hugging Face API key. If not provided, it will be read from
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
            self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "Hugging Face API key not found. Please provide an API key or set the HUGGINGFACE_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('HUGGINGFACE_MODEL', 'mistralai/Mixtral-8x7B-Instruct-v0.1')
        
        # API endpoint
        self.api_endpoint = "https://api-inference.huggingface.co/models"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name or path of the Hugging Face model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from a Hugging Face model based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from the model.
        """
        try:
            # Construct full prompt with system prompt if provided
            full_prompt = prompt
            if system_prompt:
                # Format depends on model, this is a common format for instruction models
                full_prompt = f"<s>[INST] {system_prompt}\n\n{prompt} [/INST]</s>"
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "return_full_text": False
                }
            }
            
            # Make the API call to the specific model endpoint
            response = requests.post(
                f"{self.api_endpoint}/{self.model}",
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract the generated text (format varies by model)
            if isinstance(result, list) and result:
                return result[0].get("generated_text", "")
            
            return "No response generated from the model."
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Hugging Face API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from a Hugging Face model based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from the model.
        """
        try:
            # Convert message history to a text conversation format
            conversation = ""
            
            # Add system prompt at the beginning if provided
            if system_prompt:
                conversation += f"System: {system_prompt}\n\n"
            
            # Format conversation history
            for msg in messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                conversation += f"{role}: {msg['content']}\n\n"
            
            # Add final prompt for assistant to respond
            conversation += "Assistant: "
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": conversation,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "return_full_text": False
                }
            }
            
            # Make the API call to the specific model endpoint
            response = requests.post(
                f"{self.api_endpoint}/{self.model}",
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            result = response.json()
            
            # Extract the generated text (format varies by model)
            if isinstance(result, list) and result:
                return result[0].get("generated_text", "")
            
            return "No response generated from the model."
        
        except Exception as e:
            # Handle API errors
            error_msg = f"Error when calling Hugging Face API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."