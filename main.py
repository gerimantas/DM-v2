"""
DM-v2: AI Programming Assistant
Main entry point for the application
"""
import sys
import os
import argparse
from src.assistant import ProgrammingAssistant
from ui.interface import CommandLineInterface
from config.model_config import get_default_model_for_provider


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI Programming Assistant")
    parser.add_argument("--interactive", action="store_true", help="Start in interactive mode")
    parser.add_argument("--gui", action="store_true", help="Start with graphical user interface")
    parser.add_argument("--provider", type=str, default="claude", help="AI provider to use")
    parser.add_argument("--model", type=str, help="Specific model to use")
    parser.add_argument("--query", type=str, help="Single query to the assistant")
    parser.add_argument("--task", type=str, help="Task description to convert to code")
    parser.add_argument("--file", type=str, help="File to analyze")
    return parser.parse_args()


def main():
    """Main function to run the assistant."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Check if GUI mode is requested
    if args.gui:
        try:
            # Import custom GUI here to avoid loading CustomTkinter unnecessarily
            from ui.gui_app import ProgrammingAssistantGUI
            app = ProgrammingAssistantGUI()
            app.run()
            return
        except ImportError as e:
            print(f"Error loading GUI: {e}")
            print("Falling back to interactive command-line mode.")
            args.interactive = True
    
    # Get the model if specified
    model = None
    if args.model:
        model = args.model
    
    # Initialize the assistant with specified provider and model
    assistant = ProgrammingAssistant(provider=args.provider, model=model)
    
    # Initialize the UI
    ui = CommandLineInterface(assistant)
    
    # Run in the appropriate mode
    if args.interactive:
        # Start interactive session
        ui.start_interactive_session()
    elif args.task:
        # Convert task to code
        response = assistant.convert_task_to_code(args.task)
        print(response)
    elif args.query:
        # Process a single query
        response = assistant.process_query(args.query)
        print(response)
    elif args.file:
        # Analyze a file
        if os.path.exists(args.file):
            with open(args.file, 'r') as f:
                code = f.read()
            response = assistant.analyze_code(code)
            print(response)
        else:
            print(f"Error: File {args.file} not found.")
    else:
        # By default, start interactive session
        ui.start_interactive_session()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting AI Programming Assistant...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)