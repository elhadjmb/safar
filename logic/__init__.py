import json
import os
from .screen import Screen
from .video import Video
from .sequence import Sequence


class Config:
    """
    Manages configuration for the player.
    Saves and loads configuration to/from a file.

    The file is a JSON file with the following structure:
    {
        "screens": [
            {
                "select_index": 0,
                "name": "Monitor 1",
                "width": 1920,
                "height": 1080,
                "x": 0,
                "y": 0,
            },
            ...
        ],
        "videos": [
            {
                "video_index": 0,
                "path": "path/to/video.mp4",
                "monitor": 0,
            },
            ...
        ],
        "sequences": [
            {
                "sequence_index": 0,
                "videos": [0, 1, 2]
            },
            ...
        ]
    }

    Attributes:
        screens (List[Screen]): List of Monitor instances.
        videos (List[Video]): List of Video instances.
        sequences (List[Sequence]): List of Sequence instances.
    """

    def __init__(self, monitors: list[Screen] = None, videos: list[Video] = None,
                 sequences: list[Sequence] = None):
        self.screens = [] if monitors is None else monitors
        self.videos = [] if videos is None else videos
        self.sequences = [] if sequences is None else sequences

    def make_config_dict(self):
        """
        Make a dictionary from the attributes following the JSON structure.
        """
        config_dict = {
            "screens": [],
            "videos": [],
            "sequences": []
        }

        for screen in self.screens:
            config_dict["screens"].append({
                "select_index": screen.select_index,
                "name": screen.name,
                "width": screen.width,
                "height": screen.height,
                "y": screen.y,
                "x": screen.x
            })

        for video in self.videos:
            config_dict["videos"].append({
                "video_index": video.video_index,
                "path": video.path,
                "screen": video.monitor.select_index
            })

        for sequence in self.sequences:
            config_dict["sequences"].append({
                "sequence_index": sequence.sequence_index,
                "videos": [video.video_index for video in sequence.videos]
            })

        return config_dict

    def save(self, path="config.json"):
        """
        Save configuration to a JSON file.
        """
        config_dict = self.make_config_dict()
        with open(path, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def load(self, path="config.json"):
        """
        Load configuration from a JSON file.
        """

        with open(path, 'r') as f:
            config_dict = json.load(f)

        for screen_dict in config_dict["screens"]:
            self.screens.append(Screen(screen_dict["select_index"]))

        for video_dict in config_dict["videos"]:
            v = Video(video_dict["path"], self.screens[video_dict["screen"]])
            v.video_index = video_dict["video_index"]
            self.videos.append(v)

        for sequence_dict in config_dict["sequences"]:
            videos = []
            for video_index in sequence_dict["videos"]:
                for video in self.videos:
                    if video.video_index == video_index:
                        videos.append(video)
            self.sequences.append(Sequence(videos))


class Player:
    def __init__(self):
        self.screens = []
        self.videos = []
        self.sequences = []

    def setup_screens(self):
        """
        Set up screens based on user input or auto-detection.
        """
        auto_detect = input("Auto-detect screens? (y/n): ").lower() == 'y'
        if auto_detect:
            self.screens = Screen.detect_monitors()
        else:
            while True:
                try:
                    monitor_number = int(
                        input(f"Enter monitor number (or -1 to stop) [Monitors: {Screen.detect_monitors()}]: "))
                    if monitor_number == -1:
                        break
                    self.screens.append(Screen(select_index=monitor_number))
                except ValueError as e:
                    print(f"Error: {e}")

    def setup_videos(self):
        """
        Allow user to input video file paths.
        """
        while True:
            video_path = input("Enter video path (or 'done' to finish): ")
            if video_path.lower() == 'done':
                break
            elif os.path.exists(video_path):
                monitor_number = int(input(f"Enter monitor number [Screens: {self.screens}]: "))
                self.videos.append(Video(video_path, monitor=Screen(select_index=monitor_number)))
            else:
                print("Invalid file path.")

    def create_sequences(self):
        """
        Create sequences based on user input.
        """
        print("Creating sequences. Enter 'done' to finish.")
        while True:
            video_indices = input(f"Enter video indices (comma-separated) ({self.videos}): ")
            monitor_indices = input(f"Enter monitor indices (comma-separated) ({self.screens}): ")

            if video_indices.lower() == 'done' or monitor_indices.lower() == 'done':
                break

            try:
                video_indices = [int(v) for v in video_indices.split(',')]
                monitor_indices = [int(m) for m in monitor_indices.split(',')]
                sequence_videos = [self.videos[i] for i in video_indices]
                sequence_monitors = [self.screens[i] for i in monitor_indices]
                for video in sequence_videos:
                    video.monitor = sequence_monitors[sequence_videos.index(video)]
                self.sequences.append(Sequence(sequence_videos))
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

    def save_config(self, path="config.json"):
        """
        Save configuration to a file.
        """
        config = Config(self.screens, self.videos, self.sequences)
        config.save(path)

    def load_config(self, path="config.json"):
        """
        Load configuration from a file.
        """
        # Ask user to load the configuration
        choice = input("Load configuration? (y/n): ").lower()
        if choice == 'y':
            config = Config()
            config.load(path)
            self.screens = config.screens
            self.videos = config.videos
            self.sequences = config.sequences
        else:
            print("Not loading configuration.")
