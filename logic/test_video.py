import unittest
from unittest.mock import patch, MagicMock
from video import Video
from screen import Screen  # Assuming Screen is the class used for monitor

class TestVideo(unittest.TestCase):

    def setUp(self):
        # Mock a Screen object
        self.mock_screen = Screen(select_index=0)

        # Path for a dummy video file
        self.dummy_video_path = "D:\TRL\Crows.mp4"

        # Create a Video instance
        self.video = Video(self.dummy_video_path, self.mock_screen)

    @patch('video.cv2.VideoCapture')
    @patch('video.cv2.imshow')
    @patch('video.cv2.waitKey')
    def test_play_hard(self, mock_waitKey, mock_imshow, mock_VideoCapture):
        mock_VideoCapture.return_value.read.return_value = (True, MagicMock())
        mock_waitKey.return_value = 0

        self.video.play(hard=True)
        self.assertTrue(self.video.is_playing)
        self.assertFalse(self.video.is_paused)

    @patch('video.cv2.VideoCapture')
    @patch('video.cv2.imshow')
    @patch('video.cv2.waitKey')
    def test_play_soft(self, mock_waitKey, mock_imshow, mock_VideoCapture):
        mock_VideoCapture.return_value.read.return_value = (True, MagicMock())
        mock_waitKey.return_value = 0

        self.video.play(hard=False)
        self.assertTrue(self.video.is_playing)
        self.assertFalse(self.video.is_paused)

    def test_pause(self):
        self.video.pause()
        self.assertTrue(self.video.is_paused)

    def test_stop(self):
        self.video.stop()
        self.assertFalse(self.video.is_playing)
        self.assertFalse(self.video.is_paused)

if __name__ == '__main__':
    unittest.main()
