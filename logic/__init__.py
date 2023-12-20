import json
import os
from .monitor import Monitor
from .video import Video
from .sequence import Sequence


class Config:
    """
    Manages configuration for the player.
    Saves and loads configuration to/from a file.

    The file is a JSON file with the following structure:
    {
        "monitors": [
            {
                "name": "Monitor 1",
                "info": {
                    "width": 1920,
                    "height": 1080,
                    "x": 0,
                    "y": 0
                }
            },
            {
                "name": "Monitor 2",
                "info": {
                    "width": 1920,
                    "height": 1080,
                    "x": 1920,
                    "y": 0
                }
            }
        ],
        "videos": [
            {
                "path": "C:\\Users\\User\\Videos\\video1.mp4"
            },
            {
                "path": "C:\\Users\\User\\Videos\\video2.mp4"
            }
        ],
        "sequences": [
            {
                "videos": [0, 1],
                "monitors": [0, 1]
            }
        ]
    }

    Attributes:
        monitors (List[Monitor]): List of Monitor instances.
        videos (List[Video]): List of Video instances.
        sequences (List[Sequence]): List of Sequence instances.
        path (str): Path to the configuration file.
    """

    def __init__(self, path: str = None, monitors: list[Monitor] = None, videos: list[Video] = None,
                 sequences: list[Sequence] = None):
        self.monitors = [] if monitors is None else monitors
        self.videos = [] if videos is None else videos
        self.sequences = [] if sequences is None else sequences
        self.path = path

    def save(self, path):
        """
        Save configuration to a JSON file from the attributes.
        """
        # Create a dictionary from the attributes
        config_dict = {
            "monitors": [
                {
                    "name": m.name,
                    "info": {
                        "width": m.info.width,
                        "height": m.info.height,
                        "x": m.info.x,
                        "y": m.info.y
                    }
                } for m in self.monitors
            ],
            "videos": [
                {
                    "path": v.path
                } for v in self.videos
            ],
            "sequences": [
                {
                    "videos": [self.videos.index(v) for v in s.videos],
                    "monitors": [self.monitors.index(m) for m in s.monitors]
                } for s in self.sequences
            ]
        }

        # Save the dictionary to a JSON file
        with open(path, 'w') as f:
            json.dump(config_dict, f, indent=4, default=str)

    def load(self, path):
        """
        Load configuration from a file.
        """
        with open(path, 'r') as f:
            config_dict = json.load(f)

        # Load monitors
        for monitor_dict in config_dict['monitors']:
            self.monitors.append(Monitor(monitor_dict['name']))

        # Load videos
        for video_dict in config_dict['videos']:
            self.videos.append(Video(video_dict['path']))

        # Load sequences
        for sequence_dict in config_dict['sequences']:
            sequence_videos = [self.videos[i] for i in sequence_dict['videos']]
            sequence_monitors = [self.monitors[i] for i in sequence_dict['monitors']]
            self.sequences.append(Sequence(sequence_videos, sequence_monitors))


class Player:
    def __init__(self):
        self.monitors = []
        self.videos = []
        self.sequences = []

    def setup_monitors(self):
        """
        Set up monitors based on user input or auto-detection.
        """
        auto_detect = input("Auto-detect monitors? (y/n): ").lower() == 'y'
        if auto_detect:
            self.monitors = [Monitor(m) for m in Monitor.get_monitors()]
        else:
            while True:
                try:
                    monitor_number = int(input(f"Enter monitor number (or -1 to stop) [Monitors: {}]: "))
                    if monitor_number == -1:
                        break
                    self.monitors.append(Monitor(monitor_number))
                except ValueError as e:
                    print(f"Error: {e}")

        for monitor in self.monitors:

    def setup_videos(self):
        """
        Allow user to input video file paths.
        """
        while True:
            video_path = input("Enter video path (or 'done' to finish): ")
            if video_path.lower() == 'done':
                break
            elif os.path.exists(video_path):
                self.videos.append(Video(video_path))
            else:
                print("Invalid file path.")

    def create_sequences(self):
        """
        Create sequences based on user input.
        """
        print("Creating sequences. Enter 'done' to finish.")
        while True:
            video_indices = input("Enter video indices (comma-separated): ")
            monitor_indices = input("Enter monitor indices (comma-separated): ")

            if video_indices.lower() == 'done' or monitor_indices.lower() == 'done':
                break

            try:
                video_indices = [int(v) for v in video_indices.split(',')]
                monitor_indices = [int(m) for m in monitor_indices.split(',')]
                sequence_videos = [self.videos[i] for i in video_indices]
                sequence_monitors = [self.monitors[i] for i in monitor_indices]
                self.sequences.append(Sequence(sequence_videos, sequence_monitors))
            except (IndexError, ValueError) as e:
                print(f"Error creating sequence: {e}")

    def start_sequence(self, sequence_id):
        """
        Start a specific video sequence.
        """
        try:
            self.sequences[sequence_id].start()
        except IndexError:
            print("Invalid sequence ID.")

    def stop_sequence(self, sequence_id):
        """
        Stop a specific video sequence.
        """
        try:
            self.sequences[sequence_id].stop()
        except IndexError:
            print("Invalid sequence ID.")

    def save_config(self, path):
        """
        Save configuration to a file.
        """
        config = Config(path, self.monitors, self.videos, self.sequences)
        config.save(path)

    def load_config(self, path):
        """
        Load configuration from a file.
        """
        # Ask user to load the configuration
        choice = input("Load configuration? (y/n): ").lower()
        if choice == 'y':
            config = Config()
            config.load(path)
            self.monitors = config.monitors
            self.videos = config.videos
            self.sequences = config.sequences
        else:
            print("Not loading configuration.")
