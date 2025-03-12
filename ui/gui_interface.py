"""
Graphical User Interface for the AI Programming Assistant.
Provides a simple GUI for interacting with the assistant.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
from threading import Thread
from pathlib import Path

# Add project root to Python path if needed
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.assistant import ProgrammingAssistant
from src.utils import save_code_to_file, extract_code


class ProgrammingAssistantGUI:
    """
    Graphical User Interface for the AI Programming Assistant.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("AI Programming Assistant")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize the assistant
        self.assistant = ProgrammingAssistant()
        
        # Last generated code (for save functionality)
        self.last_code = ""
        
        # Create UI elements
        self._create_menu()
        self._create_widgets()
        self._setup_tags()
        
        # Status variables
        self.processing = False
    
    def _create_menu(self):
        """Create the application menu."""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Code...", command=self._save_code_dialog)
        file_menu.add_command(label="Open File for Analysis...", command=self._open_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Clear Input", command=lambda: self.input_text.delete(1.0, tk.END))
        edit_menu.add_command(label="Clear Output", command=lambda: self.output_text.delete(1.0, tk.END))
        edit_menu.add_command(label="Clear History", command=self._clear_history)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Analyze Code", command=self._analyze_current_code)
        tools_menu.add_command(label="Explain Code", command=self._explain_current_code)
        tools_menu.add_command(label="Simplify Code", command=self._simplify_current_code)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Usage Guide", command=self._show_usage_guide)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def _create_widgets(self):
        """Create and arrange the UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input label and text area
        input_label = ttk.Label(main_frame, text="Enter your programming task or question:")
        input_label.pack(anchor="w", pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        
        # Mode selection frame
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_label = ttk.Label(mode_frame, text="Mode:")
        mode_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.mode_var = tk.StringVar(value="general")
        modes = [
            ("General Query", "general"),
            ("Task to Code", "task"),
            ("Code Analysis", "analyze")
        ]
        
        for text, value in modes:
            ttk.Radiobutton(mode_frame, text=text, variable=self.mode_var, value=value).pack(side=tk.LEFT, padx=5)
        
        # Submit button with processing indicator
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.submit_button = ttk.Button(button_frame, text="Submit", command=self._process_input)
        self.submit_button.pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(button_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=10)
        
        self.progress_bar = ttk.Progressbar(button_frame, mode="indeterminate", length=200)
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        
        # Quick actions frame
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(actions_frame, text="Save Code", command=self._save_code_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Copy Code", command=self._copy_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Clear", command=lambda: self.output_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Output label and text area
        output_label = ttk.Label(main_frame, text="Assistant Response:")
        output_label.pack(anchor="w", pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, height=20, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Make output text read-only
        self.output_text.config(state=tk.DISABLED)
        
        # Bind events
        self.input_text.bind("<Control-Return>", lambda event: self._process_input())
    
    def _setup_tags(self):
        """Set up text tags for syntax highlighting."""
        # Configure text tags for syntax highlighting
        self.output_text.tag_configure("code_block", background="#f0f0f0", font=("Courier", 10))
        self.output_text.tag_configure("keyword", foreground="#0000FF")
        self.output_text.tag_configure("string", foreground="#008000")
        self.output_text.tag_configure("comment", foreground="#808080", font=("Courier", 10, "italic"))
        self.output_text.tag_configure("normal", font=("Arial", 10))
        self.output_text.tag_configure("heading", font=("Arial", 12, "bold"))
    
    def _process_input(self):
        """Process the user input and display the response."""
        if self.processing:
            return
        
        user_input = self.input_text.get(1.0, tk.END).strip()
        if not user_input:
            messagebox.showinfo("Empty Input", "Please enter a task or question.")
            return
        
        # Start processing
        self.processing = True
        self.status_var.set("Processing...")
        self.submit_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        
        # Clear the output text for new response
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
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
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        
        if is_error:
            self.output_text.insert(tk.END, text, "normal")
        else:
            # Process the text for formatting
            self._format_output(text)
        
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(1.0)  # Scroll to top
    
    def _format_output(self, text):
        """
        Format the output text with syntax highlighting.
        
        Args:
            text: The text to format.
        """
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
                
                # Insert the code block with tag
                self.output_text.insert(tk.END, code_text, "code_block")
                
                # Simple syntax highlighting for Python code
                self._highlight_python_syntax(
                    self.output_text.index("end-1c linestart"), 
                    self.output_text.index("end-1c")
                )
                
                self.output_text.insert(tk.END, "\n\n")
            else:
                # Regular text
                lines = part.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('# '):
                        # Heading
                        self.output_text.insert(tk.END, line + '\n', "heading")
                    elif line.strip():
                        # Normal text
                        self.output_text.insert(tk.END, line + '\n', "normal")
                    elif i < len(lines) - 1:  # Avoid extra newline at the end
                        self.output_text.insert(tk.END, '\n')
    
    def _highlight_python_syntax(self, start, end):
        """
        Apply syntax highlighting to Python code.
        
        Args:
            start: Start index of the code block.
            end: End index of the code block.
        """
        # Define patterns for syntax highlighting
        patterns = [
            (r'\b(def|class|import|from|if|else|elif|for|while|try|except|finally|with|as|return|pass|break|continue|in|is|and|or|not|True|False|None)\b', "keyword"),
            (r'(#.*)$', "comment"),
            (r'(".*?"|\'.*?\')', "string"),
        ]
        
        # Get the text content
        content = self.output_text.get(start, end)
        
        # Apply patterns
        for pattern, tag in patterns:
            pos = 0
            while True:
                match = re.search(pattern, content[pos:], re.MULTILINE)
                if not match:
                    break
                    
                start_idx = pos + match.start()
                end_idx = pos + match.end()
                
                # Convert character indices to tkinter indices
                line_start = content[:start_idx].count('\n')
                char_start = start_idx - content[:start_idx].rfind('\n') - 1
                if char_start < 0:  # If it's the first line
                    char_start = start_idx
                
                line_end = content[:end_idx].count('\n')
                char_end = end_idx - content[:end_idx].rfind('\n') - 1
                if char_end < 0:  # If it's the first line
                    char_end = end_idx
                
                start_tk = f"{start} + {line_start} lines + {char_start} chars"
                end_tk = f"{start} + {line_end} lines + {char_end} chars"
                
                # Apply the tag
                self.output_text.tag_add(tag, start_tk, end_tk)
                
                pos = end_idx
    
    def _reset_ui(self):
        """Reset the UI after processing."""
        self.submit_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.status_var.set("Ready")
    
    def _save_code_dialog(self):
        """Open a dialog to save the extracted code to a file."""
        if not self.last_code:
            messagebox.showinfo("No Code", "No code found in the current response.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Save Code"
        )
        
        if file_path:
            result = save_code_to_file(self.last_code, file_path)
            messagebox.showinfo("Save Result", result)
    
    def _copy_code(self):
        """Copy the last generated code to clipboard."""
        if not self.last_code:
            messagebox.showinfo("No Code", "No code found in the current response.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_code)
        messagebox.showinfo("Code Copied", "Code has been copied to clipboard.")
    
    def _clear_history(self):
        """Clear the assistant's conversation history."""
        self.assistant.clear_conversation_history()
        messagebox.showinfo("History Cleared", "Conversation history has been cleared.")
    
    def _open_file_dialog(self):
        """Open a file dialog to select a file for analysis."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Open File for Analysis"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
                
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, code)
                
                # Set mode to analyze
                self.mode_var.set("analyze")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def _analyze_current_code(self):
        """Analyze the code in the input text area."""
        code = self.input_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showinfo("Empty Input", "Please enter code to analyze.")
            return
        
        self.mode_var.set("analyze")
        self._process_input()
    
    def _explain_current_code(self):
        """Explain the code in the input text area."""
        code = self.input_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showinfo("Empty Input", "Please enter code to explain.")
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
        
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, prompt)
        
        self.mode_var.set("general")
        self._process_input()
    
    def _simplify_current_code(self):
        """Simplify the code in the input text area."""
        code = self.input_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showinfo("Empty Input", "Please enter code to simplify.")
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
        
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, prompt)
        
        self.mode_var.set("general")
        self._process_input()
    
    def _show_about(self):
        """Show the about dialog."""
        about_text = """
AI Programming Assistant v1.0

An AI-powered assistant that helps automate programming tasks by converting 
natural language task descriptions into executable Python code.

Powered by Claude API from Anthropic.
        """
        messagebox.showinfo("About", about_text)
    
    def _show_usage_guide(self):
        """Show the usage guide dialog."""
        guide_text = """
Usage Guide:

1. Choose a mode:
   - General Query: Ask programming questions or get advice
   - Task to Code: Convert a task description into Python code
   - Code Analysis: Analyze existing code for improvements

2. Enter your query or code in the input area

3. Click Submit or press Ctrl+Enter to send your request

4. View the response in the output area

5. Use the tools menu for additional features:
   - Analyze Code: Get feedback on code quality and suggestions
   - Explain Code: Get a simple explanation of how code works
   - Simplify Code: Get a beginner-friendly version of complex code

6. Save or copy generated code using the quick action buttons

Tips:
- Be specific in your task descriptions
- Include relevant details like file formats or data structures
- Use Clear History when starting a new topic
        """
        messagebox.showinfo("Usage Guide", guide_text)


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = ProgrammingAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()