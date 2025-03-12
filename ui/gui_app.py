"""
Main application class for the AI Programming Assistant GUI.
Orchestrates the various components and provides the entry point.
"""
import os
import sys
from pathlib import Path
import customtkinter as ctk

# Add project root to Python path if needed
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import components
from ui.components.main_window import create_main_window
from ui.components.input_panel import create_input_panel
from ui.components.output_panel import create_output_panel
from ui.components.menu_bar import create_menu_bar
from ui.components.model_selector import ModelSelector

# Import handlers
from ui.handlers.input_handlers import InputHandler
from ui.handlers.menu_handlers import MenuHandler
from ui.handlers.text_handlers import TextHandler
from ui.ocr.ocr_handlers import OCRHandler

# Import assistant components
from src.assistant import ProgrammingAssistant
from src.ocr_helper import OCRHelper


class ProgrammingAssistantGUI:
    """
    Graphical User Interface for the AI Programming Assistant.
    Main class that orchestrates all components.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        # Set CustomTkinter appearance
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Create the main window
        self.root = ctk.CTk()
        create_main_window(self.root, "AI Programming Assistant", "900x700", min_size=(800, 600))
        
        # Create frames
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Create UI components
        # Menu bar
        self.menu_handler = MenuHandler(self)
        create_menu_bar(self.root, self.menu_handler)
        
        # Model selector
        self.model_selector_frame = ctk.CTkFrame(self.root)
        self.model_selector_frame.pack(fill="x", padx=10, pady=5)
        self.model_selector = ModelSelector(self.model_selector_frame, self._on_model_changed)
        
        # Initialize the assistant with default provider ("claude")
        self.assistant = ProgrammingAssistant(provider="claude")
        
        # Initialize OCR helper
        self.ocr_helper = OCRHelper(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        
        # Create a temporary directory for screenshots
        self.temp_dir = Path(os.path.join(project_root, "temp"))
        self.temp_dir.mkdir(exist_ok=True)
        
        # Font size settings
        self.input_font_size = 14
        self.output_font_size = 14
        
        # Last generated code (for save functionality)
        self.last_code = ""
        
        # Status variables
        self.processing = False
        self.use_ocr = True  # Default to use OCR for screenshots
        
        # Input panel
        input_components = create_input_panel(
            self.top_frame, 
            self.input_font_size,
            lambda event: self._adjust_font_size("input", event),
            lambda event: self._handle_paste(event)
        )
        self.input_text = input_components["input_text"]
        self.mode_var = input_components["mode_var"]
        self.submit_button = input_components["submit_button"]
        self.status_label = input_components["status_label"]
        self.progress_bar = input_components["progress_bar"]
        
        # Connect submit button
        self.input_handler = InputHandler(self)
        self.submit_button.configure(command=self.input_handler.process_input)
        
        # Output panel
        output_components = create_output_panel(
            self.bottom_frame, 
            self.output_font_size,
            lambda event: self._adjust_font_size("output", event)
        )
        self.output_text = output_components["output_text"]
        
        # Text handler for formatting
        self.text_handler = TextHandler(self.output_text)
        
        # OCR handler
        self.ocr_handler = OCRHandler(self)
    
    def _on_model_changed(self, provider, model):
        """
        Handle model selection changes.
        
        Args:
            provider: The selected provider
            model: The selected model
        """
        try:
            # Update the assistant with the new model
            self.assistant.set_model(provider, model)
            self.status_label.configure(text=f"Model changed to {model}")
        except Exception as e:
            from ui.components.main_window import show_message_dialog
            show_message_dialog(self.root, "Error", f"Failed to change model: {str(e)}")
        
    def _handle_paste(self, event):
        """Handle Ctrl+V paste event to check for images."""
        return self.ocr_handler.handle_paste(event)
    
    def _adjust_font_size(self, target, event):
        """Adjust the font size in text areas."""
        if target == "input":
            if event.delta > 0:
                self.input_font_size = min(self.input_font_size + 1, 24)
            else:
                self.input_font_size = max(self.input_font_size - 1, 8)
            self.input_text.configure(font=("Arial", self.input_font_size))
        elif target == "output":
            if event.delta > 0:
                self.output_font_size = min(self.output_font_size + 1, 24)
            else:
                self.output_font_size = max(self.output_font_size - 1, 8)
            self.output_text.configure(font=("Arial", self.output_font_size))
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


# Only run if this script is executed directly
if __name__ == "__main__":
    app = ProgrammingAssistantGUI()
    app.run()