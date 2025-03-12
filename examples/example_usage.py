"""
Example usage of the AI Programming Assistant.
This file contains practical examples of converting natural language task descriptions
into executable Python code using the assistant.
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.assistant import AIAssistant
from src.code_analyzer import CodeAnalyzer

def main():
    print("AI Programming Assistant Usage Examples")
    print("======================================\n")
    
    # Initialize the AI assistant
    assistant = AIAssistant()
    
    # Example 1: File Operations
    print("Example 1: File Operations")
    print("--------------------------")
    file_task = "Create a script that reads all text files in a directory, counts the word frequency in each file, and outputs a summary CSV"
    
    print(f"Task: {file_task}\n")
    file_code = assistant.generate_code(file_task)
    print(f"Generated Code:\n{file_code}\n")
    
    # Example 2: Data Processing
    print("Example 2: Data Processing")
    print("--------------------------")
    data_task = "Create a script that downloads stock price data for Microsoft (MSFT) for the last 30 days and plots it as a line chart"
    
    print(f"Task: {data_task}\n")
    data_code = assistant.generate_code(data_task)
    print(f"Generated Code:\n{data_code}\n")
    
    # Example 3: Web Interaction
    print("Example 3: Web Interaction")
    print("--------------------------")
    web_task = "Create a script that fetches the current weather for London from a weather API and prints a human-readable summary"
    
    print(f"Task: {web_task}\n")
    web_code = assistant.generate_code(web_task)
    print(f"Generated Code:\n{web_code}\n")
    
    # Example 4: Code Analysis
    print("Example 4: Code Analysis")
    print("-----------------------")
    sample_code = """
def calculate_stats(numbers):
    total = 0
    for num in numbers:
        total += num
    mean = total / len(numbers)
    
    squared_diffs = [(x - mean) ** 2 for x in numbers]
    variance = sum(squared_diffs) / len(numbers)
    std_dev = variance ** 0.5
    
    return mean, variance, std_dev
    """
    
    print(f"Sample Code:\n{sample_code}\n")
    
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_code(sample_code)
    
    print(f"Code Analysis:\n{analysis}\n")

if __name__ == "__main__":
    main()