"""
UI components for selecting AI model providers and models.
"""
import customtkinter as ctk
from typing import Callable, Dict, Any, Optional

from config.model_config import PROVIDERS, get_models_for_provider


class ModelSelector:
    """
    UI component for selecting AI model provider and model.
    """
    
    def __init__(self, parent_frame, callback: Optional[Callable] = None):
        """
        Initialize the model selector component.
        
        Args:
            parent_frame: Parent frame to place the component
            callback: Optional callback function to call when selection changes
        """
        self.parent = parent_frame
        self.callback = callback
        self.current_provider = "claude"  # Default provider
        
        # Create the selector UI components
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI components for model selection."""
        # Create main frame
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="x", padx=10, pady=5)
        
        # Create provider selection label
        provider_label = ctk.CTkLabel(
            self.frame,
            text="AI Provider:",
            font=("Arial", 14)
        )
        provider_label.pack(side="left", padx=(0, 5))
        
        # Create provider dropdown
        self.provider_var = ctk.StringVar(value="claude")
        self.provider_menu = ctk.CTkOptionMenu(
            self.frame,
            values=list(PROVIDERS.keys()),
            command=self._on_provider_changed,
            variable=self.provider_var,
            width=150,
            dynamic_resizing=False
        )
        self.provider_menu.pack(side="left", padx=5)
        
        # Create model selection label
        model_label = ctk.CTkLabel(
            self.frame,
            text="Model:",
            font=("Arial", 14)
        )
        model_label.pack(side="left", padx=(20, 5))
        
        # Create model dropdown
        models = get_models_for_provider(self.current_provider)
        model_options = [model["id"] for model in models]
        
        self.model_var = ctk.StringVar(value=model_options[0] if model_options else "")
        self.model_menu = ctk.CTkOptionMenu(
            self.frame,
            values=model_options,
            command=self._on_model_changed,
            variable=self.model_var,
            width=220,
            dynamic_resizing=False
        )
        self.model_menu.pack(side="left", padx=5)
        
        # API key button
        self.api_key_button = ctk.CTkButton(
            self.frame,
            text="Set API Key",
            command=self._show_api_key_dialog,
            width=100
        )
        self.api_key_button.pack(side="right", padx=5)
        
        # Model info button
        self.info_button = ctk.CTkButton(
            self.frame,
            text="?",
            command=self._show_model_info,
            width=30
        )
        self.info_button.pack(side="right", padx=5)
    
    def _on_provider_changed(self, provider: str):
        """
        Handle provider selection change.
        
        Args:
            provider: The selected provider
        """
        self.current_provider = provider
        
        # Update model options
        models = get_models_for_provider(provider)
        model_options = [model["id"] for model in models]
        
        # Update model dropdown
        self.model_menu.configure(values=model_options)
        if model_options:
            self.model_var.set(model_options[0])
        
        # Call callback if provided
        if self.callback:
            self.callback(provider=provider, model=self.model_var.get())
    
    def _on_model_changed(self, model: str):
        """
        Handle model selection change.
        
        Args:
            model: The selected model
        """
        # Call callback if provided
        if self.callback:
            self.callback(provider=self.current_provider, model=model)
    
    def _show_api_key_dialog(self):
        """Show dialog for setting API key."""
        # Create the dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Set {PROVIDERS.get(self.current_provider, self.current_provider)} API Key")
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        
        # Center dialog on parent window
        if hasattr(self.parent, 'winfo_rootx') and hasattr(self.parent, 'winfo_rooty'):
            x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 250
            y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 100
            dialog.geometry(f"+{x}+{y}")
        
        # Instructions
        provider_name = PROVIDERS.get(self.current_provider, self.current_provider)
        instructions = ctk.CTkLabel(
            dialog,
            text=f"Enter your {provider_name} API key.\nThis will be stored in the .env file.",
            font=("Arial", 14),
            justify="left"
        )
        instructions.pack(pady=(20, 10), padx=20, anchor="w")
        
        # API key entry
        api_key_frame = ctk.CTkFrame(dialog)
        api_key_frame.pack(fill="x", padx=20, pady=10)
        
        api_key_label = ctk.CTkLabel(
            api_key_frame,
            text="API Key:",
            font=("Arial", 14)
        )
        api_key_label.pack(side="left", padx=(0, 10))
        
        api_key_entry = ctk.CTkEntry(
            api_key_frame,
            width=350,
            font=("Arial", 14),
            show="•"
        )
        api_key_entry.pack(side="left")
        
        # Try to load existing API key from environment
        import os
        from dotenv import load_dotenv
        from pathlib import Path
        
        # Get the project root directory
        project_root = Path(__file__).resolve().parent.parent.parent
        env_path = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_path)
        
        # Get API key based on provider
        key_var_name = f"{self.current_provider.upper()}_API_KEY"
        existing_key = os.getenv(key_var_name)
        
        if existing_key:
            api_key_entry.insert(0, existing_key)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=lambda: self._save_api_key(api_key_entry.get(), dialog, key_var_name),
            width=100
        )
        save_button.pack(side="left")
    
    def _save_api_key(self, api_key: str, dialog, key_var_name: str):
        """
        Save API key to .env file.
        
        Args:
            api_key: The API key to save
            dialog: The dialog to close
            key_var_name: The environment variable name for the API key
        """
        if not api_key:
            return
        
        try:
            from pathlib import Path
            
            # Get the project root directory
            project_root = Path(__file__).resolve().parent.parent.parent
            env_path = project_root / '.env'
            
            # Load existing .env file or create new one
            env_vars = {}
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key] = value
            
            # Update or add the API key
            env_vars[key_var_name] = api_key
            
            # Write updated .env file
            with open(env_path, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            
            # Close dialog
            dialog.destroy()
            
            # Show success message
            self._show_message("API Key Saved", f"The API key for {PROVIDERS.get(self.current_provider, self.current_provider)} has been saved.")
            
            # Update environment variable in current session
            import os
            os.environ[key_var_name] = api_key
            
        except Exception as e:
            # Show error message
            self._show_message("Error", f"Failed to save API key: {str(e)}")
    
    def _show_model_info(self):
        """Show information about the selected model."""
        # Get the selected model details
        models = get_models_for_provider(self.current_provider)
        selected_model_id = self.model_var.get()
        
        selected_model = None
        for model in models:
            if model["id"] == selected_model_id:
                selected_model = model
                break
        
        if not selected_model:
            return
        
        # Create the dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Model Information")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        
        # Center dialog on parent window
        if hasattr(self.parent, 'winfo_rootx') and hasattr(self.parent, 'winfo_rooty'):
            x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 200
            y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 125
            dialog.geometry(f"+{x}+{y}")
        
        # Model provider
        provider_name = PROVIDERS.get(self.current_provider, self.current_provider)
        provider_label = ctk.CTkLabel(
            dialog,
            text=f"Provider: {provider_name}",
            font=("Arial", 16, "bold")
        )
        provider_label.pack(pady=(20, 5), anchor="w", padx=20)
        
        # Model name
        model_name_label = ctk.CTkLabel(
            dialog,
            text=f"Model: {selected_model['name']}",
            font=("Arial", 14)
        )
        model_name_label.pack(pady=5, anchor="w", padx=20)
        
        # Model ID
        model_id_label = ctk.CTkLabel(
            dialog,
            text=f"ID: {selected_model['id']}",
            font=("Arial", 12)
        )
        model_id_label.pack(pady=5, anchor="w", padx=20)
        
        # Context window
        context_label = ctk.CTkLabel(
            dialog,
            text=f"Max Tokens: {selected_model['tokens']}",
            font=("Arial", 12)
        )
        context_label.pack(pady=5, anchor="w", padx=20)
        
        # Description
        description_label = ctk.CTkLabel(
            dialog,
            text=f"Description: {selected_model['description']}",
            font=("Arial", 12),
            wraplength=360,
            justify="left"
        )
        description_label.pack(pady=5, anchor="w", padx=20)
        
        # Close button
        close_button = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=80
        )
        close_button.pack(pady=20)
    
    def _show_message(self, title: str, message: str):
        """
        Show a message dialog.
        
        Args:
            title: Dialog title
            message: Message to display
        """
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        
        # Center dialog on parent window
        if hasattr(self.parent, 'winfo_rootx') and hasattr(self.parent, 'winfo_rooty'):
            x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 150
            y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 75
            dialog.geometry(f"+{x}+{y}")
        
        # Message label
        message_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 14),
            wraplength=280
        )
        message_label.pack(pady=(20, 0))
        
        # OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=80
        )
        ok_button.pack(pady=20)
    
    def get_selection(self) -> Dict[str, str]:
        """
        Get the current provider and model selection.
        
        Returns:
            Dictionary with 'provider' and 'model' keys
        """
        return {
            "provider": self.current_provider,
            "model": self.model_var.get()
        }
    
    def set_selection(self, provider: str, model: Optional[str] = None):
        """
        Set the provider and model selection.
        
        Args:
            provider: Provider to select
            model: Model to select (optional, will use default if not provided)
        """
        if provider in PROVIDERS:
            # Set provider
            self.provider_var.set(provider)
            self.current_provider = provider
            
            # Update model options
            models = get_models_for_provider(provider)
            model_options = [model["id"] for model in models]
            
            # Update model dropdown
            self.model_menu.configure(values=model_options)
            
            # Set model if provided, otherwise use first model
            if model and model in model_options:
                self.model_var.set(model)
            elif model_options:
                self.model_var.set(model_options[0])
            
            # Call callback if provided
            if self.callback:
                self.callback(provider=provider, model=self.model_var.get())