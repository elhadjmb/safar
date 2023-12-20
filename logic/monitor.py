import screeninfo

class Monitor:
    """
    Represents a monitor display.

    Attributes:
        number (int): The monitor number.
        info (screeninfo.Monitor): Detailed information about the monitor.
    """

    def __init__(self, number):
        """
        Initialize a Monitor instance.

        Args:
            number (int): The monitor number.

        Raises:
            ValueError: If the specified monitor number does not exist.
        """
        self.number = number
        self.info = self._get_monitor_info()

        if not self.info:
            raise ValueError(f"Monitor number {number} does not exist.")

    @staticmethod
    def _get_monitors():
        """
        Get available monitors.

        Returns:
            List[screeninfo.Monitor]: A list of available monitors.
        """
        return screeninfo.get_monitors()

    def _get_monitor_info(self):
        """
        Retrieve information for the specified monitor.

        Returns:
            screeninfo.Monitor: Information about the specified monitor, or None if not found.
        """
        monitors = Monitor._get_monitors()
        for monitor in monitors:
            if monitor.number == self.number:
                return monitor
        return None
