from multiprocessing import Process

from .monitor import Monitor


class Sequence:
    """
    Manages a sequence of videos to be played on specified monitors.

    Attributes:
        videos (List[Video]): List of Video instances.
        monitors (List[Monitor]): List of Monitor instances.
        _processes (List[Process]): Internal list of processes for video playback.

    Methods:
        start: Start playing the video sequence on the specified monitors.
        stop: Stop the video sequence on all monitors.
    """

    def __init__(self, videos=None, monitors=None):
        """
        Initialize a Sequence instance.

        Args:
            videos (List[Video], optional): List of Video instances.
            monitors (List[Monitor], optional): List of Monitor instances.
        """
        self.videos = videos or []
        self.monitors = monitors or Monitor.get_monitors()
        self._processes = []

        # Ensure videos and monitors are mapped correctly.
        if len(self.videos) != len(self.monitors):
            raise ValueError("The number of videos must match the number of monitors.")

    def start(self):
        """
        Start playing the video sequence on the specified monitors.
        """
        for video, monitor in zip(self.videos, self.monitors):
            process = Process(target=self._play_video_on_monitor, args=(video, monitor))
            process.start()
            self._processes.append(process)

    def _play_video_on_monitor(self, video, monitor):
        """
        Play a video on a specified monitor.

        Args:
            video (Video): The video to be played.
            monitor (Monitor): The monitor on which to play the video.
        """
        # TODO: This method will handle the video playback on a specific monitor.
        # It may involve setting the monitor as the target display for the video and handling video controls.
        pass

    def stop(self):
        """
        Stop the video sequence on all monitors.
        """
        for process in self._processes:
            process.terminate()  # Or a more graceful stop, if applicable.
            process.join()
        self._processes = []
