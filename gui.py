import json

import customtkinter as ctk  # type: ignore


class KeyPressGUI:
    def __init__(self, player):
        ctk.set_appearance_mode('system')  # Automatically match the OS theme
        ctk.set_default_color_theme('dark-blue')  # Set the color theme

        self.player = player
        self.key_function_map = {}
        self.root = ctk.CTk()
        self.root.title("SAFAR!")

        # Instructions label
        instruction_text = "Press a key to execute its corresponding function."
        self.instructions_label = ctk.CTkLabel(self.root, text=instruction_text, font=("Helvetica", 12))
        self.instructions_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Key-Function Mapping Display (Custom Table)
        self.mapping_frame = ctk.CTkFrame(self.root)
        self.mapping_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.create_mapping_table()

        # Load Config Button
        self.load_config_button = ctk.CTkButton(self.root, text="Load Config", command=self.load_config)
        self.load_config_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Last key pressed display
        self.last_key_label = ctk.CTkLabel(self.root, text="Last Key Pressed: None", font=("Helvetica", 12))
        self.last_key_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Status Bar for messages
        self.status_bar = ctk.CTkLabel(self.root, text="", font=("Helvetica", 10))
        self.status_bar.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # General key binding
        self.root.bind('<Key>', self.key_pressed)

        # Window size and layout management
        self.root.geometry('400x400')
        self.root.minsize(400, 400)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)  # Make the Treeview expandable

        # Load initial config
        self.load_config()

        # Start the GUI
        self.root.mainloop()

    def key_pressed(self, event):
        key = event.keysym
        self.last_key_label.configure(text=f"Last Key Pressed: {key}")
        if key in self.key_function_map:
            try:
                self.key_function_map[key]()
            except Exception as e:
                self.status_bar.configure(text=f"Error: {e}")

    def load_config(self):
        config_path = "config.json"
        try:
            self.player.load_config(config_path)
            self.update_key_function_map()
            self.status_bar.configure(text="Config loaded successfully.")
        except FileNotFoundError:
            self.status_bar.configure(text="Config file not found.")
        except json.JSONDecodeError:
            self.status_bar.configure(text="Error parsing config file.")

    def update_key_function_map(self):
        self.key_function_map = self.player.create_key_function_map()

        # Clear existing rows
        for widget in self.mapping_frame.winfo_children():
            if not isinstance(widget, ctk.CTkLabel):  # Skip header labels
                widget.destroy()

        # Populate the table
        for row, (key, func) in enumerate(self.key_function_map.items(), start=1):
            ctk.CTkLabel(self.mapping_frame, text=key).grid(row=row, column=0, sticky='nsew')
            ctk.CTkLabel(self.mapping_frame, text=func.__name__).grid(row=row, column=1, sticky='nsew')
            ctk.CTkLabel(self.mapping_frame, text='Description here').grid(row=row, column=2,
                                                                           sticky='nsew')  # Add descriptions

    def create_mapping_table(self):
        # Header
        ctk.CTkLabel(self.mapping_frame, text='Key', font=('Helvetica', 10, 'bold')).grid(row=0, column=0,
                                                                                          sticky='nsew')
        ctk.CTkLabel(self.mapping_frame, text='Function Name', font=('Helvetica', 10, 'bold')).grid(row=0, column=1,
                                                                                                    sticky='nsew')
        ctk.CTkLabel(self.mapping_frame, text='Description', font=('Helvetica', 10, 'bold')).grid(row=0, column=2,
                                                                                                  sticky='nsew')

        # Set column weights for resizing
        self.mapping_frame.grid_columnconfigure(0, weight=1)
        self.mapping_frame.grid_columnconfigure(1, weight=2)
        self.mapping_frame.grid_columnconfigure(2, weight=3)
