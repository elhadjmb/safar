from logic import *


def main():
    """
    Main function to control video playback based on user input.
    """
    sequences = {
        '1': ["path_to_video_sequence1_monitor1.mp4", "path_to_video_sequence1_monitor2.mp4"],
        '2': ["path_to_video_sequence2_monitor1.mp4", "path_to_video_sequence2_monitor2.mp4"],
        # Add more sequences as needed
    }
    app = Application(sequences)
    app.run()


if __name__ == "__main__":
    main()
