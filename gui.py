import tkinter as tk
from tkinter import ttk

from logic import Player


class KeyPressGUI:
    def __init__(self, player):
        self.player = player
        self.key_function_map = {}
        self.root = tk.Tk()
        self.root.title("SAFAR!")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a nicer theme
        self.root.configure(bg='light gray')

        # Instructions label
        instruction_text = "Press a key to execute its corresponding function."
        self.instructions_label = ttk.Label(self.root, text=instruction_text, font=("Helvetica", 12))
        self.instructions_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Key-Function Mapping Display
        self.mapping_display = ttk.Treeview(self.root, columns=('Key', 'Function'), show='headings')
        self.mapping_display.heading('Key', text='Key')
        self.mapping_display.heading('Function', text='Function Name')
        self.mapping_display.column('Key', width=100)
        self.mapping_display.column('Function', width=200)
        self.mapping_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Load Config Button
        self.load_config_button = ttk.Button(self.root, text="Load Config", command=self.load_config)
        self.load_config_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Update key-function map and populate Treeview
        self.load_config()

        # Populate the treeview with key-function map
        for key, func in self.key_function_map.items():  # Corrected this line
            self.mapping_display.insert('', 'end', values=(key, func.__name__))

        # Last key pressed display
        self.last_key_label = ttk.Label(self.root, text="Last Key Pressed: None", font=("Helvetica", 12))
        self.last_key_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # General key binding
        self.root.bind('<Key>', self.key_pressed)

        # Window size and layout
        self.root.geometry('400x400')
        self.root.minsize(400, 400)

        # Start the GUI
        self.root.mainloop()

    def key_pressed(self, event):
        key = event.keysym
        self.last_key_label.config(text=f"Last Key Pressed: {key}")
        if key in self.key_function_map:
            self.key_function_map[key]()

    def load_config(self):
        config_path = "config.json"
        self.player.load_config(config_path)
        # Update the key-function map and the GUI display
        self.update_key_function_map()

    def update_key_function_map(self):
        self.key_function_map = self.player.create_key_function_map()
        self.mapping_display.delete(*self.mapping_display.get_children())  # Clear existing entries
        for key, func in self.key_function_map.items():
            self.mapping_display.insert('', 'end', values=(key, func.__name__))


player = Player(headless=True)
gui = KeyPressGUI(player)
