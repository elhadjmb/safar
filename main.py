import logic

def main():
    sequences = {
        '1': ["path_to_video_sequence1_monitor1.mp4", "path_to_video_sequence1_monitor2.mp4"],  # Replace with your paths
        '2': ["path_to_video_sequence2_monitor1.mp4", "path_to_video_sequence2_monitor2.mp4"],  # Replace with your paths
        # Add more sequences as needed
    }

    should_run = Value('i', False)
    current_processes = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode in sequences:
                    # Stop current videos
                    should_run.value = False
                    for p in current_processes:
                        p.join()

                    # Start new sequence
                    current_processes = start_video_sequence(sequences[event.unicode], should_run)
                elif event.unicode == '0':
                    # Stop current videos and display black screen
                    should_run.value = False
                    for p in current_processes:
                        p.join()
                    current_processes = []
                    for monitor in get_monitors():
                        pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor.number)
                        pygame.display.get_surface().fill((0, 0, 0))
                        pygame.display.update()



if __name__ == "__main__":
    main()
