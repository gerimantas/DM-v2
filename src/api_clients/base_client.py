"""
Base API Client class for AI model providers.
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

class BaseAPIClient(ABC):
    """
    Abstract base class for AI model API clients.
    Defines common interface for all model providers.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            api_key: API key for the model provider. If not provided, will try to get it from environment.
        """
        self.api_key = api_key
        self.model = ""  # Default model will be set by subclasses
    
    @abstractmethod
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the model to use.
        """
        pass
    
    @abstractmethod
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from the model.
        """
        pass
    
    @abstractmethod
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from the model based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from the model.
        """
        pass