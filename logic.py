from multiprocessing import Process

import cv2
import pygame
from screeninfo import get_monitors


def play_video_on_monitor(video_path, monitor_number, should_run):
    pygame.init()

    monitors = get_monitors()
    if monitor_number >= len(monitors):
        raise ValueError(f"Monitor {monitor_number} not found. Available monitors: {len(monitors)}")

    monitor = monitors[monitor_number]
    screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor_number)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")

    while should_run.value:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = pygame.surfarray.make_surface(frame)
        screen.blit(pygame.transform.rotate(pygame.transform.flip(frame, True, False), 90), (0, 0))

        pygame.display.update()

    cap.release()
    pygame.quit()


def start_video_sequence(videos, should_run):
    processes = []

    for monitor_number, video_path in enumerate(videos):
        should_run.value = True
        p = Process(target=play_video_on_monitor, args=(video_path, monitor_number, should_run))
        p.start()
        processes.append(p)

    return processes
