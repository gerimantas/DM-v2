"""
Output panel components for the AI Programming Assistant GUI.
"""
import customtkinter as ctk


def create_output_panel(parent, font_size, font_adjust_callback):
    """
    Create the output panel with text area for displaying assistant responses.
    
    Args:
        parent: Parent frame
        font_size: Initial font size for output text
        font_adjust_callback: Callback for font size adjustment
        
    Returns:
        Dictionary containing the created components
    """
    # Output label
    output_label = ctk.CTkLabel(
        parent, 
        text="Assistant Response:",
        font=("Arial", 14)
    )
    output_label.pack(anchor="w", pady=(0, 5))
    
    # Output text area
    output_text = ctk.CTkTextbox(
        parent, 
        font=("Arial", font_size),
        wrap="word"
    )
    output_text.pack(fill="both", expand=True)
    
    # Bind font adjustment event
    output_text.bind("<Control-MouseWheel>", font_adjust_callback)
    
    # Return components
    return {
        "output_text": output_text
    }