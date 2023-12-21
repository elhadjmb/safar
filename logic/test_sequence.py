import unittest
from unittest.mock import patch, MagicMock
from sequence import Sequence

class TestSequence(unittest.TestCase):

    def setUp(self):
        # Mock Video and Screen objects
        self.mock_video1 = MagicMock()
        self.mock_video2 = MagicMock()
        self.mock_screen1 = MagicMock()
        self.mock_screen2 = MagicMock()

        # Set up a list of video-monitor pairs
        self.video_monitor_pairs = [(self.mock_video1, self.mock_screen1), (self.mock_video2, self.mock_screen2)]

    @patch('sequence.Screen.detect_monitors')
    def test_sequence_initialization_with_no_videos(self, mock_detect_monitors):
        # Setup the mock
        mock_detect_monitors.return_value = [self.mock_screen1, self.mock_screen2]

        # Test initialization with no videos
        sequence = Sequence([])
        self.assertEqual(len(sequence.videos), 2)  # Expecting 2 black screens

    def test_sequence_initialization_with_videos(self):
        # Test initialization with videos
        sequence = Sequence(self.video_monitor_pairs)
        self.assertEqual(len(sequence.videos), 2)

    @patch('sequence.threading.Thread.start')
    def test_start(self, mock_thread_start):
        # Test start method
        sequence = Sequence(self.video_monitor_pairs)
        sequence.start()
        self.assertEqual(len(sequence.threads), 2)

    def test_stop(self):
        # Test stop method
        sequence = Sequence(self.video_monitor_pairs)
        sequence.start()
        sequence.stop()
        self.assertEqual(len(sequence.threads), 0)

    def test_freeze(self):
        # Test freeze method
        sequence = Sequence(self.video_monitor_pairs)
        sequence.freeze()
        self.mock_video1.pause.assert_called_once()
        self.mock_video2.pause.assert_called_once()

if __name__ == '__main__':
    unittest.main()
