import cv2
import threading

class Video:
    """
    Represents a video file.

    Attributes:
        path (str): Path to the video file.
        cap (cv2.VideoCapture): OpenCV VideoCapture object.
        is_playing (bool): Flag to indicate if the video is currently playing.
        lock (threading.Lock): Lock for thread-safe operations.

    Methods:
        play(): Start or resume video playback.
        pause(): Pause video playback.
        stop(): Stop video playback and release resources.
    """

    def __init__(self, path):
        """
        Initialize a Video instance.

        Args:
            path (str): Path to the video file.
        """
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.is_playing = False
        self.lock = threading.Lock()


