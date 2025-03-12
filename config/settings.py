"""
Configuration settings for the AI Programming Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / '.env'

# Load environment variables from .env file if present
load_dotenv(dotenv_path=env_path)

# API settings - check for both environment variable names
ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")

# System settings
MAX_HISTORY_LENGTH = 20  # Maximum number of messages to keep in conversation history
DEFAULT_MAX_TOKENS = 4000  # Default maximum tokens for responses

# File paths
DEFAULT_SAVE_PATH = "generated_code"
EXAMPLES_PATH = "examples"

# User interface settings
CLI_COLORS = {
    "user_input": "green",
    "assistant_output": "white",
    "code": "yellow",
    "error": "red",
    "info": "cyan",
    "warning": "magenta"
}

# Task templates for beginners
BEGINNER_TEMPLATES = {
    "file_read": "# Template for reading a file\n"
                "# This code reads the contents of a file and prints it\n\n"
                "file_path = 'your_file.txt'  # Change this to your file's path\n\n"
                "# Open the file and read its contents\n"
                "with open(file_path, 'r') as file:\n"
                "    content = file.read()\n\n"
                "# Print the file contents\n"
                "print(content)\n",
                
    "file_write": "# Template for writing to a file\n"
                 "# This code writes text to a file\n\n"
                 "file_path = 'output.txt'  # The file to write to\n"
                 "content = 'This is the text that will be written to the file.'\n\n"
                 "# Open the file in write mode and write the content\n"
                 "with open(file_path, 'w') as file:\n"
                 "    file.write(content)\n\n"
                 "print(f'Content written to {file_path}')\n"
}

# Task analysis helpers - keywords to identify task types
TASK_KEYWORDS = {
    "file_operations": ["file", "read", "write", "open", "save", "folder", "directory"],
    "data_processing": ["csv", "data", "filter", "sort", "analyze", "json", "parse"],
    "web_interaction": ["web", "http", "url", "api", "scrape", "download", "request"],
    "ui_creation": ["ui", "interface", "gui", "button", "window", "form", "display"],
    "automation": ["schedule", "automate", "repeat", "daily", "trigger", "cron"],
    "calculation": ["calculate", "math", "compute", "average", "sum", "statistics"]
}