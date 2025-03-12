"""
Unit tests for the API client module.
Tests API request functionality, error handling, and response processing.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.api_client import ClaudeAPIClient
from config.settings import SYSTEM_PROMPTS

class TestClaudeAPIClient(unittest.TestCase):
    """Test cases for the Claude API client."""
    
    def setUp(self):
        """Set up test fixtures before each test method is run."""
        # Create a client with a mock API key
        self.client = ClaudeAPIClient(api_key="mock_api_key")
        
        # Sample prompt for testing
        self.sample_prompt = "Write a Python function to count words in a string."
        
        # Sample API response
        self.sample_response = {
            "id": "msg_012345",
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "```python\ndef count_words(text):\n    \"\"\"\n    Count the number of words in a string.\n    \n    Args:\n        text (str): The input string\n        \n    Returns:\n        int: Number of words in the string\n    \"\"\"\n    # Handle empty strings\n    if not text or text.isspace():\n        return 0\n    \n    # Split the text by whitespace and count words\n    words = text.split()\n    return len(words)\n\n# Example usage\nif __name__ == \"__main__\":\n    sample_text = \"Hello world, this is a test string.\"\n    word_count = count_words(sample_text)\n    print(f\"Word count: {word_count}\")\n```"
                }
            ],
            "model": "claude-3-7-sonnet-20250219",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 12,
                "output_tokens": 194
            }
        }
    
    @patch('requests.post')
    def test_generate_code(self, mock_post):
        """Test that the generate_code method works correctly."""
        # Configure the mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_response
        mock_post.return_value = mock_response
        
        # Call the method
        code = self.client.generate_code(self.sample_prompt)
        
        # Verify the response was processed correctly
        self.assertIn("def count_words(text):", code)
        self.assertIn("return len(words)", code)
        
        # Verify the API was called with the correct parameters
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        
        # Check that the request body contains the expected data
        request_data = json.loads(kwargs['data'])
        self.assertEqual(request_data['model'], "claude-3-7-sonnet-20250219")
        self.assertEqual(request_data['max_tokens'], 4000)
        
        # Check that system and user messages are included
        self.assertEqual(len(request_data['messages']), 2)
        self.assertEqual(request_data['messages'][0]['role'], "system")
        self.assertEqual(request_data['messages'][1]['role'], "user")
        
    @patch('requests.post')
    def test_error_handling(self, mock_post):
        """Test that API errors are handled correctly."""
        # Configure the mock to raise an exception
        mock_post.side_effect = Exception("API connection error")
        
        # Call the method and check exception handling
        result = self.client.generate_code(self.sample_prompt)
        
        # Should return an error message
        self.assertIn("Error:", result)
        self.assertIn("API connection error", result)
    
    @patch('requests.post')
    def test_non_200_response(self, mock_post):
        """Test handling of non-200 HTTP responses."""
        # Configure a failed response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.client.generate_code(self.sample_prompt)
        
        # Should return an error message
        self.assertIn("Error:", result)
        self.assertIn("400", result)
    
    def test_extract_code_from_response(self):
        """Test that code is correctly extracted from API responses."""
        # Test with code blocks
        response_with_code = """
        Here's a function to count words:
        
        ```python
        def count_words(text):
            return len(text.split())
        ```
        
        You can use it like this:
        ```python
        result = count_words("hello world")
        print(result)  # Outputs: 2
        ```
        """
        
        extracted = self.client._extract_code_from_response(response_with_code)
        self.assertEqual(extracted.count("def count_words"), 1)
        self.assertIn("return len(text.split())", extracted)
        self.assertIn("result = count_words", extracted)
        
        # Test with no code blocks
        response_no_code = "I can't generate code for that request."
        extracted_no_code = self.client._extract_code_from_response(response_no_code)
        self.assertEqual(extracted_no_code, response_no_code)

if __name__ == '__main__':
    unittest.main()