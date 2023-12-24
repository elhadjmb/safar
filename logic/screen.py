import cv2
import numpy as np
from screeninfo import get_monitors


class Screen:
    """
    Represents a computer monitor, providing necessary details for video playback.

    Attributes:
        select_index (int): The index of the monitor in the system's monitor list.
        width (int): Width of the monitor in pixels.
        height (int): Height of the monitor in pixels.
        x (int): The X-coordinate of the top-left corner of the monitor.
        y (int): The Y-coordinate of the top-left corner of the monitor.
        location (str): The location of the monitor in the room (Circle, BigMountain, Mountains).
    """

    def __repr__(self):
        return f"Screen {self.select_index}: {self.name}"

    def __init__(self, select_index=0, location=None):
        monitors = get_monitors()
        if select_index >= len(monitors):
            raise ValueError("Selected monitor index is out of range.")

        selected_monitor = monitors[select_index]
        self.select_index = select_index
        self.width = selected_monitor.width
        self.height = selected_monitor.height
        self.x = selected_monitor.x
        self.y = selected_monitor.y
        self.location = location
        self.name = selected_monitor.name + f" ({self.location})"

        # Create a unique window for each monitor
        self.window_name = f"Screen_{self.select_index}"
        self.window_created = False

    def create_window(self):
        """Create the OpenCV window if it hasn't been created already."""
        if not self.window_created:
            cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(self.window_name, self.x, self.y)
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self.window_created = True

    def close_window(self):
        """Close the OpenCV window."""
        if self.window_created:
            cv2.destroyWindow(self.window_name)
            self.window_created = False

    def blink(self, color=(0, 0, 255), duration=0.5):
        """
        Blink the screen with a specified color (BGR format) and duration.
        Default color is red: (0, 0, 255).
        """
        self.create_window()

        # Create an image filled with the specified color
        colored_img = np.full((self.height, self.width, 3), color, dtype=np.uint8)

        # Show the colored image
        cv2.imshow(self.window_name, colored_img)
        cv2.waitKey(int(duration * 1000))

        self.close_window()

    @staticmethod
    def detect_monitors():
        """Return a list of all detected screens."""
        monitors = get_monitors()
        return [Screen(select_index=monitors.index(m)) for m in monitors]
