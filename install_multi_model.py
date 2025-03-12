"""
Installation script for setting up multi-model support.
This script:
1. Creates necessary directory structure
2. Copies new files to appropriate locations
3. Updates existing files
4. Creates a .env file from template if it doesn't exist
"""
import os
import shutil
from pathlib import Path
import sys

def main():
    """Run the installation process."""
    print("Installing multi-model support for AI Programming Assistant...")
    
    # Get project root directory
    project_root = Path(__file__).resolve().parent
    
    # Step 1: Create directories
    print("Creating directories...")
    
    # Create api_clients directory
    api_clients_dir = project_root / "src" / "api_clients"
    api_clients_dir.mkdir(exist_ok=True, parents=True)
    
    # Create config directory if doesn't exist
    config_dir = project_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Create UI components directory if doesn't exist
    ui_components_dir = project_root / "ui" / "components"
    ui_components_dir.mkdir(exist_ok=True, parents=True)
    
    # Step 2: Create API client files
    print("Creating API client files...")
    
    # Create __init__.py in api_clients
    with open(api_clients_dir / "__init__.py", 'w') as f:
        f.write('"""API clients for various AI model providers."""\n')
        f.write('from .base_client import BaseAPIClient\n')
        f.write('from .claude_client import ClaudeAPIClient\n')
        f.write('from .openai_client import OpenAIAPIClient\n')
        f.write('from .gemini_client import GeminiAPIClient\n')
        f.write('from .huggingface_client import HuggingFaceAPIClient\n')
        f.write('from .grok_client import GrokAPIClient\n')
        f.write('from .deepseek_client import DeepseekAPIClient\n\n')
        f.write('def create_api_client(provider, api_key=None):\n')
        f.write('    """Factory function to create API clients."""\n')
        f.write('    provider = provider.lower()\n')
        f.write('    if provider == "claude" or provider == "anthropic":\n')
        f.write('        return ClaudeAPIClient(api_key)\n')
        f.write('    elif provider == "openai":\n')
        f.write('        return OpenAIAPIClient(api_key)\n')
        f.write('    elif provider == "gemini" or provider == "google":\n')
        f.write('        return GeminiAPIClient(api_key)\n')
        f.write('    elif provider == "huggingface":\n')
        f.write('        return HuggingFaceAPIClient(api_key)\n')
        f.write('    elif provider == "grok":\n')
        f.write('        return GrokAPIClient(api_key)\n')
        f.write('    elif provider == "deepseek":\n')
        f.write('        return DeepseekAPIClient(api_key)\n')
        f.write('    else:\n')
        f.write('        raise ValueError(f"Unsupported provider: {provider}")\n')
    
    # Create individual client files
    # (Code omitted as it's already provided in the previous messages)
    
    # Step 3: Create model config
    print("Creating model configuration file...")
    # (Code omitted as it's already provided in the previous messages)
    
    # Step 4: Create model selector component
    print("Creating model selector component...")
    # (Code omitted as it's already provided in the previous messages)
    
    # Step 5: Create .env template
    print("Creating .env template...")
    env_template_path = project_root / ".env.template"
    env_path = project_root / ".env"
    
    # Create .env.template file
    # (Code omitted as it's already provided in the previous messages)
    
    # Copy template to .env if it doesn't exist
    if not env_path.exists():
        shutil.copy(env_template_path, env_path)
        print("Created .env file from template")
    
    # Step 6: Update README with multi-model information
    print("Updating README with multi-model information...")
    readme_path = project_root / "README.md"
    
    if readme_path.exists():
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        # Add multi-model section
        multi_model_section = '''
## Multi-Model Support

The AI Programming Assistant now supports multiple AI model providers, allowing you to choose the best AI model for your needs.

### Supported Providers

- **Claude (Anthropic)**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- **OpenAI**: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
- **Google Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash
- **Hugging Face**: Mixtral 8x7B, Llama 3 70B, Phi-3 Mini
- **Grok (xAI)**: Grok-1
- **Deepseek**: Deepseek Coder, Deepseek Chat

### Setting Up API Keys

To use the different AI models, you'll need to provide the respective API keys:

1. Rename `.env.template` to `.env` in the project root directory
2. Add your API keys for the providers you want to use
3. Alternatively, use the "Set API Key" button in the UI to configure keys

The application will automatically store your API keys in the `.env` file.
'''
        
        # Add the section after the Features section
        if "## Features" in readme_content:
            new_readme = readme_content.replace("## Requirements", f"{multi_model_section}\n\n## Requirements")
        else:
            new_readme = f"{readme_content}\n{multi_model_section}"
        
        with open(readme_path, 'w') as f:
            f.write(new_readme)
    
    print("\nInstallation complete! The AI Programming Assistant now supports multiple AI models.")
    print("\nAvailable providers:")
    print("- Claude (Anthropic)")
    print("- OpenAI")
    print("- Google Gemini")
    print("- Hugging Face")
    print("- Grok (xAI)")
    print("- Deepseek")
    print("\nYou'll need to add your API keys to the .env file or use the 'Set API Key' button in the UI.")
    print("Run the application with 'python run_gui.py' to get started.")

if __name__ == "__main__":
    main()