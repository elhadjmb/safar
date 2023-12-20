import cv2


class Video:
    """
    Represents a video, capable of playing, pausing, and stopping the video on a specified monitor.

    Attributes:
        path (str): Path to the video file.
    """

    def __init__(self, path):
        self.path = path
        self.cap = None
        self.is_playing = False

    def play(self, monitor):
        """Play the video on a specified monitor."""
        self.cap = cv2.VideoCapture(self.path)

        # Set the window to the size of the monitor
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Video", monitor.x, monitor.y)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.is_playing = True
        while self.is_playing:
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def pause(self):
        """Pause the video."""
        self.is_playing = False
        self.cap.release()

    def stop(self):
        """Stop the video."""
        self.is_playing = False
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
