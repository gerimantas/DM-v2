"""
Menu bar components for the AI Programming Assistant GUI.
"""
import customtkinter as ctk


def create_menu_bar(parent, handler):
    """
    Create the top menu bar with buttons for file, tools, OCR, and help.
    
    Args:
        parent: Parent window
        handler: Handler object that contains menu callback methods
        
    Returns:
        Menu frame and button references
    """
    menu_frame = ctk.CTkFrame(parent)
    menu_frame.pack(fill="x", padx=10, pady=5)
    
    # File operations menu button
    file_button = ctk.CTkButton(
        menu_frame, 
        text="File", 
        command=handler.show_file_menu,
        font=("Arial", 14),
        width=80
    )
    file_button.pack(side="left", padx=(0, 5))
    
    # Tools menu button
    tools_button = ctk.CTkButton(
        menu_frame, 
        text="Tools", 
        command=handler.show_tools_menu,
        font=("Arial", 14),
        width=80
    )
    tools_button.pack(side="left", padx=5)
    
    # OCR menu button
    ocr_button = ctk.CTkButton(
        menu_frame, 
        text="OCR", 
        command=handler.show_ocr_menu,
        font=("Arial", 14),
        width=80
    )
    ocr_button.pack(side="left", padx=5)
    
    # Help menu button
    help_button = ctk.CTkButton(
        menu_frame, 
        text="Help", 
        command=handler.show_help_menu,
        font=("Arial", 14),
        width=80
    )
    help_button.pack(side="left", padx=5)
    
    return {
        "menu_frame": menu_frame,
        "file_button": file_button,
        "tools_button": tools_button,
        "ocr_button": ocr_button,
        "help_button": help_button
    }