"""
Base API Client class and implementations for various AI model providers.
Supports: Claude (Anthropic), OpenAI, Google Gemini, Hugging Face, Grok, and Deepseek.
"""
import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Define base client class
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
        project_root = Path(__file__).resolve().parent.parent
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


class DeepseekAPIClient(BaseAPIClient):
    """
    Client for interacting with the Deepseek API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Deepseek API client.
        
        Args:
            api_key: Deepseek API key. If not provided, it will be read from
                    the environment variable or .env file.
        """
        super().__init__(api_key)
        
        # Try to load from .env file explicitly
        project_root = Path(__file__).resolve().parent.parent
        env_path = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_path)
        
        # Try to get the API key
        if not self.api_key:
            self.api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "Deepseek API key not found. Please provide an API key or set the DEEPSEEK_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-coder')
        
        # API endpoint
        self.api_endpoint = "https://api.deepseek.com/v1/chat/completions"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the Deepseek model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from Deepseek based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Deepseek.
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
            error_msg = f"Error when calling Deepseek API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from Deepseek based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from Deepseek.
        """
        try:
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Prepare message list with system prompt if provided
            deepseek_messages = []
            if system_prompt:
                deepseek_messages.append({"role": "system", "content": system_prompt})
            
            # Add the conversation history
            deepseek_messages.extend(messages)
            
            data = {
                "model": self.model,
                "messages": deepseek_messages,
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
            error_msg = f"Error when calling Deepseek API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."


# Factory function to create the appropriate client
def create_api_client(provider: str, api_key: Optional[str] = None) -> BaseAPIClient:
    """
    Factory function to create an API client for the specified provider.
    
    Args:
        provider: Name of the AI provider ('claude', 'openai', 'gemini', 'huggingface', 'grok', 'deepseek')
        api_key: Optional API key for the provider
        
    Returns:
        An instance of the appropriate API client
        
    Raises:
        ValueError: If the provider is not supported
    """
    provider = provider.lower()
    
    if provider == 'claude' or provider == 'anthropic':
        return ClaudeAPIClient(api_key)
    elif provider == 'openai':
        return OpenAIAPIClient(api_key)
    elif provider == 'gemini' or provider == 'google':
        return GeminiAPIClient(api_key)
    elif provider == 'huggingface':
        return HuggingFaceAPIClient(api_key)
    elif provider == 'grok':
        return GrokAPIClient(api_key)
    elif provider == 'deepseek':
        return DeepseekAPIClient(api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

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


class OpenAIAPIClient(BaseAPIClient):
    """
    Client for interacting with the OpenAI API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI API client.
        
        Args:
            api_key: OpenAI API key. If not provided, it will be read from
                    the environment variable or .env file.
        """
        super().__init__(api_key)
        
        # Try to load from .env file explicitly
        project_root = Path(__file__).resolve().parent.parent
        env_path = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_path)
        
        # Try to get the API key
        if not self.api_key:
            self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Verify that we have an API key
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please provide an API key or set the OPENAI_API_KEY "
                "environment variable in your .env file."
            )
        
        # Set default model
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        # API endpoint
        self.api_endpoint = "https://api.openai.com/v1/chat/completions"
    
    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for queries.
        
        Args:
            model_name: The name of the OpenAI model to use.
        """
        self.model = model_name
    
    def generate_response(self, 
                          prompt: str, 
                          system_prompt: Optional[str] = None, 
                          max_tokens: int = 4000) -> str:
        """
        Generate a response from OpenAI based on the prompt.
        
        Args:
            prompt: The user's message/query.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from OpenAI.
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
                "Authorization": f"Bearer {self.api_key}"
            }
            
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
            
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
            error_msg = f"Error when calling OpenAI API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."
    
    def generate_response_with_history(self, 
                                       messages: List[Dict[str, str]], 
                                       system_prompt: Optional[str] = None,
                                       max_tokens: int = 4000) -> str:
        """
        Generate a response from OpenAI based on conversation history.
        
        Args:
            messages: List of message objects with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model's behavior.
            max_tokens: Maximum number of tokens in the response.
            
        Returns:
            The text response from OpenAI.
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
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Add system message at the beginning
            openai_messages = [{"role": "system", "content": system_instruction}]
            openai_messages.extend(messages)
            
            data = {
                "model": self.model,
                "messages": openai_messages,
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
            error_msg = f"Error when calling OpenAI API: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"API response: {e.response.text}")
            return f"I encountered an error: {error_msg}. Please check your API key and network connection."


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
        project_root = Path(__file__).resolve().parent.parent
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
        project_root = Path(__file__).resolve().parent.parent
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
        project_root = Path(__file__).resolve().parent.parent
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