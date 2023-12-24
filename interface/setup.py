import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk  # type: ignore


class SetupBackend:
    def __init__(self, root, config):
        self.root = root
        self.config = config

    def detect_screens(self):
        for widget in self.screen_list_frame.winfo_children():
            widget.destroy()
        self.screen_location_entries = {}  # Store the location entries for each screen
        for i, screen in enumerate(self.config.screens):
            screen_label = ctk.CTkLabel(self.screen_list_frame, text=f"Screen {i}: {screen.name}")
            screen_label.pack(pady=5, fill="x")
            blink_button = ctk.CTkButton(self.screen_list_frame, text="Blink", command=lambda s=screen: s.blink())
            blink_button.pack(pady=5)

            # Add an entry widget for location input
            location_entry = ctk.CTkEntry(self.screen_list_frame, placeholder_text="Enter Location")
            location_entry.pack(pady=5, fill="x")
            self.screen_location_entries[screen] = location_entry

    def add_video(self):
        filepath = filedialog.askopenfilename()
        screen_index = int(self.screen_index_var.get())
        if filepath:
            self.config.setup_video(filepath, screen_index)
            self.update_video_list()

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

    def map_key_sequence(self):
        key = self.key_entry.get()
        sequence_index = int(self.sequence_index_entry.get())
        self.config.setup_key_sequence_map(key, sequence_index)
        self.update_key_mapping_list()

    def update_screen_locations(self):
        """Update screen locations from the entry fields."""
        for screen, entry in self.screen_location_entries.items():
            location = entry.get()
            screen.location = location  # Assuming 'location' is an attribute of Screen

    def update_sequence_list(self):
        for widget in self.sequence_list_frame.winfo_children():
            widget.destroy()
        for sequence in self.config.sequences:
            sequence_label = ctk.CTkLabel(self.sequence_list_frame,
                                          text=f"Sequence {sequence.sequence_index}: {sequence.description}")
            sequence_label.pack(pady=5, fill="x")

    def update_key_mapping_list(self):
        for widget in self.key_mapping_list_frame.winfo_children():
            widget.destroy()
        for key, sequence_index in self.config.key_sequence_map.items():
            mapping_label = ctk.CTkLabel(self.key_mapping_list_frame, text=f"Key '{key}' -> Sequence {sequence_index}")
            mapping_label.pack(pady=5, fill="x")

    def update_video_list(self):
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()
        for video in self.config.videos:
            video_label = ctk.CTkLabel(self.video_list_frame,
                                       text=f"Video {video.video_index}: {video.path} on Screen {video.monitor.select_index}")
            video_label.pack(pady=5, fill="x")

    def save_config(self):
        try:
            self.update_screen_locations()  # Update locations before saving
            self.config.save()
            messagebox.showinfo("Success", "Configuration Saved Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")


class SetupGUI(SetupBackend):
    def __init__(self, config):
        root = ctk.CTk()
        root.title("Configuration Setup")
        super().__init__(root, config)
        self.root.geometry("600x800")
        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        # Main frame using grid layout
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Sections setup
        self.setup_screen_section(main_frame)
        self.setup_video_section(main_frame)
        self.setup_sequence_section(main_frame)
        self.setup_key_mapping_section(main_frame)
        self.setup_save_section(main_frame)

    def setup_section_frame(self, parent, row, title):
        # Section frame
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, sticky="nsew", padx=10, pady=10)
        section_frame.grid_columnconfigure(1, weight=1)

        # Section title
        ctk.CTkLabel(section_frame, text=title, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        return section_frame
    def setup_screen_section(self, parent):
        screen_frame = self.setup_section_frame(parent, 0, "")
        ctk.CTkLabel(screen_frame, text="Screen Setup", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(screen_frame, text="Detect Screens", command=self.detect_screens).grid(row=0, column=1,
                                                                                             sticky="e")
        self.screen_list_frame = ctk.CTkFrame(screen_frame)
        self.screen_list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.detect_screens()

    def setup_video_section(self, parent):
        video_frame = self.setup_section_frame(parent, 1, "")
        ctk.CTkLabel(video_frame, text="Video Setup", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")

        # Dropdown for screen index
        self.screen_index_var = tk.StringVar()
        screen_indices = [f"{i}" for i in [screen.select_index for screen in self.config.screens]]
        if screen_indices:
            self.screen_index_var.set(screen_indices[0])  # Default value
        self.screen_index_dropdown = ctk.CTkOptionMenu(video_frame, variable=self.screen_index_var,
                                                       values=screen_indices)
        self.screen_index_dropdown.grid(row=1, column=1, sticky='ew', padx=5)

        # Add Video button
        add_video_button = ctk.CTkButton(video_frame, text="Add Video", command=self.add_video)
        add_video_button.grid(row=1, column=2, sticky='e', padx=5)

        self.video_list_frame = ctk.CTkFrame(video_frame)
        self.video_list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.update_video_list()

    def setup_sequence_section(self, parent):
        sequence_frame = self.setup_section_frame(parent, 2, "")
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
        self.update_sequence_list()

    def setup_key_mapping_section(self, parent):
        key_mapping_frame = self.setup_section_frame(parent, 3, "Key Mapping")

        ctk.CTkLabel(key_mapping_frame, text="Enter Key:").grid(row=1, column=0, sticky='w', padx=5)
        self.key_entry = ctk.CTkEntry(key_mapping_frame)
        self.key_entry.grid(row=1, column=1, sticky='ew')

        ctk.CTkLabel(key_mapping_frame, text="Sequence Index:").grid(row=1, column=2, sticky='w', padx=5)
        self.sequence_index_entry = ctk.CTkEntry(key_mapping_frame)
        self.sequence_index_entry.grid(row=1, column=3, sticky='ew')

        map_key_button = ctk.CTkButton(key_mapping_frame, text="Map Key", command=self.map_key_sequence)
        map_key_button.grid(row=1, column=4, sticky='e', padx=5)

        self.key_mapping_list_frame = ctk.CTkFrame(key_mapping_frame)
        self.key_mapping_list_frame.grid(row=2, column=0, columnspan=5, sticky='ew', padx=10)
        self.update_key_mapping_list()

    def setup_save_section(self, parent):
        save_frame = self.setup_section_frame(parent, 4, "")
        ctk.CTkButton(save_frame, text="Save Configuration", command=self.save_config).grid(row=1, column=0, sticky='e')
