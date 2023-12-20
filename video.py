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

    def _play_video(self):
        """
        Internal method to handle video playback.
        """
        while self.is_playing:
            ret, frame = self.cap.read()
            if not ret:
                break

            cv2.imshow("Video", frame)
            cv2.waitKey(1)

        cv2.destroyWindow("Video")

    def play(self):
        """
        Start or resume video playback.
        """
        with self.lock:
            if not self.is_playing:
                self.is_playing = True
                self.playback_thread = threading.Thread(target=self._play_video)
                self.playback_thread.start()

    def pause(self):
        """
        Pause video playback.
        """
        with self.lock:
            self.is_playing = False
            # The playback thread will automatically stop.

    def stop(self):
        """
        Stop video playback and release resources.
        """
        with self.lock:
            self.is_playing = False
            self.cap.release()
            cv2.destroyAllWindows()
