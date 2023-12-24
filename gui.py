import json
from tkinter import filedialog, simpledialog, messagebox

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
        app = ConfigGUI(root, self.player.config)
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
        self.root.geometry("600x800")
        self.setup_widgets()

    def setup_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = ctk.CTkCanvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(main_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        content_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Setup sections
        self.setup_screen_section(content_frame)
        self.setup_video_section(content_frame)
        self.setup_sequence_section(content_frame)
        self.setup_key_mapping_section(content_frame)
        self.setup_save_section(content_frame)

        # Configure grid for content_frame to expand elements
        content_frame.grid_columnconfigure(0, weight=1)
        for i in range(5):
            content_frame.grid_rowconfigure(i, weight=1)

    def setup_section_frame(self, parent, row):
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, sticky="nsew", padx=10, pady=10)
        section_frame.grid_columnconfigure(1, weight=1)
        return section_frame

    def setup_screen_section(self, parent):
        screen_frame = self.setup_section_frame(parent, 0)
        ctk.CTkLabel(screen_frame, text="Screen Setup", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(screen_frame, text="Detect Screens", command=self.detect_screens).grid(row=0, column=1,
                                                                                             sticky="e")
        self.screen_list_frame = ctk.CTkFrame(screen_frame)
        self.screen_list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def detect_screens(self):
        for widget in self.screen_list_frame.winfo_children():
            widget.destroy()
        self.config.setup_screens()
        for i, screen in enumerate(self.config.screens):
            screen_label = ctk.CTkLabel(self.screen_list_frame, text=f"Screen {i}: {screen.name}")
            screen_label.pack(pady=5, fill="x")
            blink_button = ctk.CTkButton(self.screen_list_frame, text="Blink", command=lambda s=screen: s.blink())
            blink_button.pack(pady=5)

    def setup_video_section(self, parent):
        video_frame = self.setup_section_frame(parent, 1)
        ctk.CTkLabel(video_frame, text="Video Setup", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(video_frame, text="Add Video", command=self.add_video).grid(row=0, column=1, sticky="e")
        self.video_list_frame = ctk.CTkFrame(video_frame)
        self.video_list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def add_video(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            screen_index = simpledialog.askinteger("Input", "Enter Screen Index")
            self.config.setup_video(filepath, screen_index)
            self.update_video_list()

    def update_video_list(self):
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()
        for video in self.config.videos:
            video_label = ctk.CTkLabel(self.video_list_frame,
                                       text=f"Video {video.video_index}: {video.path} on Screen {video.monitor.select_index}")
            video_label.pack(pady=5, fill="x")

    def setup_sequence_section(self, parent):
        sequence_frame = self.setup_section_frame(parent, 2)
        ctk.CTkLabel(sequence_frame, text="Sequence Setup", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                             sticky='w')
        self.video_indexes_entry = ctk.CTkEntry(sequence_frame,
                                                placeholder_text="Enter Video Indexes (comma-separated)")
        self.video_indexes_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.sequence_description_entry = ctk.CTkEntry(sequence_frame, placeholder_text="Enter Sequence Description")
        self.sequence_description_entry.grid(row=0, column=2, sticky='ew', padx=5)
        ctk.CTkButton(sequence_frame, text="Add Sequence", command=self.add_sequence).grid(row=0, column=3, sticky='e')

        self.sequence_list_frame = ctk.CTkFrame(parent)
        self.sequence_list_frame.grid(row=3, column=0, sticky='ew', padx=10)

    def add_sequence(self):
        video_indexes = self.video_indexes_entry.get()
        description = self.sequence_description_entry.get()
        if video_indexes and description:
            try:
                video_indexes = [int(i.strip()) for i in video_indexes.split(',')]
                self.config.setup_sequence(video_indexes, description)
                self.update_sequence_list()
            except ValueError:
                messagebox.showerror("Error", "Invalid video indexes format")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields")

    def update_sequence_list(self):
        for widget in self.sequence_list_frame.winfo_children():
            widget.destroy()
        for sequence in self.config.sequences:
            sequence_label = ctk.CTkLabel(self.sequence_list_frame,
                                          text=f"Sequence {sequence.sequence_index}: {sequence.description}")
            sequence_label.pack(pady=5, fill="x")

    def setup_key_mapping_section(self, parent):
        key_mapping_frame = ctk.CTkFrame(parent)
        key_mapping_frame.grid(row=6, column=0, sticky='ew', padx=10, pady=10)
        key_mapping_frame.grid_columnconfigure(1, weight=1)
        key_mapping_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(key_mapping_frame, text="Key Mapping", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                             sticky='w')
        self.key_entry = ctk.CTkEntry(key_mapping_frame, placeholder_text="Enter Key")
        self.key_entry.grid(row=0, column=1, sticky='ew')
        self.sequence_index_entry = ctk.CTkEntry(key_mapping_frame, placeholder_text="Enter Sequence Index")
        self.sequence_index_entry.grid(row=0, column=2, sticky='ew')
        ctk.CTkButton(key_mapping_frame, text="Map Key", command=self.map_key_sequence).grid(row=0, column=3,
                                                                                             sticky='e')

        self.key_mapping_list_frame = ctk.CTkFrame(parent)
        self.key_mapping_list_frame.grid(row=7, column=0, sticky='ew', padx=10)

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
            mapping_label.pack(pady=5, fill="x")

    def setup_save_section(self, parent):
        save_frame = self.setup_section_frame(parent, 4)
        ctk.CTkButton(save_frame, text="Save Configuration", command=self.save_config).grid(row=0, column=0, sticky='e')

    def save_config(self):
        try:
            self.config.save()
            messagebox.showinfo("Success", "Configuration Saved Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
