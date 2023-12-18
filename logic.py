import cv2
import pygame
from screeninfo import get_monitors
from multiprocessing import Process, Value
import numpy as np


def init_pygame():
    """
    Initialize pygame for video display.
    """
    pygame.init()


def fade_in_effect(screen, final_frame, duration=2):
    """
    Apply fade-in effect to the screen.
    """
    fade_in_steps = 30
    for alpha in np.linspace(0, 255, fade_in_steps):
        fade_frame = cv2.addWeighted(final_frame, alpha / 255, np.zeros_like(final_frame), 1 - alpha / 255, 0)
        frame_surface = pygame.surfarray.make_surface(fade_frame)
        screen.blit(pygame.transform.rotate(pygame.transform.flip(frame_surface, True, False), 90), (0, 0))
        pygame.display.update()
        pygame.time.delay(int((duration / fade_in_steps) * 1000))  # Fade-in step duration


def play_video_on_monitor(video_path, monitor_number, should_run):
    """
    Plays a video on a specified monitor with a fade-in effect at the start.
    """
    monitors = get_monitors()
    if monitor_number >= len(monitors):
        print(f"Monitor {monitor_number} not found. Available monitors: {len(monitors)}")
        return

    monitor = monitors[monitor_number]
    screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor_number)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open video file {video_path}")
        return

    ret, first_frame = cap.read()
    if not ret:
        print(f"Failed to read the first frame from {video_path}")
        return

    # Convert first frame color and apply fade-in effect
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
    fade_in_effect(screen, first_frame)

    while should_run.value:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(pygame.transform.rotate(pygame.transform.flip(frame_surface, True, False), 90), (0, 0))
        pygame.display.update()

    cap.release()
    pygame.quit()


def start_video_sequence(videos, should_run):
    """
    Starts a new video sequence on multiple monitors.
    """
    processes = []

    for monitor_number, video_path in enumerate(videos):
        should_run.value = True
        p = Process(target=play_video_on_monitor, args=(video_path, monitor_number, should_run))
        p.start()
        processes.append(p)

    return processes


def stop_video_sequence(processes, should_run):
    """
    Stops the current video sequence.
    """
    should_run.value = False
    for p in processes:
        p.join()


def display_black_screen():
    """
    Displays a black screen on all monitors.
    """
    for monitor in get_monitors():
        pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor.number)
        pygame.display.get_surface().fill((0, 0, 0))
        pygame.display.update()
