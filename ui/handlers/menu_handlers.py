"""
Menu action handlers for the AI Programming Assistant GUI.
"""
import customtkinter as ctk
from ui.components.main_window import create_dialog, show_message_dialog


class MenuHandler:
    """
    Handler for menu actions in the GUI.
    """
    
    def __init__(self, app):
        """
        Initialize with reference to the main application.
        
        Args:
            app: Main application instance
        """
        self.app = app
    
    def show_file_menu(self):
        """Show the file menu as a popup dialog."""
        menu = create_dialog(
            self.app.root, 
            "File Menu", 
            "200x150", 
            center=False
        )
        
        # Get the position based on the button
        x = self.app.root.winfo_rootx() + 20
        y = self.app.root.winfo_rooty() + 50
        menu.geometry(f"+{x}+{y}")
        
        # Menu items
        ctk.CTkButton(
            menu, 
            text="Open File...", 
            command=lambda: [menu.destroy(), self._open_file_dialog()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Save Code...", 
            command=lambda: [menu.destroy(), self._save_code_dialog()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Clear History", 
            command=lambda: [menu.destroy(), self._clear_history()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Exit", 
            command=self.app.root.quit
        ).pack(fill="x", padx=10, pady=5)
    
    def show_tools_menu(self):
        """Show the tools menu as a popup dialog."""
        menu = create_dialog(
            self.app.root, 
            "Tools Menu", 
            "200x150", 
            center=False
        )
        
        # Get the position based on the button
        x = self.app.root.winfo_rootx() + 100
        y = self.app.root.winfo_rooty() + 50
        menu.geometry(f"+{x}+{y}")
        
        # Menu items
        ctk.CTkButton(
            menu, 
            text="Analyze Code", 
            command=lambda: [menu.destroy(), self._analyze_current_code()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Explain Code", 
            command=lambda: [menu.destroy(), self._explain_current_code()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Simplify Code", 
            command=lambda: [menu.destroy(), self._simplify_current_code()]
        ).pack(fill="x", padx=10, pady=5)
    
    def show_ocr_menu(self):
        """Show the OCR menu as a popup dialog."""
        menu = create_dialog(
            self.app.root, 
            "OCR Menu", 
            "200x190", 
            center=False
        )
        
        # Get the position based on the button
        x = self.app.root.winfo_rootx() + 140
        y = self.app.root.winfo_rooty() + 50
        menu.geometry(f"+{x}+{y}")
        
        # Toggle OCR switch
        ocr_switch_frame = ctk.CTkFrame(menu)
        ocr_switch_frame.pack(fill="x", padx=10, pady=5)
        
        ocr_switch_label = ctk.CTkLabel(
            ocr_switch_frame,
            text="Use OCR for screenshots:",
            font=("Arial", 12)
        )
        ocr_switch_label.pack(side="left", padx=5)
        
        ocr_switch = ctk.CTkSwitch(
            ocr_switch_frame,
            text="",
            command=self.app.ocr_handler.toggle_ocr,
            onvalue=True,
            offvalue=False
        )
        ocr_switch.pack(side="right", padx=5)
        
        # Set the switch according to current OCR status
        if self.app.use_ocr:
            ocr_switch.select()
        else:
            ocr_switch.deselect()
        
        # OCR menu items
        ctk.CTkButton(
            menu, 
            text="OCR Settings", 
            command=lambda: [menu.destroy(), self.app.ocr_handler.setup_ocr_settings()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Test OCR", 
            command=lambda: [menu.destroy(), self.app.ocr_handler.test_ocr()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="Extract Text From Image", 
            command=lambda: [menu.destroy(), self.app.ocr_handler.extract_text_from_image()]
        ).pack(fill="x", padx=10, pady=5)
    
    def show_help_menu(self):
        """Show the help menu as a popup dialog."""
        menu = create_dialog(
            self.app.root, 
            "Help Menu", 
            "200x100", 
            center=False
        )
        
        # Get the position based on the button
        x = self.app.root.winfo_rootx() + 180
        y = self.app.root.winfo_rooty() + 50
        menu.geometry(f"+{x}+{y}")
        
        # Menu items
        ctk.CTkButton(
            menu, 
            text="Usage Guide", 
            command=lambda: [menu.destroy(), self._show_usage_guide()]
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            menu, 
            text="About", 
            command=lambda: [menu.destroy(), self._show_about()]
        ).pack(fill="x", padx=10, pady=5)
    
    def _open_file_dialog(self):
        """Open a file dialog to select a file for analysis."""
        file_types = [("Python files", "*.py"), ("All files", "*.*")]
        file_path = ctk.filedialog.askopenfilename(
            filetypes=file_types,
            title="Open File for Analysis"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
                
                self.app.input_text.delete("1.0", "end")
                self.app.input_text.insert("1.0", code)
                
                # Set mode to analyze
                self.app.mode_var.set("analyze")
            except Exception as e:
                show_message_dialog(self.app.root, "Error", f"Failed to open file: {str(e)}")
    
    def _save_code_dialog(self):
        """Open a dialog to save the extracted code to a file."""
        if not self.app.last_code:
            show_message_dialog(self.app.root, "No Code", "No code found in the current response.")
            return
        
        # Open file dialog
        file_types = [("Python files", "*.py"), ("All files", "*.*")]
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=file_types,
            title="Save Code"
        )
        
        if file_path:
            from src.utils import save_code_to_file
            result = save_code_to_file(self.app.last_code, file_path)
            show_message_dialog(self.app.root, "Save Result", result)
    
    def _clear_history(self):
        """Clear the assistant's conversation history."""
        self.app.assistant.clear_conversation_history()
        show_message_dialog(self.app.root, "History Cleared", "Conversation history has been cleared.")
    
    def _analyze_current_code(self):
        """Analyze the code in the input text area."""
        code = self.app.input_text.get("1.0", "end").strip()
        if not code:
            show_message_dialog(self.app.root, "Empty Input", "Please enter code to analyze.")
            return
        
        self.app.mode_var.set("analyze")
        self.app.input_handler.process_input()
    
    def _explain_current_code(self):
        """Explain the code in the input text area."""
        code = self.app.input_text.get("1.0", "end").strip()
        if not code:
            show_message_dialog(self.app.root, "Empty Input", "Please enter code to explain.")
            return
        
        # Customize the prompt for explanation
        prompt = f"""Please explain this code in simple terms for someone with minimal programming knowledge:

```python
{code}
```

Break down:
1. What the code does overall
2. What each major section does
3. Any important programming concepts being used
4. How someone might modify it for their needs
"""
        
        self.app.input_text.delete("1.0", "end")
        self.app.input_text.insert("1.0", prompt)
        
        self.app.mode_var.set("general")
        self.app.input_handler.process_input()
    
    def _simplify_current_code(self):
        """Simplify the code in the input text area."""
        code = self.app.input_text.get("1.0", "end").strip()
        if not code:
            show_message_dialog(self.app.root, "Empty Input", "Please enter code to simplify.")
            return
        
        # Customize the prompt for simplification
        prompt = f"""Please simplify this code and explain it for a beginner:

```python
{code}
```

Please:
1. Create a simplified version that's easier to understand
2. Add detailed comments explaining what each line does
3. Explain any complex or advanced concepts in simple terms
4. Preserve the functionality while making the code more readable
"""
        
        self.app.input_text.delete("1.0", "end")
        self.app.input_text.insert("1.0", prompt)
        
        self.app.mode_var.set("general")
        self.app.input_handler.process_input()
    
    def _show_about(self):
        """Show the about dialog."""
        about_text = """
AI Programming Assistant v1.1

An AI-powered assistant that helps automate programming tasks by converting 
natural language task descriptions into executable Python code.

Features:
- Natural language to code conversion
- Code analysis and explanation
- OCR for extracting code from screenshots

Powered by Claude API from Anthropic and Tesseract OCR.
        """
        show_message_dialog(self.app.root, "About", about_text, width=400, height=300)
    
    def _show_usage_guide(self):
        """Show the usage guide dialog."""
        usage_dialog = create_dialog(
            self.app.root,
            "Usage Guide",
            "500x400"
        )
        
        # Create scrollable frame for the guide
        frame = ctk.CTkScrollableFrame(usage_dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        guide_text = """
Usage Guide:

1. Choose a mode:
   - General Query: Ask programming questions or get advice
   - Task to Code: Convert a task description into Python code
   - Code Analysis: Analyze existing code for improvements

2. Enter your query or code in the input area

3. Click Submit or press Ctrl+Enter to send your request

4. View the response in the output area

5. Use the Tools menu for additional features:
   - Analyze Code: Get feedback on code quality and suggestions
   - Explain Code: Get a simple explanation of how code works
   - Simplify Code: Get a beginner-friendly version of complex code

6. OCR Features:
   - Use OCR to extract text from screenshots automatically
   - Access OCR settings to configure Tesseract path
   - Test OCR with sample images
   - Extract text directly from any image file

7. Save or copy generated code using the quick action buttons

Tips:
- Be specific in your task descriptions
- Include relevant details like file formats or data structures
- Use Clear History when starting a new topic
- Use Ctrl+mouse wheel to adjust text size for better readability
- Use "Paste Screenshot" or Ctrl+V to include images from your clipboard
- Enable OCR for automatic code extraction from screenshots
        """
        
        guide_label = ctk.CTkLabel(
            frame, 
            text=guide_text,
            font=("Arial", 12),
            justify="left",
            wraplength=480
        )
        guide_label.pack(pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            usage_dialog, 
            text="OK", 
            command=usage_dialog.destroy
        )
        ok_button.pack(pady=10)