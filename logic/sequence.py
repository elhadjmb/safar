from multiprocessing import Process

from . import Video
from .monitor import Monitor


class Sequence:
    """
    Manages a sequence of videos to be played on different monitors.

    Attributes:
        videos (list of tuples): Each tuple contains a Video object and its corresponding Monitor.
    """

    def __init__(self, videos):
        self.videos = videos
        self.processes = []

        if not videos:
            # If no videos are specified, map black screens to all monitors.
            self._add_blackscreens()

    def start(self):
        """Start playing the sequence of videos on respective monitors."""
        for video, monitor in self.videos:
            process = Process(target=self._play_video, args=(video))
            process.start()
            self.processes.append(process)

    def _play_video(self, video):
        """Helper method to play a video on a given monitor."""
        video.play()

    def stop(self):
        """Stop all videos in the sequence."""
        for process in self.processes:
            process.terminate()
        self.processes.clear()

    def _add_blackscreens(self):
        monitors = Monitor.detect_monitors()
        for monitor in monitors:
            black_screen = Video(path=None, monitor=monitor)
            self.videos.append(black_screen)
