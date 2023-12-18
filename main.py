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

    should_run = Value('i', False)
    current_processes = []
    init_pygame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode in sequences:
                    stop_video_sequence(current_processes, should_run)
                    current_processes = start_video_sequence(sequences[event.unicode], should_run)
                elif event.unicode == '0':
                    stop_video_sequence(current_processes, should_run)
                    current_processes = []
                    display_black_screen()


if __name__ == "__main__":
    main()
