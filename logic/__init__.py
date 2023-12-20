import os
from .monitor import Monitor
from .video import Video
from .sequence import Sequence


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
            self.monitors = [Monitor(m.number) for m in Monitor.get_monitors()]
        else:
            while True:
                try:
                    monitor_number = int(input("Enter monitor number (or -1 to stop): "))
                    if monitor_number == -1:
                        break
                    self.monitors.append(Monitor(monitor_number))
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
