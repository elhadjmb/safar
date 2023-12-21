import random
import threading

from . import Video
from .screen import Screen


class Sequence:
    """
    Manages a sequence of videos to be played on different screens.

    Attributes:
        videos (list of tuples): Each tuple contains a Video object and its corresponding Monitor.
    """

    def __repr__(self):
        return f"Sequence {self.sequence_index} ({len(self.videos)} videos)"

    def __init__(self, videos):
        self.sequence_index = random.randint(0, 1_000_000)
        self.videos = videos
        self.threads = []

        if not videos:
            # If no videos are specified, map black screens to all screens.
            self._add_blackscreens()

    def start(self):
        """Start playing the sequence of videos on respective screens."""
        for video in self.videos:
            thread = threading.Thread(target=self._play_video, args=(video,))
            thread.start()
            self.threads.append(thread)

    def _play_video(self, video):
        """Helper method to play a video on a given monitor."""
        video.play()

    def stop(self):
        """Stop all videos in the sequence."""
        for video in self.videos:
            video.stop()
        for thread in self.threads:
            thread.join()
        self.threads.clear()

    def _add_blackscreens(self):
        monitors = Screen.detect_monitors()
        for monitor in monitors:
            black_screen = Video(path=None, monitor=monitor)
            self.videos.append(black_screen)

    def freeze(self):
        """Pause all videos in the sequence."""
        for video in self.videos:
            video.pause()
