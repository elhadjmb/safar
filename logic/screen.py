import cv2
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
    """

    def __repr__(self):
        return f"Screen {self.select_index} ({self.width}x{self.height})"

    def __init__(self, select_index=0):
        monitors = get_monitors()
        if select_index >= len(monitors):
            raise ValueError("Selected monitor index is out of range.")

        selected_monitor = monitors[select_index]
        self.select_index = select_index
        self.width = selected_monitor.width
        self.height = selected_monitor.height
        self.x = selected_monitor.x
        self.y = selected_monitor.y
        self.name = selected_monitor.name

        # Create a unique window for each monitor
        self.window_name = f"Screen_{self.select_index}"
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(self.window_name, self.x, self.y)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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

    @staticmethod
    def detect_monitors():
        """Return a list of all detected screens."""
        monitors = get_monitors()
        return [Screen(select_index=monitors.index(m)) for m in monitors]
