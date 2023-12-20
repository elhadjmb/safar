from screeninfo import get_monitors


class Monitor:
    """
    Represents a computer monitor, providing necessary details for video playback.

    Attributes:
        index (int): The index of the monitor in the system's monitor list.
        width (int): Width of the monitor in pixels.
        height (int): Height of the monitor in pixels.
        x (int): The X-coordinate of the top-left corner of the monitor.
        y (int): The Y-coordinate of the top-left corner of the monitor.
    """

    def __init__(self, select_index=0):
        monitors = get_monitors()
        if select_index >= len(monitors):
            raise ValueError("Selected monitor index is out of range.")

        selected_monitor = monitors[select_index]
        self.index = select_index
        self.width = selected_monitor.width
        self.height = selected_monitor.height
        self.x = selected_monitor.x
        self.y = selected_monitor.y
        self.name = selected_monitor.name

    @staticmethod
    def detect_monitors():
        """Return a list of all detected monitors."""
        return get_monitors()
