# Multi-Model Support

The AI Programming Assistant now supports multiple AI model providers, allowing you to choose the best AI model for your needs.

## Supported Providers

- **Claude (Anthropic)**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- **OpenAI**: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
- **Google Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash
- **Hugging Face**: Mixtral 8x7B, Llama 3 70B, Phi-3 Mini
- **Grok (xAI)**: Grok-1
- **Deepseek**: Deepseek Coder, Deepseek Chat

## Setting Up API Keys

To use the different AI models, you'll need to provide the respective API keys:

1. Rename `.env.template` to `.env` in the project root directory
2. Add your API keys for the providers you want to use
3. Alternatively, use the "Set API Key" button in the UI to configure keys

The application will automatically store your API keys in the `.env` file.

## Selecting Models in the UI

The application interface includes a model selector at the top of the window:

1. Choose a provider from the dropdown menu
2. Select a specific model from that provider
3. Click the "?" button to see information about the selected model
4. Use the "Set API Key" button to configure your API key for the selected provider

## Model Configuration

Each provider offers different models with varying capabilities:

### Claude (Anthropic)
- **Claude 3 Opus**: Most powerful model, best for complex tasks
- **Claude 3 Sonnet**: Balance of intelligence and speed
- **Claude 3 Haiku**: Fast model for everyday tasks

### OpenAI
- **GPT-4o**: Latest and most capable model
- **GPT-4 Turbo**: Powerful general purpose model
- **GPT-3.5 Turbo**: Efficient model for most tasks

### Google Gemini
- **Gemini 1.5 Pro**: Advanced multimodal model
- **Gemini 1.5 Flash**: Faster, efficient version

### Hugging Face
- **Mixtral 8x7B**: High-quality mixture of experts model
- **Llama 3 70B**: Meta's latest large language model
- **Phi-3 Mini**: Compact but capable model

### Grok (xAI)
- **Grok-1**: First generation Grok model

### Deepseek
- **Deepseek Coder**: Specialized for code generation
- **Deepseek Chat**: General purpose chat model

## Command-Line Model Selection

When using the command-line interface, you can specify the provider and model:

```
python main.py --provider openai --model gpt-4o "Create a script that reads CSV files"
```

Or set a default in your `.env` file.

## Programmatic Usage

You can specify the provider and model when initializing the assistant:

```python
from src.assistant import ProgrammingAssistant

# Create an assistant with a specific provider and model
assistant = ProgrammingAssistant(provider="openai", model="gpt-4o")

# Or change the model later
assistant.set_model("gemini", "gemini-1.5-pro-latest")

# Generate code
response = assistant.generate_code("Create a script to download YouTube videos")
print(response)
```