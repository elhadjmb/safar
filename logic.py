import pygame
import sys
from screeninfo import get_monitors

def play_video(video_path, monitor_number):
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()

    # Get screen information
    monitors = get_monitors()
    if monitor_number >= len(monitors):
        raise ValueError(f"Monitor {monitor_number} not found. Available monitors: {len(monitors)}")

    monitor = monitors[monitor_number]

    # Set up the screen for the selected monitor
    screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN)

    # Load the video
    video = pygame.movie.Movie(video_path)

    # Set the video screen and start
    video.set_display(screen)
    video.play()

    # Keep running until the video is finished or user quits
    while video.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.stop()
                pygame.quit()
                sys.exit()

