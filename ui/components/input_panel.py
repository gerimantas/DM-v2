"""
Input panel components for the AI Programming Assistant GUI.
"""
import customtkinter as ctk


def create_input_panel(parent, font_size, font_adjust_callback, paste_callback=None):
    """
    Create the input panel with text area, mode selection, and action buttons.
    
    Args:
        parent: Parent frame
        font_size: Initial font size for input text
        font_adjust_callback: Callback for font size adjustment
        paste_callback: Callback for paste event handling
        
    Returns:
        Dictionary containing the created components
    """
    # Input label
    input_label = ctk.CTkLabel(
        parent, 
        text="Enter your programming task or question:",
        font=("Arial", 14)
    )
    input_label.pack(anchor="w", pady=(0, 5))
    
    # Input text area
    input_text = ctk.CTkTextbox(
        parent, 
        height=150,
        font=("Arial", font_size),
        wrap="word"
    )
    input_text.pack(fill="x", pady=(0, 10))
    
    # Bind events
    input_text.bind("<Control-Return>", lambda event: submit_button.invoke())
    input_text.bind("<Control-MouseWheel>", font_adjust_callback)
    
    if paste_callback:
        input_text.bind("<Control-v>", paste_callback)
    
    # Create mode selection frame
    mode_frame = ctk.CTkFrame(parent)
    mode_frame.pack(fill="x", pady=(0, 10))
    
    mode_label = ctk.CTkLabel(mode_frame, text="Mode:", font=("Arial", 12))
    mode_label.pack(side="left", padx=(0, 5))
    
    # Radio buttons for mode selection
    mode_var = ctk.StringVar(value="general")
    
    general_radio = ctk.CTkRadioButton(
        mode_frame, 
        text="General Query", 
        variable=mode_var, 
        value="general",
        font=("Arial", 14)
    )
    general_radio.pack(side="left", padx=5)
    
    task_radio = ctk.CTkRadioButton(
        mode_frame, 
        text="Task to Code", 
        variable=mode_var, 
        value="task",
        font=("Arial", 14)
    )
    task_radio.pack(side="left", padx=5)
    
    analyze_radio = ctk.CTkRadioButton(
        mode_frame, 
        text="Code Analysis", 
        variable=mode_var, 
        value="analyze",
        font=("Arial", 14)
    )
    analyze_radio.pack(side="left", padx=5)
    
    # Create button frame
    button_frame = ctk.CTkFrame(parent)
    button_frame.pack(fill="x", pady=(0, 10))
    
    # Submit button
    submit_button = ctk.CTkButton(
        button_frame, 
        text="Submit", 
        font=("Arial", 14)
    )
    submit_button.pack(side="left", padx=(0, 10))
    
    # Status label
    status_label = ctk.CTkLabel(
        button_frame, 
        text="Ready",
        font=("Arial", 14)
    )
    status_label.pack(side="left", padx=5)
    
    # Progress bar
    progress_bar = ctk.CTkProgressBar(button_frame, width=200)
    progress_bar.pack(side="left", padx=10)
    progress_bar.set(0)  # Set initial value to 0
    
    # Create action buttons
    actions_frame = ctk.CTkFrame(parent)
    actions_frame.pack(fill="x", pady=(0, 10))
    
    # Dictionary to hold button references (to be configured in main class)
    action_buttons = {}
    
    # Save code button
    save_button = ctk.CTkButton(
        actions_frame, 
        text="Save Code", 
        font=("Arial", 14)
    )
    save_button.pack(side="left", padx=(0, 5))
    action_buttons["save"] = save_button
    
    # Copy code button
    copy_button = ctk.CTkButton(
        actions_frame, 
        text="Copy Code", 
        font=("Arial", 14)
    )
    copy_button.pack(side="left", padx=5)
    action_buttons["copy"] = copy_button
    
    # Paste screenshot button
    paste_screenshot_button = ctk.CTkButton(
        actions_frame, 
        text="Paste Screenshot", 
        font=("Arial", 14)
    )
    paste_screenshot_button.pack(side="left", padx=5)
    action_buttons["paste_screenshot"] = paste_screenshot_button
    
    # Clear output button
    clear_button = ctk.CTkButton(
        actions_frame, 
        text="Clear Output", 
        font=("Arial", 14)
    )
    clear_button.pack(side="left", padx=5)
    action_buttons["clear"] = clear_button
    
    # Return components
    return {
        "input_text": input_text,
        "mode_var": mode_var,
        "submit_button": submit_button,
        "status_label": status_label,
        "progress_bar": progress_bar,
        "action_buttons": action_buttons
    }