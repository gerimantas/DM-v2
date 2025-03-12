# src/api_clients/__init__.py

from typing import Optional

from .base_client import BaseAPIClient
from .claude_client import ClaudeAPIClient
from .openai_client import OpenAIAPIClient
from .gemini_client import GeminiAPIClient
from .huggingface_client import HuggingFaceAPIClient
from .grok_client import GrokAPIClient
from .deepseek_client import DeepseekAPIClient

def create_api_client(provider: str, api_key: Optional[str] = None) -> BaseAPIClient:
    """
    Factory function to create an API client for the specified provider.
    
    Args:
        provider: Name of the AI provider
        api_key: Optional API key for the provider
        
    Returns:
        An instance of the appropriate API client
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