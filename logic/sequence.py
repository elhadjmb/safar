import random
import threading
from multiprocessing import Process

from .screen import Screen
from .video import Video


class Sequence:
    """
    Manages a sequence of videos to be played on different screens.

    Attributes:
        videos (list of Video): Contains Video objects.
    """

    def __repr__(self):
        return f"Sequence {self.sequence_index} ({len(self.videos)} videos)"

    def __init__(self, videos):
        self.sequence_index = random.randint(0, 1_000_000)
        self.videos = videos
        self.threads = []
        self.processes = []
        self.use_threads = False

        if not videos:
            # If no videos are specified, map black screens to all screens.
            self._add_blackscreens()

    def start(self):
        """Start playing the sequence of videos on respective screens."""
        if not self.use_threads:
            for video in self.videos:
                thread = threading.Thread(target=self._play_video, args=(video,))
                thread.start()
                self.threads.append(thread)
        else:
            for video in self.videos:
                process = Process(target=self._play_video, args=(video,))
                process.start()
                self.processes.append(process)

    def _play_video(self, video):
        """Helper method to play a video on a given monitor."""
        video.play()

    def stop(self):
        """Stop all videos in the sequence."""
        for video in self.videos:
            video.stop()
        if not self.use_threads:
            for thread in self.threads:
                thread.join()
            self.threads.clear()
        else:
            for process in self.processes:
                process.join()
            self.processes.clear()

    def _add_blackscreens(self):
        monitors = Screen.detect_monitors()
        for monitor in monitors:
            black_screen = Video(path=None, monitor=monitor)
            self.videos.append(black_screen)

    def freeze(self):
        """Pause all videos in the sequence."""
        for video in self.videos:
            video.pause()
