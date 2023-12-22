import json

import customtkinter as ctk  # type: ignore


class KeyPressGUI:
    def __init__(self, player):
        self.player = player
        self.key_function_map = {}
        self.root = ctk.CTk()

        self.setup_root_window()
        self.create_instructions_label()
        self.create_mapping_frame()
        self.create_load_config_button()
        self.create_last_key_label()
        self.create_setup_button()  # Add this line to create the Setup button
        self.create_status_bar()
        self.root.mainloop()

    def setup_root_window(self):
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')
        self.root.title("SAFAR!")
        self.root.geometry('400x400')
        self.root.minsize(400, 400)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.bind('<Key>', self.key_pressed)

    def create_instructions_label(self):
        instruction_text = "Press a key to execute its corresponding function."
        self.instructions_label = ctk.CTkLabel(self.root, text=instruction_text, font=("Helvetica", 12))
        self.instructions_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def create_mapping_frame(self):
        self.mapping_frame = ctk.CTkFrame(self.root)
        self.mapping_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.create_mapping_table()

    def create_load_config_button(self):
        self.load_config_button = ctk.CTkButton(self.root, text="Load Config", command=self.load_config)
        self.load_config_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def create_last_key_label(self):
        self.last_key_label = ctk.CTkLabel(self.root, text="Last Key Pressed: None", font=("Helvetica", 12))
        self.last_key_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def create_status_bar(self):
        self.status_bar = ctk.CTkLabel(self.root, text="", font=("Helvetica", 10))
        self.status_bar.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def key_pressed(self, event):
        key = event.keysym
        self.last_key_label.configure(text=f"Last Key Pressed: {key}")
        self.execute_key_function(key)

    def execute_key_function(self, key):
        if key in self.key_function_map:
            try:
                self.key_function_map[key]()
            except Exception as e:
                self.status_bar.configure(text=f"Error: {e}")

    def create_setup_button(self):
        self.setup_button = ctk.CTkButton(self.root, text="Setup", state='disabled', command=self.open_setup_window)
        self.setup_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    def load_config(self):
        try:
            self.player.load_config()
            self.update_key_function_map()
            self.setup_button.configure(state='normal')  # Enable the button after successful load
            self.status_bar.configure(text="Config loaded successfully.")
        except FileNotFoundError:
            self.status_bar.configure(text="Config file not found.")
            self.setup_button.configure(state='disabled')
        except json.JSONDecodeError:
            self.status_bar.configure(text="Error parsing config file.")
            self.setup_button.configure(state='disabled')

    def open_setup_window(self):
        # Code to create and show a new setup window
        self.setup_window = ctk.CTkToplevel(self.root)
        self.setup_window.title("Setup Configuration")
        self.setup_window.geometry("300x300")
        # Add more setup components here as needed

    def update_key_function_map(self):
        self.key_function_map = self.player.create_key_function_map()
        self.populate_mapping_table()

    def populate_mapping_table(self):
        self.clear_existing_mapping_rows()
        for row, (key, func) in enumerate(self.key_function_map.items(), start=1):
            self.add_mapping_row(row, key, func)

    def clear_existing_mapping_rows(self):
        for widget in self.mapping_frame.winfo_children():
            if not isinstance(widget, ctk.CTkLabel):  # Skip header labels
                widget.destroy()

    def add_mapping_row(self, row, key, func):
        ctk.CTkLabel(self.mapping_frame, text=key).grid(row=row, column=0, sticky='nsew')
        ctk.CTkLabel(self.mapping_frame, text=func.__name__).grid(row=row, column=1, sticky='nsew')
        ctk.CTkLabel(self.mapping_frame, text='Description here').grid(row=row, column=2, sticky='nsew')

    def create_mapping_table(self):
        headers = ['Key', 'Function Name', 'Description']
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.mapping_frame, text=header, font=('Helvetica', 10, 'bold'))
            label.grid(row=0, column=col, sticky='nsew')
            self.mapping_frame.grid_columnconfigure(col, weight=1)
