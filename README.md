# AI Programming Assistant with Claude API

An AI-powered assistant that helps automate programming tasks by converting natural language task descriptions into executable Python code.

## Features

- 🧠 **AI-Powered Code Generation**: Leverages Claude API to generate high-quality Python code based on natural language task descriptions
- 📚 **Code Templates**: Pre-built templates for common programming tasks
- 🔍 **Code Analysis**: Identifies potential issues and suggests improvements
- 💻 **User-Friendly Interface**: Simple command-line interface for interacting with the assistant
- 🛠️ **Customizable**: Easily extend with new templates and functionality

## Project Structure

```
C:\ai_projects\DM_v2\
│
├── config\             # Configuration settings
├── src\                # Core functionality
├── ui\                 # User interface
├── examples\           # Example usage
├── templates\          # Pre-built code templates
├── tests\              # Unit tests
├── .env                # Environment variables (API keys)
└── main.py             # Entry point
```

## Requirements

- Python 3.8+
- Claude API key (Anthropic)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/gerimantas/DM-v2.git
   cd DM-v2
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Rename `.env.example` to `.env`
   - Add your Claude API key to the `.env` file

## Usage

### Basic Usage

Run the assistant with:

```
python main.py
```

Then follow the prompts to describe your programming task.

### Command Examples

```
# Generate code for file operations
python main.py "Create a script that reads all text files in a directory and counts word frequency"

# Generate code for data processing
python main.py "Create a script to analyze stock price data for Microsoft"

# Generate code for web interaction
python main.py "Create a script to fetch current weather for London"
```

### Advanced Usage

For more advanced options, use the UI module:

```
python -m ui.interface
```

This provides additional commands for:
- Template selection
- Code analysis
- Example browsing
- Interactive mode

## Extending the Assistant

### Adding New Templates

1. Create your template in the appropriate template file (`templates/file_operations.py`, etc.)
2. Register the template in the template registry
3. Update the template matching logic in `assistant.py`

### Customizing Prompts

Modify the system prompts in `config/settings.py` to customize how the AI generates code.

## Testing

Run tests with:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Anthropic for the Claude API
- Contributors to the open-source libraries used in this project