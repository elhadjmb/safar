import random

import cv2
import numpy as np


class Video:
    """
    Represents a video, capable of playing, pausing, and stopping the video on a specified monitor.

    Attributes:
        path (str): Path to the video file.
    """

    def __repr__(self):
        return f"Video {self.video_index} ({self.path})"

    def __init__(self, path, monitor):
        self.video_index = random.randint(0, 1_000_000)
        self.is_paused = None
        self.path = path
        self.monitor = monitor
        self.cap = None
        self.is_playing = False

    def play(self, hard=True):
        """
        Play the video either hard or soft.
        Hard play is when the video is played without the ability to pause.
        Soft play is when the video is played with the ability to pause.
        """
        if hard:
            self.play_hard()
        else:
            self.play_soft()

    def play_hard(self):
        """Play the video or display a black screen on the specified monitor."""
        # Setup the window for fullscreen display on the specified monitor
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Video", self.monitor.x, self.monitor.y)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.is_playing = True
        if self.path:
            self.cap = cv2.VideoCapture(self.path)

            while self.is_playing:
                ret, frame = self.cap.read()
                if not ret:
                    break
                cv2.imshow("Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            # Display a black screen if path is None
            while self.is_playing:
                black_screen = np.zeros((self.monitor.height, self.monitor.width, 3), dtype=np.uint8)
                cv2.imshow("Video", black_screen)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def play_soft(self):
        """Play the video or display a black screen on the specified monitor."""
        # Setup the window for fullscreen display on the specified monitor
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Video", self.monitor.x, self.monitor.y)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.is_playing = True
        self.is_paused = False
        if self.path:
            self.cap = cv2.VideoCapture(self.path)

            while self.is_playing:
                if not self.is_paused:
                    ret, frame = self.cap.read()
                    if not ret:
                        break
                    cv2.imshow("Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            # Display a black screen if path is None
            while self.is_playing:
                if not self.is_paused:
                    black_screen = np.zeros((self.monitor.height, self.monitor.width, 3), dtype=np.uint8)
                    cv2.imshow("Video", black_screen)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def pause(self):
        """Pause the video."""
        self.is_paused = True

    def stop(self):
        """Stop the video."""
        self.is_playing = False
        self.is_paused = False
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
