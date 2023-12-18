from gui import VideoSequenceConfigurator
import tkinter as tk
from logic import Application


def main(gui=True):
    """
    Main function to control video playback based on user input.
    """
    if gui:
        root = tk.Tk()
        app = VideoSequenceConfigurator(root)
        app.load_configuration()
        root.mainloop()

        # After closing the GUI, run the application with the saved configuration
        if app.config:  # Check if configuration exists
            application = Application(app.config)
            application.run()

        return
    sequences = {
        '1': ["path_to_video_sequence1_monitor1.mp4", "path_to_video_sequence1_monitor2.mp4"],
        '2': ["path_to_video_sequence2_monitor1.mp4", "path_to_video_sequence2_monitor2.mp4"],
        # Add more sequences as needed
    }
    app = Application(sequences)
    app.run()


if __name__ == "__main__":
    main()
