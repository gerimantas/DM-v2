"""
Input processing handlers for the AI Programming Assistant GUI.
"""
import os
import re
from threading import Thread
from src.utils import extract_code


class InputHandler:
    """
    Handler for processing user input and interacting with the assistant.
    """
    
    def __init__(self, app):
        """
        Initialize with reference to the main application.
        
        Args:
            app: Main application instance
        """
        self.app = app
    
    def process_input(self):
        """Process the user input and display the response."""
        if self.app.processing:
            return
        
        user_input = self.app.input_text.get("1.0", "end").strip()
        if not user_input:
            from ui.components.main_window import show_message_dialog
            show_message_dialog(self.app.root, "Empty Input", "Please enter a task or question.")
            return
        
        # Start processing
        self.app.processing = True
        self.app.status_label.configure(text="Processing...")
        self.app.submit_button.configure(state="disabled")
        self.app.progress_bar.start()
        
        # Clear the output text for new response
        self.app.output_text.delete("1.0", "end")
        
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
            mode = self.app.mode_var.get()
            
            # Check for image references
            image_path = None
            match = re.search(r'\[Screenshot attached: (.*?)\]', user_input)
            if match:
                image_path = match.group(1)
                # Remove the reference from the query
                user_input = re.sub(r'\[Screenshot attached: .*?\]', '', user_input).strip()
            
            if mode == "task":
                response = self.app.assistant.convert_task_to_code(user_input)
            elif mode == "analyze":
                # Check if the input is a file path or code snippet
                if os.path.exists(user_input):
                    with open(user_input, 'r') as f:
                        code = f.read()
                else:
                    code = user_input
                response = self.app.assistant.analyze_code(code)
            else:  # general
                if image_path and os.path.exists(image_path):
                    # Process with image if available
                    response = self._process_query_with_image(user_input, image_path)
                else:
                    response = self.app.assistant.process_query(user_input)
            
            # Extract code from response if present
            self.app.last_code = extract_code(response) or ""
            
            # Update UI in the main thread
            self.app.root.after(0, lambda: self._update_output(response))
        except Exception as e:
            error_message = f"Error processing your request: {str(e)}"
            self.app.root.after(0, lambda: self._update_output(error_message, is_error=True))
        finally:
            # Reset processing state
            self.app.processing = False
            self.app.root.after(0, self._reset_ui)
    
    def _process_query_with_image(self, query, image_path):
        """
        Process a query that includes an image using OCR when enabled.
        
        Args:
            query: The user's text query
            image_path: Path to the screenshot image
            
        Returns:
            Response from the assistant
        """
        from PIL import Image
        
        try:
            # Try to open the image to verify it exists and is valid
            img = Image.open(image_path)
            
            # Check if OCR is enabled
            if self.app.use_ocr and self.app.ocr_helper.tesseract_available:
                # Extract text from the image using OCR
                extracted_code, detected_language = self.app.ocr_helper.extract_code_with_language_detection(image_path)
                
                if extracted_code and not "Error extracting" in extracted_code:
                    # Create an enhanced query with the extracted code
                    lang_info = f" (detected language: {detected_language})" if detected_language != "unknown" else ""
                    
                    enhanced_query = f"{query}\n\nHere's the code extracted from the screenshot{lang_info}:\n\n```{detected_language}\n{extracted_code}\n```\n\nPlease analyze this code based on my request above."
                else:
                    # If OCR failed, fall back to the original approach
                    enhanced_query = f"{query}\n\nI'm looking at a screenshot that contains code or programming-related content. Please help me understand or improve it based on my description above."
            else:
                # If OCR is disabled, use the original approach
                enhanced_query = f"{query}\n\nI'm looking at a screenshot that contains code or programming-related content. Please help me understand or improve it based on my description above."
            
            # Process with the enhanced query
            return self.app.assistant.process_query(enhanced_query)
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def _update_output(self, text, is_error=False):
        """
        Update the output text.
        
        Args:
            text: The text to display.
            is_error: Whether the text is an error message.
        """
        self.app.output_text.delete("1.0", "end")
        
        if is_error:
            self.app.output_text.insert("end", text)
        else:
            # Process the text for formatting
            self.app.text_handler.format_output(text)
    
    def _reset_ui(self):
        """Reset the UI after processing."""
        self.app.submit_button.configure(state="normal")
        self.app.progress_bar.stop()
        self.app.status_label.configure(text="Ready")