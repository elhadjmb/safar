import cv2
import pygame
import sys
from screeninfo import get_monitors
from multiprocessing import Process

def play_video_on_monitor(video_path, monitor_number):
    pygame.init()


    monitors = get_monitors()
    if monitor_number >= len(monitors):
        raise ValueError(f"Monitor {monitor_number} not found. Available monitors: {len(monitors)}")

    monitor = monitors[monitor_number]
    screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor_number)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = pygame.surfarray.make_surface(frame)
        screen.blit(pygame.transform.rotate(pygame.transform.flip(frame, True, False), 90), (0, 0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

def start_video_playback(video_path, monitor_number):
    p = Process(target=play_video_on_monitor, args=(video_path, monitor_number))
    p.start()
    return p