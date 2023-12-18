import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os

from logic import Monitor


class VideoSequenceConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Sequence Configurator")
        self.root.geometry("600x500")

        self.config = {"sequences": {}, "hotkeys": {}}
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.sequence_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.sequence_frame, anchor="nw")

        self.add_sequence_button = ttk.Button(self.root, text="Add Video Sequence", command=self.add_video_sequence)
        self.add_sequence_button.pack(pady=10)

        self.save_config_button = ttk.Button(self.root, text="Save Configuration",
                                             command=self.confirm_save_configuration)
        self.save_config_button.pack(pady=10)

        self.load_config_button = ttk.Button(self.root, text="Load Configuration",
                                             command=self.load_and_display_configuration)
        self.load_config_button.pack(pady=10)

        self.load_from_file_button = ttk.Button(self.root, text="Load Config from File",
                                                command=self.load_and_display_configuration)
        self.load_from_file_button.pack(pady=10)

        self.use_current_config_button = ttk.Button(self.root, text="Use Current Configuration",
                                                    command=self.create_playback_interface)
        self.use_current_config_button.pack(pady=10)

    def add_video_sequence(self):
        sequence_id = len(self.config["sequences"]) + 1
        sequence_key = str(sequence_id)

        sequence_frame = ttk.LabelFrame(self.sequence_frame, text=f"Sequence {sequence_id}")
        sequence_frame.pack(padx=10, pady=10, fill="x", expand=True)

        monitors = self.get_monitors()
        videos = []
        for monitor_num in range(len(monitors)):
            monitor_frame = ttk.Frame(sequence_frame)
            monitor_frame.pack(padx=10, pady=5, fill="x", expand=True)

            file_button = ttk.Button(monitor_frame, text=f"Select Video for Monitor {monitor_num + 1}",
                                     command=lambda m=monitor_num: self.select_video_file(sequence_key, m))
            file_button.pack(side="left", padx=10)

            file_label = ttk.Label(monitor_frame, text="No file selected", width=40)
            file_label.pack(side="left", padx=10)
            videos.append({"button": file_button, "label": file_label})

        self.config["sequences"][sequence_key] = videos

        hotkey_frame = ttk.Frame(sequence_frame)
        hotkey_frame.pack(padx=10, pady=5, fill="x", expand=True)

        hotkey_label = ttk.Label(hotkey_frame, text="Hotkey:")
        hotkey_label.pack(side="left", padx=5)
        hotkey_button = ttk.Button(sequence_frame, text="Set Hotkey",
                                   command=lambda sk=sequence_key: self.capture_hotkey(sk))
        hotkey_button.pack(side="left", padx=5)

    def capture_hotkey(self, sequence_key):
        self.hotkey_capture_window = tk.Toplevel(self.root)
        self.hotkey_capture_window.title("Press a Key for Hotkey")
        self.hotkey_capture_window.geometry("200x100")
        tk.Label(self.hotkey_capture_window, text="Press a key...").pack(pady=20)
        self.hotkey_capture_window.bind("<Key>", lambda event: self.set_hotkey(sequence_key, event))

    def set_hotkey(self, sequence_key, input):
        # Determine if input is an event or a string
        hotkey = input.keysym if isinstance(input, tk.Event) else input

        # Check for hotkey conflicts
        if hotkey in self.config["hotkeys"] and self.config["hotkeys"][hotkey] != sequence_key:
            response = messagebox.askyesno("Hotkey Conflict",
                                           f"The hotkey '{hotkey}' is already assigned. Do you want to reassign it?")
            if not response:
                return

        self.config["hotkeys"][hotkey] = sequence_key
        messagebox.showinfo("Hotkey Set", f"Hotkey for Sequence {sequence_key} set to '{hotkey}'.")

        if isinstance(input, tk.Event):
            self.hotkey_capture_window.destroy()

    def select_video_file(self, sequence_key, monitor_num):
        filepath = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])
        if filepath:
            self.config["sequences"][sequence_key][monitor_num]["label"].configure(text=os.path.basename(filepath))
            self.config["sequences"][sequence_key][monitor_num]["button"].configure(text="Change Video")
            self.config["sequences"][sequence_key][monitor_num] = filepath

    def check_configuration_ready(self):
        if self.config["sequences"] and self.config["hotkeys"]:
            self.use_current_config_button["state"] = "normal"
        else:
            self.use_current_config_button["state"] = "disabled"

    def confirm_save_configuration(self):
        if messagebox.askokcancel("Confirm Save", "Are you sure you want to save this configuration?"):
            self.save_configuration()

    def save_configuration(self):
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)
        messagebox.showinfo("Configuration Saved", "The configuration has been saved successfully.")

    def load_configuration(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)

    @staticmethod
    def get_monitors():
        return Monitor.get_monitors()

    def load_and_display_configuration(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
            self.display_loaded_configuration()
        else:
            messagebox.showinfo("Load Configuration", "No saved configuration found.")

    def display_loaded_configuration(self):
        for sequence_key, videos in self.config["sequences"].items():
            self.add_loaded_sequence(sequence_key, videos)

    def add_loaded_sequence(self, sequence_key, videos):
        sequence_id = sequence_key
        sequence_frame = ttk.LabelFrame(self.sequence_frame, text=f"Sequence {sequence_id}", padx=10, pady=10)
        sequence_frame.pack(padx=10, pady=5, fill="x", expand=True)

        for monitor_num, video_path in enumerate(videos):
            monitor_frame = ttk.Frame(sequence_frame)
            monitor_frame.pack(padx=10, pady=5, fill="x", expand=True)

            file_label = ttk.Label(monitor_frame,
                                   text=os.path.basename(video_path) if video_path else "No file selected", width=40)
            file_label.pack(side="left", padx=10)

        # Add hotkey entry if exists in config
        hotkey = [k for k, v in self.config["hotkeys"].items() if v == sequence_key]
        hotkey_label = ttk.Label(sequence_frame, text="Hotkey:")
        hotkey_label.pack(side="left", padx=5)
        hotkey_entry = ttk.Entry(sequence_frame)
        hotkey_entry.insert(0, hotkey[0] if hotkey else "")
        hotkey_entry.pack(side="left", padx=5)

    def create_playback_interface(self):
        self.playback_window = tk.Toplevel(self.root)
        self.playback_window.title("Playback Interface")
        self.hotkey_labels = {}

        for hotkey, sequence_key in self.config["hotkeys"].items():
            label_text = f"Hotkey: {hotkey} - Sequence: {sequence_key}"
            label = ttk.Label(self.playback_window, text=label_text)
            label.pack()
            self.hotkey_labels[hotkey] = label

        self.playback_window.bind("<Key>", self.handle_hotkey_press)

    def handle_hotkey_press(self, event):
        hotkey = event.keysym
        if hotkey in self.config["hotkeys"]:
            sequence_key = self.config["hotkeys"][hotkey]
            self.start_video_sequence(sequence_key)
            self.highlight_hotkey(hotkey)

    def start_video_sequence(self, sequence_key):
        from logic import VideoSequence
        sequence_data = self.config["sequences"].get(sequence_key)
        if sequence_data:
            video_sequence = VideoSequence({sequence_key: sequence_data})
            video_sequence.start_sequence(sequence_key)
