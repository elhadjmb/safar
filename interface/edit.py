import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk  # Make sure customtkinter is installed

from logic import Config


class ConfigBackend:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = Config()
        self.detected_screens = []
        self.load_config()

    def load_config(self):
        """Load configuration from the JSON file."""
        self.config.load("config.json")

    def save_config(self):
        """Save the current configuration to the JSON file."""
        self.config.save("config.json")

    def detect_screens(self):
        """Detect and store available screens."""
        self.detected_screens = self.config.screens  # Replace with your actual screen detection logic

    def remap_screen(self, config_screen_id, detected_screen_id):
        """
        Remap a screen in the configuration.

        Args:
            config_screen_id (int): The ID of the screen in the configuration.
            detected_screen_id (int): The ID of the detected screen to map to.
        """
        if config_screen_id < len(self.config.screens) and detected_screen_id < len(self.detected_screens):
            config_screen = self.config.screens[config_screen_id]
            detected_screen = self.detected_screens[detected_screen_id]

            # Assuming each screen has 'select_index', 'name', 'width', 'height', 'x', 'y'
            config_screen.select_index = detected_screen_id
            config_screen.name = detected_screen.name
            config_screen.width = detected_screen.width
            config_screen.height = detected_screen.height
            config_screen.x = detected_screen.x
            config_screen.y = detected_screen.y
        else:
            raise IndexError("Screen ID out of range.")


class ConfigGUI(ConfigBackend):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Screen Configuration")
        self.setup_widgets()

    def setup_widgets(self):
        # Main frame with improved layout
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Label
        self.header_label = ctk.CTkLabel(self.main_frame, text="Screen Configuration Tool", font=("Arial", 14, "bold"))
        self.header_label.pack(pady=(0, 10))

        # Screen detection section with clear labeling
        self.detect_button = ctk.CTkButton(self.main_frame, text="Detect Screens", command=self.on_detect_screens)
        self.detect_button.pack(pady=(0, 10))

        # Detected screens frame with label
        self.detected_screens_label = ctk.CTkLabel(self.main_frame, text="Detected Screens:", font=("Arial", 12))
        self.detected_screens_label.pack(pady=(5, 0))

        self.detected_screens_frame = ctk.CTkFrame(self.main_frame)
        self.detected_screens_frame.pack(pady=(0, 10), fill="both", expand=True)

        # Configuration screens frame with label
        self.config_screens_label = ctk.CTkLabel(self.main_frame, text="Configuration Screens:", font=("Arial", 12))
        self.config_screens_label.pack(pady=(5, 0))

        self.config_screens_frame = ctk.CTkFrame(self.main_frame)
        self.config_screens_frame.pack(pady=(0, 10), fill="both", expand=True)

        # Save button with improved positioning
        self.save_button = ctk.CTkButton(self.main_frame, text="Save Configuration", command=self.on_save_config)
        self.save_button.pack(pady=(10, 0))

    def on_detect_screens(self):
        self.detect_screens()
        self.display_detected_screens()
        self.display_config_screens()

    def display_detected_screens(self):
        for widget in self.detected_screens_frame.winfo_children():
            widget.destroy()

        for i, screen in enumerate(self.detected_screens):
            screen_frame = ctk.CTkFrame(self.detected_screens_frame)
            screen_frame.pack(pady=2, fill="x", expand=True)
            screen_frame.grid_columnconfigure(1, weight=1)  # Ensure label expands

            label = ctk.CTkLabel(screen_frame, text=f"Detected Screen {i}: {screen.name}")
            label.grid(row=0, column=0, sticky="w", padx=5)

            blink_button = ctk.CTkButton(screen_frame, text="Blink", command=lambda s=screen: s.blink())
            blink_button.grid(row=0, column=1, sticky="e", padx=5)

    def display_config_screens(self):
        for widget in self.config_screens_frame.winfo_children():
            widget.destroy()

        for i, screen in enumerate(self.config.screens):
            config_frame = ctk.CTkFrame(self.config_screens_frame)
            config_frame.pack(pady=2, fill="x", expand=True)
            config_frame.grid_columnconfigure(1, weight=1)  # Ensure label expands

            label = ctk.CTkLabel(config_frame, text=f"Config Screen {i}: {screen.name}")
            label.grid(row=0, column=0, sticky="w", padx=5)

            screen_var = tk.StringVar(value=[f"Screen {j}" for j in range(len(self.detected_screens))][0])
            dropdown = ctk.CTkOptionMenu(config_frame, variable=screen_var, values=screen_var.get())
            dropdown.grid(row=0, column=1, padx=5)

            remap_button = ctk.CTkButton(config_frame, text="Remap",
                                         command=lambda i=i, var=screen_var: self.remap_and_update(i, var))
            remap_button.grid(row=0, column=2, padx=5)
    def remap_and_update(self, config_screen_id, screen_var):
        detected_screen_id = int(screen_var.get().split(" ")[1])
        self.remap_screen(config_screen_id, detected_screen_id)
        messagebox.showinfo("Success", f"Screen {config_screen_id} remapped to Detected Screen {detected_screen_id}")

    def on_save_config(self):
        self.save_config()
        messagebox.showinfo("Success", "Configuration Saved Successfully")


# Create and run the GUI
root = ctk.CTk()
app = ConfigGUI(root)
root.mainloop()
