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

    def __init__(self, path, monitor, video_index=0):
        self.video_index = video_index
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
        self.play_soft()

    def play_soft(self):
        """Play the video with fade-in and fade-out effects."""
        # Ensure the screen's window is created before displaying the video
        self.monitor.create_window()

        self.is_playing = True
        self.is_paused = False

        if self.path:
            self.cap = cv2.VideoCapture(self.path)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            delay = int(1000 / fps) if fps > 0 else 25

            while self.is_playing:
                if not self.is_paused and self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if not ret:
                        break
                    # Resize and display the frame
                    frame_to_show = self.resize_frame(frame)
                    cv2.imshow(self.monitor.window_name, frame_to_show)

                if cv2.waitKey(delay) & 0xFF == ord('q') or not self.is_playing:  # TODO: experiment with delay 1
                    break

        # Display a black screen indefinitely after video ends
        self.display_black_screen()

    def fade_effect(self, start_alpha, end_alpha, duration, fps):
        """Apply fade effect to the video."""
        step = (end_alpha - start_alpha) / (duration * fps)
        alpha = start_alpha

        while alpha <= end_alpha and alpha >= start_alpha:
            fade_frame = np.zeros((self.monitor.height, self.monitor.width, 3), dtype=np.uint8)
            cv2.addWeighted(fade_frame, alpha, fade_frame, 1 - alpha, 0, fade_frame)
            cv2.imshow(self.monitor.window_name, fade_frame)  # Use monitor's window
            alpha += step
            cv2.waitKey(int(1000 / fps))

    def display_black_screen(self):
        """Display a black screen indefinitely."""
        while self.is_playing:
            black_screen = np.zeros((self.monitor.height, self.monitor.width, 3), dtype=np.uint8)
            cv2.imshow(self.monitor.window_name, black_screen)  # Use monitor's window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def pause(self):
        """Pause the video."""
        self.is_paused = True

    def stop(self):
        """Stop the video."""
        self.is_playing = False
        self.is_paused = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.monitor.close_window()

    def resize_frame(self, frame):
        """Resize the frame to fit the monitor's resolution while maintaining the aspect ratio."""
        height, width = frame.shape[:2]
        scale = min(self.monitor.width / width, self.monitor.height / height)
        new_size = (int(width * scale), int(height * scale))
        resized_frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
        # Create a black background
        background = np.zeros((self.monitor.height, self.monitor.width, 3), dtype=np.uint8)
        # Calculate center position
        x_center = (self.monitor.width - new_size[0]) // 2
        y_center = (self.monitor.height - new_size[1]) // 2
        # Place the resized frame onto the black background
        background[y_center:y_center + new_size[1], x_center:x_center + new_size[0]] = resized_frame
        return background
