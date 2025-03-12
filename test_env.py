"""
Test script to verify that environment variables are loading correctly from .env file
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parent
env_path = project_root / '.env'

print("Environment Variable Test Script")
print("===============================")
print(f"Current working directory: {os.getcwd()}")
print(f"Looking for .env file at: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

# Try to load the .env file
load_dotenv(dotenv_path=env_path)

# Check if the API key was loaded
claude_api_key = os.getenv('CLAUDE_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

if claude_api_key:
    # Mask the key for security when printing
    masked_key = claude_api_key[:4] + '*' * (len(claude_api_key) - 8) + claude_api_key[-4:]
    print(f"\nCLAUDE_API_KEY found: {masked_key}")
else:
    print("\nCLAUDE_API_KEY not found!")

if anthropic_api_key:
    # Mask the key for security when printing
    masked_key = anthropic_api_key[:4] + '*' * (len(anthropic_api_key) - 8) + anthropic_api_key[-4:]
    print(f"ANTHROPIC_API_KEY found: {masked_key}")
else:
    print("ANTHROPIC_API_KEY not found!")

# Check for model specification
claude_model = os.getenv('CLAUDE_MODEL')
if claude_model:
    print(f"CLAUDE_MODEL found: {claude_model}")
else:
    print("CLAUDE_MODEL not found!")

# Print all environment variables starting with CLAUDE_ or ANTHROPIC_
print("\nAll relevant environment variables:")
for key in os.environ:
    if key.startswith('CLAUDE_') or key.startswith('ANTHROPIC_'):
        value = os.environ[key]
        if 'KEY' in key and len(value) > 8:
            masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
            print(f"{key}={masked_value}")
        else:
            print(f"{key}={value}")

print("\nTest complete!")