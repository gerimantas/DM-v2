"""
Unit tests for the AIAssistant class.
Tests the task processing, code generation, and template integration functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.assistant import AIAssistant
from src.api_client import ClaudeAPIClient

class TestAIAssistant(unittest.TestCase):
    """Test cases for the AI Programming Assistant."""
    
    def setUp(self):
        """Set up test fixtures before each test method is run."""
        # Create assistant with a mock API client
        with patch('src.api_client.ClaudeAPIClient') as mock_client_class:
            self.mock_api_client = mock_client_class.return_value
            self.assistant = AIAssistant(api_client=self.mock_api_client)
        
        # Sample task for testing
        self.sample_task = "Create a function to read a CSV file and calculate the average of a specific column"
        
        # Sample code response
        self.sample_code = """
import pandas as pd

def calculate_column_average(file_path, column_name):
    '''
    Reads a CSV file and calculates the average of a specific column.
    
    Args:
        file_path (str): Path to the CSV file
        column_name (str): Name of the column to calculate average for
        
    Returns:
        float: The average value of the specified column
    '''
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the CSV file")
    
    # Calculate the average of the specified column
    average = df[column_name].mean()
    
    return average

# Example usage
if __name__ == "__main__":
    file_path = "data.csv"
    column_name = "value"
    avg = calculate_column_average(file_path, column_name)
    print(f"The average of column '{column_name}' is: {avg}")
"""
    
    def test_init(self):
        """Test that the assistant initializes correctly."""
        # Test with default parameters (using mock from setUp)
        self.assertIsNotNone(self.assistant)
        
        # Test with explicit API client
        with patch('src.api_client.ClaudeAPIClient') as mock_client_class:
            mock_client = mock_client_class.return_value
            assistant = AIAssistant(api_client=mock_client)
            self.assertEqual(assistant.api_client, mock_client)
        
        # Test create_api_client method is called when no client is provided
        with patch('src.assistant.AIAssistant.create_api_client') as mock_create:
            mock_create.return_value = "mock_client"
            assistant = AIAssistant()
            mock_create.assert_called_once()
            self.assertEqual(assistant.api_client, "mock_client")
    
    def test_create_api_client(self):
        """Test the create_api_client method."""
        with patch('src.assistant.ClaudeAPIClient') as mock_client_class:
            mock_client_class.return_value = "new_client"
            client = self.assistant.create_api_client()
            self.assertEqual(client, "new_client")
            mock_client_class.assert_called_once()
    
    def test_generate_code(self):
        """Test the generate_code method."""
        # Configure the mock API client
        self.mock_api_client.generate_code.return_value = self.sample_code
        
        # Call the method
        result = self.assistant.generate_code(self.sample_task)
        
        # Verify the API client was called correctly
        self.mock_api_client.generate_code.assert_called_once_with(self.sample_task)
        
        # Verify the result
        self.assertEqual(result, self.sample_code)
    
    def test_enhance_prompt(self):
        """Test the enhance_prompt method."""
        # Test basic prompt enhancement
        enhanced = self.assistant.enhance_prompt("Create a function to read a file")
        self.assertIn("Create a function to read a file", enhanced)
        
        # Test with language specification
        enhanced_py = self.assistant.enhance_prompt(
            "Create a function to read a file", 
            language="Python"
        )
        self.assertIn("Python", enhanced_py)
        
        # Test with example specification
        enhanced_with_example = self.assistant.enhance_prompt(
            "Create a function to read a file",
            include_example=True
        )
        self.assertIn("example", enhanced_with_example.lower())
    
    def test_suggest_template(self):
        """Test the suggest_template method."""
        # Test file operations case
        file_task = "Create a script to read all files in a directory"
        template_info = self.assistant.suggest_template(file_task)
        self.assertEqual(template_info["template_type"], "file_operations")
        
        # Test data processing case
        data_task = "Process CSV data and calculate statistics"
        template_info = self.assistant.suggest_template(data_task)
        self.assertEqual(template_info["template_type"], "data_processing")
        
        # Test web interaction case
        web_task = "Create a script to download data from a website"
        template_info = self.assistant.suggest_template(web_task)
        self.assertEqual(template_info["template_type"], "web_interaction")
        
        # Test case with no matching template
        random_task = "Create a game of tic-tac-toe"
        template_info = self.assistant.suggest_template(random_task)
        self.assertIsNone(template_info["template_type"])
    
    @patch('builtins.print')
    def test_process_task(self, mock_print):
        """Test the process_task method."""
        # Configure the mock API client
        self.mock_api_client.generate_code.return_value = self.sample_code
        
        # Mock the suggest_template method
        with patch.object(self.assistant, 'suggest_template') as mock_suggest:
            mock_suggest.return_value = {
                "template_type": "data_processing",
                "template_name": "csv_processing",
                "confidence": 0.9
            }
            
            # Call the method
            result = self.assistant.process_task(self.sample_task)
            
            # Verify suggest_template was called
            mock_suggest.assert_called_once_with(self.sample_task)
            
            # Verify generate_code was called with enhanced prompt
            self.mock_api_client.generate_code.assert_called_once()
            
            # Check the result
            self.assertEqual(result, self.sample_code)
            
            # Verify that print was called with template information
            mock_print.assert_any_call("Suggested template: data_processing (csv_processing)")

if __name__ == '__main__':
    unittest.main()