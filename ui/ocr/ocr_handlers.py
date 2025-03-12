"""
OCR handling functionality for the AI Programming Assistant GUI.
"""
import os
import time
from threading import Thread
from pathlib import Path
from PIL import ImageGrab, Image
import customtkinter as ctk
from ui.components.main_window import create_dialog, show_message_dialog


class OCRHandler:
    """
    Handler for OCR-related functionality.
    """
    
    def __init__(self, app):
        """
        Initialize with reference to the main application.
        
        Args:
            app: Main application instance
        """
        self.app = app
    
    def handle_paste(self, event):
        """
        Handle Ctrl+V paste event to check for images.
        
        Args:
            event: The paste event
            
        Returns:
            "break" if image handled, None otherwise
        """
        try:
            # Check if there's an image in clipboard
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):
                # If image found, use the screenshot function
                self.paste_screenshot()
                return "break"  # Prevent default paste behavior
            # Otherwise let the default paste action occur
            return None
        except Exception:
            # If there's an error, allow regular paste
            return None
    
    def paste_screenshot(self):
        """Paste screenshot from clipboard and add to the query."""
        try:
            # Get image from clipboard
            img = ImageGrab.grabclipboard()
            
            if img is None or not isinstance(img, Image.Image):
                show_message_dialog(
                    self.app.root, 
                    "Clipboard Empty", 
                    "No image found in clipboard. Copy an image first."
                )
                return
            
            # Create a temporary file to save the image
            temp_dir = self.app.temp_dir
            temp_dir.mkdir(exist_ok=True)
            
            # Generate a unique filename
            timestamp = int(time.time())
            img_path = temp_dir / f"screenshot_{timestamp}.png"
            
            # Save the image
            img.save(img_path)
            
            # Add reference to the image in the input
            current_text = self.app.input_text.get("1.0", "end").strip()
            
            if current_text:
                # Add the image reference to existing text
                new_text = f"{current_text}\n\n[Screenshot attached: {img_path}]"
            else:
                # Create new text with the image reference
                new_text = f"Analyze this screenshot: {img_path}"
            
            # Update the input text
            self.app.input_text.delete("1.0", "end")
            self.app.input_text.insert("1.0", new_text)
            
            show_message_dialog(
                self.app.root, 
                "Screenshot Added", 
                "Screenshot has been added to your query."
            )
            
        except Exception as e:
            show_message_dialog(
                self.app.root, 
                "Error", 
                f"Failed to paste screenshot: {str(e)}"
            )
    
    def toggle_ocr(self):
        """Toggle the OCR feature on/off."""
        self.app.use_ocr = not self.app.use_ocr
    
    def setup_ocr_settings(self):
        """Open a dialog to configure OCR settings."""
        settings_dialog = create_dialog(
            self.app.root,
            "OCR Settings",
            "500x300"
        )
        
        # Tesseract path setting
        path_frame = ctk.CTkFrame(settings_dialog)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        path_label = ctk.CTkLabel(
            path_frame, 
            text="Tesseract OCR Path:",
            font=("Arial", 12)
        )
        path_label.pack(side="left", padx=(0, 5))
        
        path_entry = ctk.CTkEntry(
            path_frame,
            width=300,
            font=("Arial", 12)
        )
        path_entry.pack(side="left", padx=5)
        path_entry.insert(0, self.app.ocr_helper.tesseract_path or "")
        
        browse_button = ctk.CTkButton(
            path_frame,
            text="Browse",
            width=80,
            command=lambda: self._browse_tesseract_path(path_entry)
        )
        browse_button.pack(side="left", padx=5)
        
        # OCR Status label
        status_label = ctk.CTkLabel(
            settings_dialog,
            text=f"Tesseract OCR Status: {'Available' if self.app.ocr_helper.tesseract_available else 'Not Available'}",
            font=("Arial", 14),
            text_color="green" if self.app.ocr_helper.tesseract_available else "red"
        )
        status_label.pack(pady=10)
        
        # Preprocessing options frame
        preproc_frame = ctk.CTkFrame(settings_dialog)
        preproc_frame.pack(fill="x", padx=10, pady=10)
        
        preproc_label = ctk.CTkLabel(
            preproc_frame,
            text="Image Preprocessing:",
            font=("Arial", 12)
        )
        preproc_label.pack(anchor="w", padx=5, pady=5)
        
        # Save button
        save_button = ctk.CTkButton(
            settings_dialog,
            text="Save Settings",
            command=lambda: self._save_ocr_settings(path_entry.get(), settings_dialog)
        )
        save_button.pack(pady=10)
    
    def _browse_tesseract_path(self, entry_widget):
        """Browse for Tesseract executable path."""
        file_path = ctk.filedialog.askopenfilename(
            title="Select Tesseract Executable",
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")]
        )
        
        if file_path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, file_path)
    
    def _save_ocr_settings(self, tesseract_path, dialog):
        """Save OCR settings and reinitialize the OCR helper."""
        try:
            # Reinitialize OCR helper with new path
            self.app.ocr_helper = self.app.ocr_helper.__class__(tesseract_path)
            dialog.destroy()
            show_message_dialog(
                self.app.root, 
                "Settings Saved", 
                "OCR settings have been updated successfully."
            )
        except Exception as e:
            show_message_dialog(
                self.app.root, 
                "Error", 
                f"Failed to save settings: {str(e)}"
            )
    
    def test_ocr(self):
        """Test OCR functionality with a sample image."""
        # Open file dialog
        file_path = ctk.filedialog.askopenfilename(
            title="Select Image for OCR Test",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Extract text
            extracted_text = self.app.ocr_helper.extract_text_from_image(file_path)
            
            # Show result
            result_dialog = create_dialog(
                self.app.root,
                "OCR Test Result",
                "600x400"
            )
            
            # Display extracted text
            result_frame = ctk.CTkFrame(result_dialog)
            result_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            result_label = ctk.CTkLabel(
                result_frame,
                text="Extracted Text:",
                font=("Arial", 14, "bold")
            )
            result_label.pack(anchor="w", pady=(0, 5))
            
            text_box = ctk.CTkTextbox(
                result_frame,
                font=("Arial", 12),
                wrap="word"
            )
            text_box.pack(fill="both", expand=True)
            text_box.insert("1.0", extracted_text)
            
            # Close button
            close_button = ctk.CTkButton(
                result_dialog,
                text="Close",
                command=result_dialog.destroy
            )
            close_button.pack(pady=10)
            
        except Exception as e:
            show_message_dialog(
                self.app.root, 
                "OCR Test Failed", 
                f"Error: {str(e)}"
            )
    
    def extract_text_from_image(self):
        """Open an image file and extract text using OCR."""
        # Open file dialog
        file_path = ctk.filedialog.askopenfilename(
            title="Select Image for Text Extraction",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Show processing dialog
        processing_dialog = create_dialog(
            self.app.root,
            "Processing",
            "300x100"
        )
        
        processing_label = ctk.CTkLabel(
            processing_dialog,
            text="Extracting text from image...",
            font=("Arial", 14)
        )
        processing_label.pack(pady=20)
        
        # Process in a thread to keep UI responsive
        def extract_thread():
            try:
                # Try to detect if this is code
                extracted_code, language = self.app.ocr_helper.extract_code_with_language_detection(file_path)
                
                # Close processing dialog
                self.app.root.after(0, processing_dialog.destroy)
                
                # Update the input text
                self.app.root.after(0, lambda: self._update_with_extracted_text(extracted_code, language))
                
            except Exception as e:
                # Close processing dialog
                self.app.root.after(0, processing_dialog.destroy)
                # Show error
                self.app.root.after(0, lambda: show_message_dialog(
                    self.app.root, 
                    "Extraction Failed", 
                    f"Error: {str(e)}"
                ))
        
        # Start thread
        thread = Thread(target=extract_thread)
        thread.daemon = True
        thread.start()
    
    def _update_with_extracted_text(self, text, language="unknown"):
        """Update the input text with the extracted text."""
        # Clear current input
        self.app.input_text.delete("1.0", "end")
        
        if language != "unknown":
            # Create formatted input with language
            new_text = f"I extracted this code that appears to be {language}. Please analyze it:\n\n```{language}\n{text}\n```"
        else:
            # Create formatted input without language
            new_text = f"I extracted this text using OCR. Please analyze it:\n\n{text}"
        
        # Insert the new text
        self.app.input_text.insert("1.0", new_text)
        
        # Set mode to analyze if it's code
        if language != "unknown":
            self.app.mode_var.set("analyze")
        
        # Show confirmation
        show_message_dialog(
            self.app.root, 
            "Text Extracted", 
            "Text has been extracted and added to the input area."
        )