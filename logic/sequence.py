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