"""
Entry point for the AI Programming Assistant GUI.
Run this script to start the application.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import directly from the gui_app module
from ui.gui_app import ProgrammingAssistantGUI

# Run the application
if __name__ == "__main__":
    app = ProgrammingAssistantGUI()
    app.run()