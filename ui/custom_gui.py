"""
Graphical User Interface for the AI Programming Assistant using CustomTkinter.
Provides a modern-looking GUI for interacting with the assistant.
"""
import os
import sys
import re
from threading import Thread
from pathlib import Path

# Add project root to Python path if needed
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import CustomTkinter
import customtkinter as ctk

# Import assistant components
from src.assistant import ProgrammingAssistant
from src.utils import save_code_to_file, extract_code


class ProgrammingAssistantGUI:
    """
    Graphical User Interface for the AI Programming Assistant.
    """
    
    def __init__(self):
        """Initialize the GUI."""
        # Set CustomTkinter appearance
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("AI Programming Assistant")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize the assistant
        self.assistant = ProgrammingAssistant()
        
        # Last generated code (for save functionality)
        self.last_code = ""
        
        # Create UI elements
        self._create_ui()
        
        # Status variables
        self.processing = False
    
    def _create_ui(self):
        """Create and arrange the UI widgets."""
        # Create main frame with padding
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create top frame for input
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Input label
        input_label = ctk.CTkLabel(
            self.top_frame, 
            text="Enter your programming task or question:",
            font=("Arial", 14)
        )
        input_label.pack(anchor="w", pady=(0, 5))
        
        # Input text area
        self.input_text = ctk.CTkTextbox(
            self.top_frame, 
            height=150,
            font=("Arial", 12),
            wrap="word"
        )
        self.input_text.pack(fill="x", pady=(0, 10))
        
        # Mode selection frame
        mode_frame = ctk.CTkFrame(self.top_frame)
        mode_frame.pack(fill="x", pady=(0, 10))
        
        mode_label = ctk.CTkLabel(mode_frame, text="Mode:", font=("Arial", 12))
        mode_label.pack(side="left", padx=(0, 5))
        
        # Radio buttons for mode selection
        self.mode_var = ctk.StringVar(value="general")
        
        general_radio = ctk.CTkRadioButton(
            mode_frame, 
            text="General Query", 
            variable=self.mode_var, 
            value="general",
            font=("Arial", 12)
        )
        general_radio.pack(side="left", padx=5)
        
        task_radio = ctk.CTkRadioButton(
            mode_frame, 
            text="Task to Code", 
            variable=self.mode_var, 
            value="task",
            font=("Arial", 12)
        )
        task_radio.pack(side="left", padx=5)
        
        analyze_radio = ctk.CTkRadioButton(
            mode_frame, 
            text="Code Analysis", 
            variable=self.mode_var, 
            value="analyze",
            font=("Arial", 12)
        )
        analyze_radio.pack(side="left", padx=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.top_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Submit button
        self.submit_button = ctk.CTkButton(
            button_frame, 
            text="Submit", 
            command=self._process_input,
            font=("Arial", 12)
        )
        self.submit_button.pack(side="left", padx=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            button_frame, 
            text="Ready",
            font=("Arial", 12)
        )
        self.status_label.pack(side="left", padx=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(button_frame, width=200)
        self.progress_bar.pack(side="left", padx=10)
        self.progress_bar.set(0)  # Set initial value to 0
        
        # Quick actions frame
        actions_frame = ctk.CTkFrame(self.top_frame)
        actions_frame.pack(fill="x", pady=(0, 10))
        
        # Action buttons
        save_button = ctk.CTkButton(
            actions_frame, 
            text="Save Code", 
            command=self._save_code_dialog,
            font=("Arial", 12)
        )
        save_button.pack(side="left", padx=(0, 5))
        
        copy_button = ctk.CTkButton(
            actions_frame, 
            text="Copy Code", 
            command=self._copy_code,
            font=("Arial", 12)
        )
        copy_button.pack(side="left", padx=5)
        
        clear_button = ctk.CTkButton(
            actions_frame, 
            text="Clear Output", 
            command=self._clear_output,
            font=("Arial", 12)
        )
        clear_button.pack(side="left", padx=5)
        
        # Create bottom frame for output
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Output label
        output_label = ctk.CTkLabel(
            self.bottom_frame, 
            text="Assistant Response:",
            font=("Arial", 14)
        )
        output_label.pack(anchor="w", pady=(0, 5))
        
        # Output text area
        self.output_text = ctk.CTkTextbox(
            self.bottom_frame, 
            font=("Arial", 12),
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True)
        
        # Create menu bar
        self._create_menu()
        
        # Bind events
        self.input_text.bind("<Control-Return>", lambda event: self._process_input())
    
    def _create_menu(self):
        """Create the menu items using buttons at the top of the window."""
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        # File operations menu button
        file_button = ctk.CTkButton(
            menu_frame, 
            text="File", 
            command=self._show_file_menu,
            font=("Arial", 12),
            width=80
        )
        file_button.pack(side="left", padx=(0, 5))
        
        # Tools menu button
        tools_button = ctk.CTkButton(
            menu_frame, 
            text="Tools", 
            command=self._show_tools_menu,
            font=("Arial", 12),
            width=80
        )
        tools_button.pack(side="left", padx=5)
        
        # Help menu button
        help_button = ctk.CTkButton(
            menu_frame, 
            text="Help", 
            command=self._show_help_menu,
            font=("Arial", 12),
            width=80
        )
        help_button.pack(side="left", padx=5)
    
    def _show_file_menu(self):
        """Show the file menu as a popup dialog."""
        menu = ctk.CTkToplevel(self.root)
        menu.title("File Menu")
        menu.geometry("200x150")
        menu.resizable(False, False)
        menu.attributes("-topmost", True)
        
        # Get the position of the main window
        x = self.root.winfo_rootx() + 20
        y = self.root.winfo_rooty() + 50
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
            command=self.root.quit
        ).pack(fill="x", padx=10, pady=5)
    
    def _show_tools_menu(self):
        """Show the tools menu as a popup dialog."""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Tools Menu")
        menu.geometry("200x150")
        menu.resizable(False, False)
        menu.attributes("-topmost", True)
        
        # Get the position of the main window
        x = self.root.winfo_rootx() + 100
        y = self.root.winfo_rooty() + 50
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
    
    def _show_help_menu(self):
        """Show the help menu as a popup dialog."""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Help Menu")
        menu.geometry("200x100")
        menu.resizable(False, False)
        menu.attributes("-topmost", True)
        
        # Get the position of the main window
        x = self.root.winfo_rootx() + 180
        y = self.root.winfo_rooty() + 50
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
    
    def _process_input(self):
        """Process the user input and display the response."""
        if self.processing:
            return
        
        user_input = self.input_text.get("1.0", "end").strip()
        if not user_input:
            self._show_message("Empty Input", "Please enter a task or question.")
            return
        
        # Start processing
        self.processing = True
        self.status_label.configure(text="Processing...")
        self.submit_button.configure(state="disabled")
        self.progress_bar.start()
        
        # Clear the output text for new response
        self.output_text.delete("1.0", "end")
        
        # Run in a separate thread to keep UI responsive
        thread = Thread(target=self._process_in_thread, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _process_in_thread(self, user_input):
        """
        Process the user input in a separate thread.
        
        Args:
            user_input: The user's input text.
        """
        try:
            # Determine which method to call based on selected mode
            mode = self.mode_var.get()
            
            if mode == "task":
                response = self.assistant.convert_task_to_code(user_input)
            elif mode == "analyze":
                # Check if the input is a file path or code snippet
                if os.path.exists(user_input):
                    with open(user_input, 'r') as f:
                        code = f.read()
                else:
                    code = user_input
                response = self.assistant.analyze_code(code)
            else:  # general
                response = self.assistant.process_query(user_input)
            
            # Extract code from response if present
            self.last_code = extract_code(response) or ""
            
            # Update UI in the main thread
            self.root.after(0, lambda: self._update_output(response))
        except Exception as e:
            error_message = f"Error processing your request: {str(e)}"
            self.root.after(0, lambda: self._update_output(error_message, is_error=True))
        finally:
            # Reset processing state
            self.processing = False
            self.root.after(0, self._reset_ui)
    
    def _update_output(self, text, is_error=False):
        """
        Update the output text with formatting.
        
        Args:
            text: The text to display.
            is_error: Whether the text is an error message.
        """
        self.output_text.delete("1.0", "end")
        
        if is_error:
            self.output_text.insert("end", text)
        else:
            # Process the text for formatting
            self._format_output(text)
    
    def _format_output(self, text):
        """
        Format the output text with code blocks highlighted.
        
        Args:
            text: The text to format.
        """
        # Split text into regular text and code blocks
        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # Code block
                code_text = part[3:-3]  # Remove the backticks
                
                # Check if language is specified
                first_line_end = code_text.find('\n')
                if first_line_end > 0:
                    first_line = code_text[:first_line_end].strip()
                    if first_line in ['python', 'py']:
                        code_text = code_text[first_line_end+1:]
                
                # Create a frame for the code block
                self.output_text.insert("end", "\n")
                
                # Insert the code block with different styling
                self.output_text.insert("end", "```\n", "code_block_marker")
                self.output_text.insert("end", code_text, "code_block")
                self.output_text.insert("end", "\n```\n", "code_block_marker")
            else:
                # Regular text
                self.output_text.insert("end", part)
        
        # Scroll to the beginning
        self.output_text.see("1.0")
    
    def _reset_ui(self):
        """Reset the UI after processing."""
        self.submit_button.configure(state="normal")
        self.progress_bar.stop()
        self.status_label.configure(text="Ready")
    
    def _save_code_dialog(self):
        """Open a dialog to save the extracted code to a file."""
        if not self.last_code:
            self._show_message("No Code", "No code found in the current response.")
            return
        
        # Open file dialog
        file_types = [("Python files", "*.py"), ("All files", "*.*")]
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=file_types,
            title="Save Code"
        )
        
        if file_path:
            result = save_code_to_file(self.last_code, file_path)
            self._show_message("Save Result", result)
    
    def _copy_code(self):
        """Copy the last generated code to clipboard."""
        if not self.last_code:
            self._show_message("No Code", "No code found in the current response.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_code)
        self._show_message("Code Copied", "Code has been copied to clipboard.")
    
    def _clear_output(self):
        """Clear the output text area."""
        self.output_text.delete("1.0", "end")
    
    def _clear_history(self):
        """Clear the assistant's conversation history."""
        self.assistant.clear_conversation_history()
        self._show_message("History Cleared", "Conversation history has been cleared.")
    
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
                
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", code)
                
                # Set mode to analyze
                self.mode_var.set("analyze")
            except Exception as e:
                self._show_message("Error", f"Failed to open file: {str(e)}")
    
    def _analyze_current_code(self):
        """Analyze the code in the input text area."""
        code = self.input_text.get("1.0", "end").strip()
        if not code:
            self._show_message("Empty Input", "Please enter code to analyze.")
            return
        
        self.mode_var.set("analyze")
        self._process_input()
    
    def _explain_current_code(self):
        """Explain the code in the input text area."""
        code = self.input_text.get("1.0", "end").strip()
        if not code:
            self._show_message("Empty Input", "Please enter code to explain.")
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
        
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", prompt)
        
        self.mode_var.set("general")
        self._process_input()
    
    def _simplify_current_code(self):
        """Simplify the code in the input text area."""
        code = self.input_text.get("1.0", "end").strip()
        if not code:
            self._show_message("Empty Input", "Please enter code to simplify.")
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
        
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", prompt)
        
        self.mode_var.set("general")
        self._process_input()
    
    def _show_message(self, title, message):
        """Show a message dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        
        # Center the dialog on the main window
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")
        
        # Message
        message_label = ctk.CTkLabel(
            dialog, 
            text=message,
            wraplength=280
        )
        message_label.pack(pady=(20, 0))
        
        # OK button
        ok_button = ctk.CTkButton(
            dialog, 
            text="OK", 
            command=dialog.destroy
        )
        ok_button.pack(pady=20)
    
    def _show_about(self):
        """Show the about dialog."""
        about_text = """
AI Programming Assistant v1.0

An AI-powered assistant that helps automate programming tasks by converting 
natural language task descriptions into executable Python code.

Powered by Claude API from Anthropic.
        """
        self._show_message("About", about_text)
    
    def _show_usage_guide(self):
        """Show the usage guide dialog."""
        usage_dialog = ctk.CTkToplevel(self.root)
        usage_dialog.title("Usage Guide")
        usage_dialog.geometry("500x400")
        usage_dialog.attributes("-topmost", True)
        
        # Center the dialog on the main window
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - 200
        usage_dialog.geometry(f"+{x}+{y}")
        
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

6. Save or copy generated code using the quick action buttons

Tips:
- Be specific in your task descriptions
- Include relevant details like file formats or data structures
- Use Clear History when starting a new topic
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
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main function to run the GUI."""
    app = ProgrammingAssistantGUI()
    app.run()


if __name__ == "__main__":
    main()