"""
DM-v2: AI Programming Assistant
GUI Launcher Script with CustomTkinter
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from ui.custom_gui import main

if __name__ == "__main__":
    main()