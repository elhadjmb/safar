import json
from tkinter import filedialog, simpledialog

import customtkinter as ctk  # type: ignore

from logic import Config


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
        self.create_setup_button()
        self.create_kill_all_button()
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
                self.key_function_map[key][0]()
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
        # TODO: Add more setup components here as needed
        ctk.set_appearance_mode("dark")  # Set the theme of GUI
        root = ctk.CTk()
        root.title("Configuration Setup")
        app = ConfigGUI(root, Config())
        root.mainloop()

    def update_key_function_map(self):
        self.key_function_map = self.player.create_key_function_map()
        self.populate_mapping_table()

    def populate_mapping_table(self):
        self.clear_existing_mapping_rows()
        for row, (key, (func, desc)) in enumerate(self.key_function_map.items(), start=1):
            self.add_mapping_row(row, key, desc)

    def clear_existing_mapping_rows(self):
        for widget in self.mapping_frame.winfo_children():
            if not isinstance(widget, ctk.CTkLabel):  # Skip header labels
                widget.destroy()

    def add_mapping_row(self, row, key, desc):
        ctk.CTkLabel(self.mapping_frame, text=key).grid(row=row, column=0, sticky='nsew')
        ctk.CTkLabel(self.mapping_frame, text=desc).grid(row=row, column=1, sticky='nsew')

    def create_mapping_table(self):
        headers = ['Key', 'Description']
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.mapping_frame, text=header, font=('Helvetica', 10, 'bold'))
            label.grid(row=0, column=col, sticky='nsew')
            self.mapping_frame.grid_columnconfigure(col, weight=1)

    def create_kill_all_button(self):
        self.kill_all_button = ctk.CTkButton(self.root, text="Kill All", command=self.kill_all_videos, fg_color="red")
        self.kill_all_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    def kill_all_videos(self):
        self.player.kill_all_sequences()
        self.status_bar.configure(text="All videos forcefully stopped.")


class ConfigGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.geometry("500x700")
        self.setup_widgets()

    def setup_widgets(self):
        # Screen Setup Section
        self.setup_screen_section()

        # Video Setup Section
        self.setup_video_section()

        # Sequence Setup Section
        self.setup_sequence_section()

        # Key Mapping Section
        self.setup_key_mapping_section()

        # Save Configuration Section
        self.setup_save_section()

    def setup_screen_section(self):
        screen_frame = ctk.CTkFrame(self.root)
        screen_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(screen_frame, text="Screen Setup", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(screen_frame, text="Detect Screens", command=self.detect_screens).pack(side="right")

    def detect_screens(self):
        self.config.setup_screens()
        for i, screen in enumerate(self.config.screens):
            screen_label = ctk.CTkLabel(self.root, text=f"Screen {i}: {screen.name}")
            screen_label.pack()
            blink_button = ctk.CTkButton(self.root, text="Blink", command=lambda s=screen: s.blink())
            blink_button.pack()

    def setup_video_section(self):
        self.video_frame = ctk.CTkFrame(self.root)
        self.video_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(self.video_frame, text="Video Setup", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(self.video_frame, text="Add Video", command=self.add_video).pack(side="right")
        self.video_list_frame = ctk.CTkFrame(self.root)
        self.video_list_frame.pack(pady=10, fill="x")

    def add_video(self):
        filepath = filedialog.askopenfilename()
        screen_index = simpledialog.askinteger("Input", "Enter Screen Index")
        self.config.setup_video(filepath, screen_index)
        self.update_video_list()

    def update_video_list(self):
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()
        # Display video list
        for video in self.config.videos:
            video_info_frame = ctk.CTkFrame(self.video_list_frame)
            video_info_frame.pack(pady=5, fill="x")
            video_label = ctk.CTkLabel(video_info_frame,
                                       text=f"Video {video.video_index}: {video.path} on Screen {video.monitor.select_index}")
            video_label.pack(side="left", padx=10)

    def setup_sequence_section(self):
        self.sequence_frame = ctk.CTkFrame(self.root)
        self.sequence_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(self.sequence_frame, text="Sequence Setup", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(self.sequence_frame, text="Add Sequence", command=self.add_sequence).pack(side="right")
        self.sequence_list_frame = ctk.CTkFrame(self.root)
        self.sequence_list_frame.pack(pady=10, fill="x")

    def add_sequence(self):
        video_indexes = simpledialog.askstring("Input", "Enter Video Indexes (comma-separated)")
        description = simpledialog.askstring("Input", "Enter Sequence Description")
        video_indexes = [int(i.strip()) for i in video_indexes.split(',')]
        self.config.setup_sequence(video_indexes, description)
        self.update_sequence_list()

    def update_sequence_list(self):
        for widget in self.sequence_list_frame.winfo_children():
            widget.destroy()
        for sequence in self.config.sequences:
            sequence_label = ctk.CTkLabel(self.sequence_list_frame,
                                          text=f"Sequence {sequence.sequence_index}: {sequence.description}")
            sequence_label.pack()

    def setup_key_mapping_section(self):
        self.key_mapping_frame = ctk.CTkFrame(self.root)
        self.key_mapping_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(self.key_mapping_frame, text="Key Mapping", font=("Arial", 12, "bold")).pack(side="left")
        self.key_entry = ctk.CTkEntry(self.key_mapping_frame, placeholder_text="Enter Key")
        self.key_entry.pack(side="left", padx=5)
        self.sequence_index_entry = ctk.CTkEntry(self.key_mapping_frame, placeholder_text="Enter Sequence Index")
        self.sequence_index_entry.pack(side="left", padx=5)
        ctk.CTkButton(self.key_mapping_frame, text="Map Key", command=self.map_key_sequence).pack(side="right")

        # Frame to display key mappings
        self.key_mapping_list_frame = ctk.CTkFrame(self.root)
        self.key_mapping_list_frame.pack(pady=10, fill="x")

    def map_key_sequence(self):
        key = self.key_entry.get()
        sequence_index = int(self.sequence_index_entry.get())
        self.config.setup_key_sequence_map(key, sequence_index)
        self.update_key_mapping_list()

    def update_key_mapping_list(self):
        for widget in self.key_mapping_list_frame.winfo_children():
            widget.destroy()
        for key, sequence_index in self.config.key_sequence_map.items():
            mapping_label = ctk.CTkLabel(self.key_mapping_list_frame, text=f"Key '{key}' -> Sequence {sequence_index}")
            mapping_label.pack()

    def setup_save_section(self):
        save_frame = ctk.CTkFrame(self.root)
        save_frame.pack(pady=20, fill="x")
        ctk.CTkButton(save_frame, text="Save Configuration", command=self.save_config).pack()

    def save_config(self):
        self.config.save()
        status_label = ctk.CTkLabel(self.container_frame, text="Configuration Saved", text_color="green")
        status_label.pack(pady=10)
