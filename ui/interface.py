"""
Command Line Interface for the AI Programming Assistant.
"""
import os
import sys
import re
from typing import Optional
from colorama import init, Fore, Style

from src.assistant import ProgrammingAssistant
from src.utils import save_code_to_file, extract_code


class CommandLineInterface:
    """
    Command Line Interface for interacting with the AI Programming Assistant.
    """
    
    def __init__(self, assistant: ProgrammingAssistant):
        """
        Initialize the CLI.
        
        Args:
            assistant: The ProgrammingAssistant instance.
        """
        # Initialize colorama for cross-platform colored output
        init()
        
        self.assistant = assistant
        self.running = False
        
        # Special commands
        self.commands = {
            "/help": self._show_help,
            "/exit": self._exit,
            "/clear": self._clear_history,
            "/save": self._save_last_code,
            "/analyze": self._analyze_file,
            "/task": self._convert_task,
            "/explain": self._explain_code,
            "/simplify": self._simplify_code
        }
    
    def start_interactive_session(self) -> None:
        """Start an interactive session with the assistant."""
        self.running = True
        
        # Print welcome message
        self._print_colored("Welcome to the AI Programming Assistant!", Fore.CYAN)
        self._print_colored("Type '/help' to see available commands or enter your query.", Fore.CYAN)
        print()  # Empty line for better readability
        
        # Main interaction loop
        while self.running:
            try:
                # Get user input
                user_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}")
                print()  # Empty line for better readability
                
                # Check if input is a special command
                if user_input.strip().startswith("/"):
                    command = user_input.split()[0].lower()
                    args = user_input[len(command):].strip()
                    
                    if command in self.commands:
                        self.commands[command](args)
                    else:
                        self._print_colored(f"Unknown command: {command}", Fore.RED)
                        self._print_colored("Type '/help' to see available commands.", Fore.YELLOW)
                elif user_input.strip():
                    # Process regular query
                    self._print_colored("Processing your request...", Fore.YELLOW)
                    response = self.assistant.process_query(user_input)
                    
                    # Format and print response
                    self._print_response(response)
                
                print()  # Empty line for better readability
            
            except KeyboardInterrupt:
                self._print_colored("\nExiting...", Fore.YELLOW)
                self.running = False
            except Exception as e:
                self._print_colored(f"An error occurred: {str(e)}", Fore.RED)
                
    def _print_colored(self, text: str, color: str) -> None:
        """
        Print text with specified color.
        
        Args:
            text: The text to print.
            color: The color to use.
        """
        print(f"{color}{text}{Style.RESET_ALL}")
    
    def _print_response(self, response: str) -> None:
        """
        Format and print the assistant's response.
        
        Args:
            response: The assistant's response.
        """
        # Format code blocks with syntax highlighting
        code_blocks = re.findall(r'```(.*?)```', response, re.DOTALL)
        formatted_response = response
        
        for block in code_blocks:
            language = ""
            content = block
            
            # Check if the block specifies a language
            if block.startswith('python\n'):
                language = 'python'
                content = block[7:]  # Remove 'python\n'
            
            if language == 'python':
                # Highlight Python code
                highlighted_block = f"{Fore.YELLOW}```python{Style.RESET_ALL}\n"
                for line in content.split('\n'):
                    # Simple syntax highlighting
                    line = re.sub(r'\b(def|class|import|from|if|else|elif|for|while|try|except|return|with|as|in|is|and|or|not|True|False|None)\b', f"{Fore.BLUE}\\1{Style.RESET_ALL}", line)
                    line = re.sub(r'(#.*)$', f"{Fore.GREEN}\\1{Style.RESET_ALL}", line)
                    line = re.sub(r'(".*?"|\'.*?\')', f"{Fore.MAGENTA}\\1{Style.RESET_ALL}", line)
                    highlighted_block += line + '\n'
                highlighted_block += f"{Fore.YELLOW}```{Style.RESET_ALL}"
                
                formatted_response = formatted_response.replace(f"```{block}```", highlighted_block)
        
        # Print the formatted response
        print(formatted_response)
    
    def _show_help(self, args: str) -> None:
        """
        Show help information.
        
        Args:
            args: Arguments (not used).
        """
        help_text = f"""
{Fore.CYAN}=== AI Programming Assistant Help ==={Style.RESET_ALL}

{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
  {Fore.GREEN}/help{Style.RESET_ALL}      - Show this help message
  {Fore.GREEN}/exit{Style.RESET_ALL}      - Exit the assistant
  {Fore.GREEN}/clear{Style.RESET_ALL}     - Clear conversation history
  {Fore.GREEN}/save{Style.RESET_ALL}      - Save the last code snippet to a file
  {Fore.GREEN}/analyze{Style.RESET_ALL}   - Analyze code in a file (e.g., /analyze path/to/file.py)
  {Fore.GREEN}/task{Style.RESET_ALL}      - Convert a task description to code (e.g., /task Create a program that counts words in a file)
  {Fore.GREEN}/explain{Style.RESET_ALL}   - Explain how a piece of code works (e.g., /explain path/to/file.py)
  {Fore.GREEN}/simplify{Style.RESET_ALL}  - Simplify and explain a piece of code (e.g., /simplify path/to/file.py)

{Fore.YELLOW}How to Use:{Style.RESET_ALL}
  - Type your programming questions or requests normally
  - For best results, be specific about what you want to achieve
  - Describe programming tasks in plain language - no programming knowledge required
  - The assistant will provide well-commented code with explanations

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  "How do I read data from a CSV file?"
  "Create a program that downloads images from a website"
  "I need code to rename all files in a folder"
  "What's wrong with this code: [paste code here]"
  "/task Create a program that sends daily weather notifications"
"""
        print(help_text)
    
    def _exit(self, args: str) -> None:
        """
        Exit the assistant.
        
        Args:
            args: Arguments (not used).
        """
        self._print_colored("Goodbye! Thank you for using the AI Programming Assistant.", Fore.CYAN)
        self.running = False
    
    def _clear_history(self, args: str) -> None:
        """
        Clear conversation history.
        
        Args:
            args: Arguments (not used).
        """
        self.assistant.clear_conversation_history()
        self._print_colored("Conversation history cleared.", Fore.YELLOW)
    
    def _save_last_code(self, args: str) -> None:
        """
        Save the last code snippet to a file.
        
        Args:
            args: File path for saving the code.
        """
        # Find the last code block in the conversation history
        code = None
        
        for message in reversed(self.assistant.conversation_history):
            if message["role"] == "assistant":
                extracted_code = extract_code(message["content"])
                if extracted_code:
                    code = extracted_code
                    break
        
        if not code:
            self._print_colored("No code found in the recent conversation.", Fore.RED)
            return
        
        # Get filename from args or use default
        filename = args.strip() if args.strip() else "generated_code.py"
        
        # Save the code
        result = save_code_to_file(code, filename)
        self._print_colored(result, Fore.GREEN)
    
    def _analyze_file(self, args: str) -> None:
        """
        Analyze code in a file.
        
        Args:
            args: Path to the file to analyze.
        """
        filename = args.strip()
        
        if not filename:
            self._print_colored("Please specify a file to analyze. Example: /analyze path/to/file.py", Fore.RED)
            return
        
        try:
            with open(filename, 'r') as f:
                code = f.read()
            
            self._print_colored(f"Analyzing {filename}...", Fore.YELLOW)
            response = self.assistant.analyze_code(code)
            self._print_response(response)
        except FileNotFoundError:
            self._print_colored(f"File not found: {filename}", Fore.RED)
        except Exception as e:
            self._print_colored(f"Error analyzing file: {str(e)}", Fore.RED)
            
    def _convert_task(self, args: str) -> None:
        """
        Convert a task description to code.
        
        Args:
            args: Task description.
        """
        if not args.strip():
            self._print_colored("Please provide a task description. Example: /task Create a program that counts words in a file", Fore.RED)
            return
        
        self._print_colored("Converting your task to code...", Fore.YELLOW)
        response = self.assistant.convert_task_to_code(args)
        self._print_response(response)
    
    def _explain_code(self, args: str) -> None:
        """
        Explain how a piece of code works.
        
        Args:
            args: Path to the file containing code to explain.
        """
        filename = args.strip()
        
        if not filename:
            self._print_colored("Please specify a file to explain. Example: /explain path/to/file.py", Fore.RED)
            return
        
        try:
            with open(filename, 'r') as f:
                code = f.read()
            
            self._print_colored(f"Explaining {filename}...", Fore.YELLOW)
            
            prompt = f"""
            Please explain this code in simple terms for someone with minimal programming knowledge:
            
            ```python
            {code}
            ```
            
            Break down:
            1. What the code does overall
            2. What each major section does
            3. Any important programming concepts being used
            4. How someone might modify it for their needs
            """
            
            response = self.assistant.api_client.generate_response(prompt)
            self._print_response(response)
        except FileNotFoundError:
            self._print_colored(f"File not found: {filename}", Fore.RED)
        except Exception as e:
            self._print_colored(f"Error explaining file: {str(e)}", Fore.RED)
    
    def _simplify_code(self, args: str) -> None:
        """
        Simplify and explain a piece of code.
        
        Args:
            args: Path to the file containing code to simplify.
        """
        filename = args.strip()
        
        if not filename:
            self._print_colored("Please specify a file to simplify. Example: /simplify path/to/file.py", Fore.RED)
            return
        
        try:
            with open(filename, 'r') as f:
                code = f.read()
            
            self._print_colored(f"Simplifying {filename}...", Fore.YELLOW)
            
            prompt = f"""
            Please simplify this code and explain it for a beginner:
            
            ```python
            {code}
            ```
            
            Please:
            1. Create a simplified version that's easier to understand
            2. Add detailed comments explaining what each line does
            3. Explain any complex or advanced concepts in simple terms
            4. Preserve the functionality while making the code more readable
            """
            
            response = self.assistant.api_client.generate_response(prompt)
            self._print_response(response)
        except FileNotFoundError:
            self._print_colored(f"File not found: {filename}", Fore.RED)
        except Exception as e:
            self._print_colored(f"Error simplifying file: {str(e)}", Fore.RED)