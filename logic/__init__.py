import json
import os

from .screen import Screen
from .sequence import Sequence, Video


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
                "screen": 0,
            },
            ...
        ],
        "sequences": [
            {
                "sequence_index": 0,
                "videos": [0, 1, 2],
                "description": "Description here"
            },
            ...
        ],
        "key_sequence_map": {
            "c": 0,
            "o": 1
        }
    }

    Attributes:
        screens (List[Screen]): List of Monitor instances.
        videos (List[Video]): List of Video instances.
        sequences (List[Sequence]): List of Sequence instances.
    """

    def __init__(self, monitors: list[Screen] = None, videos: list[Video] = None,
                 sequences: list[Sequence] = None, key_sequence_map: dict[str, Sequence] = None):
        self.screens = [] if monitors is None else monitors
        self.videos = [] if videos is None else videos
        self.sequences = [] if sequences is None else sequences
        self.key_sequence_map = key_sequence_map if key_sequence_map is not None else {}

        self.video_index = 0
        self.sequence_index = 0

        if not self.screens:
            self.setup_screens()
        if not self.videos:
            for screen_index in range(len(self.screens)):
                self.setup_video("", 0)

        temp_videos = []
        for video_index in range(len(self.videos)):
            if not self.videos[video_index].path:
                temp_videos.append(self.videos[video_index])
            temp_video_indexes = []
            for video in temp_videos:
                temp_video_indexes.append(video.video_index)
            self.setup_sequence(temp_video_indexes, "BLACK SCREENS")
            for sequence in self.sequences:
                if sequence.description == "BLACK SCREENS":
                    self.setup_key_sequence_map("0", sequence.sequence_index)
                    break

    def setup_screens(self):
        """
        Set up screens based on auto-detection.
        """
        print("Auto-detecting screens...")
        self.screens = Screen.detect_monitors()

    def setup_video(self, video_path: str, screen_index: int):
        if os.path.exists(video_path):
            video = Video(video_path, monitor=self.screens[screen_index], video_index=self.video_index)
            self.videos.append(video)
            self.video_index += 1
        else:
            print("Invalid file path.")

    def setup_sequence(self, videos_indexes: list[int], description: str):
        """
        Create sequences based on selected videos list.
        """
        videos_list = [self.videos[index] for index in videos_indexes]
        sequence = Sequence(videos_list, sequence_index=self.sequence_index, description=description)
        self.sequences.append(sequence)
        self.sequence_index += 1

    def setup_key_sequence_map(self, key: str, sequence_index: int):
        """
        Create key sequence map based on selected key and sequence.
        """
        self.key_sequence_map[key] = sequence_index

    def make_config_dict(self):
        """
        Make a dictionary from the attributes following the JSON structure.
        """
        config_dict = {
            "screens": [],
            "videos": [],
            "sequences": [],
            "key_sequence_map": self.key_sequence_map
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
                "videos": [video.video_index for video in sequence.videos],
                "description": sequence.description
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

        if "key_sequence_map" in config_dict:
            self.key_sequence_map = config_dict["key_sequence_map"]

        for screen_dict in config_dict["screens"]:
            self.screens.append(Screen(screen_dict["select_index"]))

        for video_dict in config_dict["videos"]:
            v = Video(video_dict["path"], self.screens[video_dict["screen"]])
            v.video_index = video_dict["video_index"]
            self.videos.append(v)

        for sequence_dict in config_dict["sequences"]:
            videos = []
            description = sequence_dict["description"]
            for video_index in sequence_dict["videos"]:
                for video in self.videos:
                    if video.video_index == video_index:
                        videos.append(video)
            self.sequences.append(
                Sequence(videos, sequence_index=sequence_dict["sequence_index"], description=description))


class Player:
    def __init__(self, headless=False, config: Config = None):
        self.key_sequence_map = None
        self.config = config if config is not None else Config()
        self.screens = []
        self.videos = []
        self.sequences = []
        self.headless = headless
        self.played_sequence = None
        self.load_config()

    def create_key_function_map(self):
        key_function_map = {}
        for key, sequence_index in self.key_sequence_map.items():
            key_function_map[key] = (
                lambda idx=sequence_index: self.start_sequence(idx), self.sequences[sequence_index].description)
        return key_function_map

    def start_sequence(self, sequence_id):
        """
        Start a specific video sequence.
        """
        try:
            if self.played_sequence is not None:
                self.sequences[self.played_sequence].stop()
            self.played_sequence = sequence_id
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

    def load_config(self, path="config.json"):
        """
        Load configuration from a file.
        """
        self.config.load(path)
        self.screens = self.config.screens
        self.videos = self.config.videos
        self.sequences = self.config.sequences
        self.key_sequence_map = self.config.key_sequence_map

    def kill_all_sequences(self):
        for sequence in self.sequences:
            self.stop_sequence(sequence.sequence_index)
