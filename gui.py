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
        hotkey_entry = ttk.Entry(hotkey_frame)
        hotkey_entry.pack(side="left", padx=5)
        hotkey_entry.bind("<Return>", lambda event, sk=sequence_key: self.set_hotkey(sk, hotkey_entry.get()))

    def select_video_file(self, sequence_key, monitor_num):
        filepath = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])
        if filepath:
            self.config["sequences"][sequence_key][monitor_num]["label"].configure(text=os.path.basename(filepath))
            self.config["sequences"][sequence_key][monitor_num]["button"].configure(text="Change Video")
            self.config["sequences"][sequence_key][monitor_num] = filepath

    def set_hotkey(self, sequence_key, hotkey):
        if hotkey in self.config["hotkeys"]:
            messagebox.showerror("Error", f"The hotkey '{hotkey}' is already assigned.")
            return
        self.config["hotkeys"][hotkey] = sequence_key
        messagebox.showinfo("Hotkey Set", f"Hotkey for Sequence {sequence_key} set to '{hotkey}'.")

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
