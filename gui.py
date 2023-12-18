import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class VideoSequenceConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Sequence Configurator")

        self.config = {"sequences": {}, "hotkeys": {}}
        self.setup_ui()

    def setup_ui(self):
        self.sequence_frame = tk.Frame(self.root)
        self.sequence_frame.pack(pady=10)

        self.add_sequence_button = tk.Button(self.root, text="Add Video Sequence", command=self.add_video_sequence)
        self.add_sequence_button.pack(pady=10)

        self.save_config_button = tk.Button(self.root, text="Save Configuration", command=self.save_configuration)
        self.save_config_button.pack(pady=10)

    def add_video_sequence(self):
        sequence_id = len(self.config["sequences"]) + 1
        sequence_key = str(sequence_id)

        sequence_frame = tk.LabelFrame(self.sequence_frame, text=f"Sequence {sequence_id}", padx=10, pady=10)
        sequence_frame.pack(padx=10, pady=5, fill="x")

        monitors = self.get_monitors()
        videos = []
        for monitor_num in range(len(monitors)):
            file_button = tk.Button(sequence_frame, text=f"Select Video for Monitor {monitor_num + 1}",
                                    command=lambda m=monitor_num: self.select_video_file(sequence_key, m))
            file_button.pack(padx=5, pady=5)
            videos.append("")

        hotkey_label = tk.Label(sequence_frame, text="Hotkey:")
        hotkey_label.pack(side=tk.LEFT, padx=5)
        hotkey_entry = tk.Entry(sequence_frame)
        hotkey_entry.pack(side=tk.LEFT, padx=5)
        hotkey_entry.bind("<Return>", lambda event, sk=sequence_key: self.set_hotkey(sk, hotkey_entry.get()))

        self.config["sequences"][sequence_key] = videos

    def select_video_file(self, sequence_key, monitor_num):
        filepath = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])
        if filepath:
            self.config["sequences"][sequence_key][monitor_num] = filepath

    def set_hotkey(self, sequence_key, hotkey):
        self.config["hotkeys"][hotkey] = sequence_key

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
        # TODO:replace with actual monitor detection logic
        return [0, 1]  # Assuming two monitors