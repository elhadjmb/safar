from multiprocessing import Process

import cv2

from .monitor import Monitor
import cv2
import numpy as np


class BlackScreen:
    """
    Simulates a video displaying a black screen.

    Attributes:
        duration (int): Duration for the black screen in seconds.
        frame_rate (int): Frame rate of the simulated video.
    """

    def __init__(self, duration=10, frame_rate=30):
        """
        Initialize a BlackScreen instance.

        Args:
            duration (int): Duration for the black screen in seconds. Defaults to 10.
            frame_rate (int): Frame rate of the simulated video. Defaults to 30.
        """
        self.duration = duration
        self.frame_rate = frame_rate

    def play(self, window_name, monitor):
        """
        Play the black screen on the specified monitor.

        Args:
            window_name (str): The name of the window for display.
            monitor (Monitor): The monitor on which to display the black screen.
        """
        # Create a black frame
        black_frame = np.zeros((monitor.height, monitor.width, 3), dtype=np.uint8)

        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, monitor.x, monitor.y)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        num_frames = self.duration * self.frame_rate
        for _ in range(num_frames):
            cv2.imshow(window_name, black_frame)
            if cv2.waitKey(int(1000 / self.frame_rate)) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


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

        if not videos:
            # If no videos are specified, map black screens to all monitors.
            self._map_black_screens_to_monitors()

        # Ensure videos and monitors are mapped correctly.
        if len(self.videos) != len(self.monitors):
            raise ValueError("The number of videos must match the number of monitors.")

    def _map_black_screens_to_monitors(self):
        """
        Maps black screens to all detected monitors.
        """
        # Assuming BlackScreen is a Video-like class displaying a black screen.
        self.videos = [BlackScreen() for _ in self.monitors]

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
        cap = cv2.VideoCapture(video.path)
        if not cap.isOpened():
            print(f"Error opening video file: {video.path}")
            return

        # Move the window to the monitor.
        window_name = f"Video on Monitor {monitor.number}"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, monitor.x, monitor.y)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(window_name, frame)

            # Check for 'q' key to stop playback
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        """
        Stop the video sequence on all monitors.
        """
        for process in self._processes:
            process.terminate()  # Or a more graceful stop, if applicable.
            process.join()
        self._processes = []
