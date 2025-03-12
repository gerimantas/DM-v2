"""
Core functionality for the AI Programming Assistant.
Handles processing queries and generating responses.
Specializes in converting natural language task descriptions into code for users
with minimal programming knowledge.
"""
import os
from typing import Dict, List, Optional, Tuple
from src.api_clients import create_api_client
from src.code_analyzer import CodeAnalyzer
from src.utils import format_code, extract_code


class ProgrammingAssistant:
    """
    AI Programming Assistant that leverages Claude API to help with programming tasks.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Programming Assistant.
        
        Args:
            api_key: The API key for Claude. If not provided, will try to get it from environment.
        """
        # Initialize API client
        self.api_client = ClaudeAPIClient(api_key)
        
        # Initialize code analyzer
        self.code_analyzer = CodeAnalyzer()
        
        # Conversation history for context
        self.conversation_history = []
        
        # Task-to-code conversion templates
        self.task_templates = {
            "file_operations": "Working with files (read/write/modify)",
            "data_processing": "Processing data (filtering/transforming/analyzing)",
            "web_interaction": "Web interactions (scraping/API calls/requests)",
            "ui_creation": "Creating user interfaces",
            "automation": "Automating tasks (scheduled jobs/repeated actions)",
            "calculation": "Performing calculations or data analysis"
        }
    
    def process_query(self, query: str) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: The user's query or request.
            
        Returns:
            The assistant's response.
        """
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        # Check if natural language task conversion is needed
        if self._is_task_description(query):
            response = self.convert_task_to_code(query)
        # Check if code analysis is requested
        elif "analyze this code" in query.lower() or "review this code" in query.lower():
            # Extract code from the query if present
            code = extract_code(query)
            if code:
                response = self.analyze_code(code)
            else:
                response = "I don't see any code to analyze. Please share your code."
        else:
            # Generate programming assistance response
            system_prompt = self._create_system_prompt_for_programming()
            response = self.api_client.generate_response_with_history(
                self.conversation_history,
                system_prompt=system_prompt
            )
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def analyze_code(self, code: str) -> str:
        """
        Analyze provided code and return feedback.
        
        Args:
            code: The code to analyze.
            
        Returns:
            Analysis and feedback about the code.
        """
        # Basic analysis using the code analyzer
        analysis_results = self.code_analyzer.analyze(code)
        
        # Prepare the prompt with the code and analysis results
        prompt = f"""
        Please analyze this Python code and provide feedback:
        
        ```python
        {code}
        ```
        
        Initial analysis detected:
        - Potential issues: {', '.join(analysis_results['issues']) if analysis_results['issues'] else 'None detected'}
        - Code complexity: {analysis_results['complexity']}
        
        Please provide:
        1. An explanation of what this code does
        2. Suggestions for improvements (readability, efficiency, best practices)
        3. Any potential bugs or edge cases
        4. Improved version with explanatory comments
        """
        
        # Generate response with the API
        response = self.api_client.generate_response(prompt, self._create_system_prompt_for_code_review())
        
        return response
    
    def generate_code(self, specification: str) -> str:
        """
        Generate code based on a specification.
        
        Args:
            specification: Description of what the code should do.
            
        Returns:
            Generated code with explanations.
        """
        prompt = f"""
        Please write Python code based on the following specification:
        
        {specification}
        
        The code should be:
        1. Well-commented for a beginner to understand
        2. Follow Python best practices
        3. Include example usage
        4. Be efficient and handle edge cases
        """
        
        # Generate response with the API
        response = self.api_client.generate_response(prompt, self._create_system_prompt_for_code_generation())
        
        return response
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def _is_task_description(self, query: str) -> bool:
        """
        Determine if the query is likely a natural language task description.
        
        Args:
            query: The user's query.
            
        Returns:
            True if the query appears to be a task description, False otherwise.
        """
        # Check for task description indicators
        task_indicators = [
            "create a program", "write code", "make a script",
            "i need a program", "develop a", "build a",
            "automate", "how do i code", "how to program",
            "i want to", "can you make", "help me create"
        ]
        
        query_lower = query.lower()
        
        # Check if any task indicators are present
        for indicator in task_indicators:
            if indicator in query_lower:
                return True
                
        # If query is long enough and doesn't contain code, it's likely a task
        if len(query.split()) > 8 and not extract_code(query):
            return True
            
        return False
        
    def convert_task_to_code(self, task_description: str) -> str:
        """
        Convert a natural language task description into Python code.
        
        Args:
            task_description: Natural language description of the task.
            
        Returns:
            Response containing generated code and explanation.
        """
        # Identify the task category for better prompting
        task_category = self._identify_task_category(task_description)
        
        # Create a specific prompt for task conversion
        prompt = f"""
        I need to convert this task description into working Python code.
        I have very little programming knowledge, so the code should be well-explained.
        
        TASK DESCRIPTION:
        {task_description}
        
        IDENTIFIED CATEGORY:
        {task_category}
        
        Please:
        1. Explain what you'll create in simple terms
        2. Provide the complete Python code with detailed comments explaining each part
        3. Include step-by-step instructions on how to run the code
        4. Add simple examples of how to use/modify the code for similar tasks
        """
        
        # Generate response with the API using a specialized system prompt
        system_prompt = self._create_system_prompt_for_task_conversion()
        response = self.api_client.generate_response(prompt, system_prompt)
        
        return response
        
    def _identify_task_category(self, task_description: str) -> str:
        """
        Identify the category of the task from its description.
        
        Args:
            task_description: Natural language description of the task.
            
        Returns:
            Identified task category.
        """
        # Create a prompt to identify the task category
        category_prompt = f"""
        Identify which ONE category best matches this task description:
        
        {task_description}
        
        Categories:
        - file_operations: Working with files (read/write/modify)
        - data_processing: Processing data (filtering/transforming/analyzing)
        - web_interaction: Web interactions (scraping/API calls/requests)
        - ui_creation: Creating user interfaces
        - automation: Automating tasks (scheduled jobs/repeated actions)
        - calculation: Performing calculations or data analysis
        
        Return ONLY the category name, nothing else.
        """
        
        # Get category from API
        response = self.api_client.generate_response(category_prompt)
        
        # Extract category from response
        for category in self.task_templates:
            if category in response.lower():
                return self.task_templates[category]
        
        # Default if no category is clearly identified
        return "General programming task"
    
    def _create_system_prompt_for_programming(self) -> str:
        """Create a system prompt for general programming assistance."""
        return """
        You are an AI Programming Assistant designed to help with Python programming tasks.
        
        Guidelines for your responses:
        - Provide clear, concise explanations suitable for beginners
        - Include well-commented code examples
        - Explain programming concepts without assuming prior knowledge
        - Follow Python best practices in all code you provide
        - When appropriate, suggest resources for further learning
        - Format code blocks properly using markdown
        """
    
    def _create_system_prompt_for_code_review(self) -> str:
        """Create a system prompt specifically for code review."""
        return """
        You are an AI Programming Assistant specializing in Python code review.
        
        Guidelines for your code reviews:
        - First explain what the code does at a high level
        - Identify potential bugs, edge cases, or inefficiencies
        - Suggest improvements for readability and maintainability
        - Provide an improved version with explanatory comments
        - Highlight good practices that are already present in the code
        - Use a constructive and educational tone throughout
        """
    
    def _create_system_prompt_for_code_generation(self) -> str:
        """Create a system prompt specifically for code generation."""
        return """
        You are an AI Programming Assistant specializing in Python code generation.
        
        Guidelines for generating code:
        - Write clean, efficient, and well-commented Python code
        - Follow PEP 8 style guidelines
        - Include docstrings for functions and classes
        - Provide comprehensive error handling
        - Include example usage to demonstrate the code
        - Explain your implementation choices
        - Consider edge cases and potential issues
        """
        
    def _create_system_prompt_for_task_conversion(self) -> str:
        """Create a system prompt specifically for task-to-code conversion."""
        return """
        You are an AI Programming Assistant specializing in converting natural language task 
        descriptions into working Python code for users with minimal programming knowledge.
        
        Guidelines:
        - Write extremely well-commented code with explanations of EVERY line
        - Explain programming concepts in simple language assuming NO prior knowledge
        - Structure code in small, manageable chunks with clear purpose
        - Include simple error handling with explanations of what could go wrong
        - Provide complete, ready-to-run code that accomplishes the task
        - Add detailed instructions on how to run the code
        - Include examples of how the user might modify the code for similar tasks
        - Focus on practical solutions rather than programming theory
        - Use simple variable names that clearly indicate their purpose
        """
