"""
Configuration settings for supported AI models.
Defines available models for each provider and their settings.
"""
from typing import Dict, List, Any

# Available model providers
PROVIDERS = {
    "claude": "Claude (Anthropic)",
    "openai": "OpenAI",
    "gemini": "Gemini (Google)",
    "huggingface": "Hugging Face",
    "grok": "Grok (xAI)",
    "deepseek": "Deepseek"
}

# Available models per provider
MODELS = {
    "claude": [
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "tokens": 200000, "description": "Most powerful model, best for complex tasks"},
        {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "tokens": 180000, "description": "Balance of intelligence and speed"},
        {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "tokens": 180000, "description": "Fast model for everyday tasks"},
        {"id": "claude-2.1", "name": "Claude 2.1", "tokens": 100000, "description": "Previous generation model"}
    ],
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o", "tokens": 120000, "description": "Latest and most capable model"},
        {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "tokens": 120000, "description": "Powerful general purpose model"},
        {"id": "gpt-4", "name": "GPT-4", "tokens": 8000, "description": "High-capability GPT-4 with smaller context"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "tokens": 16000, "description": "Efficient model for most tasks"}
    ],
    "gemini": [
        {"id": "gemini-1.5-pro-latest", "name": "Gemini 1.5 Pro", "tokens": 100000, "description": "Advanced multimodal model"},
        {"id": "gemini-1.5-flash-latest", "name": "Gemini 1.5 Flash", "tokens": 100000, "description": "Faster, efficient version"},
        {"id": "gemini-1.0-pro", "name": "Gemini 1.0 Pro", "tokens": 30000, "description": "Previous generation model"}
    ],
    "huggingface": [
        {"id": "mistralai/Mixtral-8x7B-Instruct-v0.1", "name": "Mixtral 8x7B", "tokens": 32000, "description": "High-quality mixture of experts model"},
        {"id": "meta-llama/Llama-3-70b-chat", "name": "Llama 3 70B", "tokens": 32000, "description": "Meta's latest large language model"},
        {"id": "microsoft/Phi-3-mini-4k-instruct", "name": "Phi-3 Mini", "tokens": 4000, "description": "Compact but capable model"}
    ],
    "grok": [
        {"id": "grok-1", "name": "Grok-1", "tokens": 8000, "description": "First generation Grok model"}
    ],
    "deepseek": [
        {"id": "deepseek-coder", "name": "Deepseek Coder", "tokens": 16000, "description": "Specialized for code generation"},
        {"id": "deepseek-chat", "name": "Deepseek Chat", "tokens": 16000, "description": "General purpose chat model"}
    ]
}

# Default system prompts optimized for each provider
DEFAULT_SYSTEM_PROMPTS = {
    "claude": """
    You are an AI programming assistant. Your goal is to help with programming tasks
    by providing clear, correct, and well-explained code and technical information.
    When writing code, include helpful comments. For beginners, explain concepts
    thoroughly and avoid jargon. Focus on Python programming best practices.
    """,
    
    "openai": """
    You are a helpful programming assistant with expertise in software development.
    Provide clear, correct, and well-commented code examples.
    Explain technical concepts in a beginner-friendly way.
    When generating code, focus on Python best practices and include explanations.
    """,
    
    "gemini": """
    As an AI programming assistant, help users write high-quality code.
    Always include detailed comments and prioritize code that follows best practices.
    For beginner programmers, explain concepts clearly and avoid complex jargon.
    When showing examples, make them practical and realistic.
    """,
    
    "huggingface": """
    You are a programming assistant. Help users write code by providing clear examples
    with helpful comments. Explain programming concepts in simple terms for beginners.
    Focus on creating clean, efficient code that follows Python best practices.
    """,
    
    "grok": """
    You are a programming assistant designed to help with coding tasks.
    Always provide well-commented code with clear explanations.
    For beginners, break down complex concepts and use simple language.
    Focus on following Python best practices in all examples.
    """,
    
    "deepseek": """
    You are a specialized coding assistant. Your primary focus is helping users write
    efficient, correct code with helpful comments. Provide beginners with clear
    explanations of programming concepts. Always follow Python best practices.
    """
}

# Provider-specific settings (like API endpoints, rate limits, etc.)
PROVIDER_SETTINGS = {
    "claude": {
        "api_endpoint": "https://api.anthropic.com/v1/messages",
        "api_version": "2023-06-01"
    },
    "openai": {
        "api_endpoint": "https://api.openai.com/v1/chat/completions"
    },
    "gemini": {
        "api_base": "https://generativelanguage.googleapis.com/v1beta/models"
    },
    "huggingface": {
        "api_endpoint": "https://api-inference.huggingface.co/models"
    },
    "grok": {
        "api_endpoint": "https://api.grok.x/v1/chat/completions"
    },
    "deepseek": {
        "api_endpoint": "https://api.deepseek.com/v1/chat/completions"
    }
}

def get_models_for_provider(provider: str) -> List[Dict[str, Any]]:
    """
    Get the list of available models for a provider.
    
    Args:
        provider: The provider name
        
    Returns:
        List of model information dictionaries
    """
    provider = provider.lower()
    return MODELS.get(provider, [])

def get_default_model_for_provider(provider: str) -> str:
    """
    Get the default model ID for a provider.
    
    Args:
        provider: The provider name
        
    Returns:
        Default model ID
    """
    provider = provider.lower()
    models = get_models_for_provider(provider)
    return models[0]["id"] if models else ""

def get_system_prompt_for_provider(provider: str) -> str:
    """
    Get the default system prompt for a provider.
    
    Args:
        provider: The provider name
        
    Returns:
        Default system prompt
    """
    provider = provider.lower()
    return DEFAULT_SYSTEM_PROMPTS.get(provider, DEFAULT_SYSTEM_PROMPTS["claude"])