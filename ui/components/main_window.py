"""
Main window setup functions for the AI Programming Assistant GUI.
"""
import customtkinter as ctk


def create_main_window(root, title, geometry, min_size=None):
    """
    Configure the main application window.
    
    Args:
        root: The root Tk window instance
        title: Window title
        geometry: Window geometry string (e.g., "900x700")
        min_size: Tuple with minimum window size (width, height)
    """
    root.title(title)
    root.geometry(geometry)
    
    if min_size:
        root.minsize(min_size[0], min_size[1])


def create_dialog(parent, title, size, resizable=False, topmost=True, center=True):
    """
    Create a modal dialog window.
    
    Args:
        parent: Parent window
        title: Dialog title
        size: Size string (e.g., "300x200")
        resizable: Whether the dialog can be resized
        topmost: Whether the dialog should be topmost
        center: Whether to center the dialog on the parent window
        
    Returns:
        The created dialog window
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry(size)
    dialog.resizable(resizable, resizable)
    
    if topmost:
        dialog.attributes("-topmost", True)
    
    if center:
        # Center the dialog on the parent window
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (int(size.split("x")[0]) // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (int(size.split("x")[1]) // 2)
        dialog.geometry(f"+{x}+{y}")
    
    return dialog


def show_message_dialog(parent, title, message, width=300, height=150):
    """
    Show a simple message dialog with an OK button.
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Message to display
        width: Dialog width
        height: Dialog height
    """
    dialog = create_dialog(parent, title, f"{width}x{height}")
    
    # Message label
    message_label = ctk.CTkLabel(
        dialog, 
        text=message,
        wraplength=width - 20
    )
    message_label.pack(pady=(20, 0))
    
    # OK button
    ok_button = ctk.CTkButton(
        dialog, 
        text="OK", 
        command=dialog.destroy
    )
    ok_button.pack(pady=20)