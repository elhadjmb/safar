import cv2
import pygame
from screeninfo import get_monitors
from multiprocessing import Process, Value
import numpy as np


class Monitor:
    def __init__(self, monitor_number):
        self.monitor_number = monitor_number
        self.screen = None
        self.setup_monitor()

    def setup_monitor(self):
        monitors = get_monitors()
        if self.monitor_number >= len(monitors):
            raise ValueError(f"Monitor {self.monitor_number} not found. Available monitors: {len(monitors)}")

        monitor = monitors[self.monitor_number]
        self.screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN,
                                              display=self.monitor_number)

    def play_video(self, video_path, should_run):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise IOError(f"Cannot open video file {video_path}")

        ret, first_frame = cap.read()
        if not ret:
            raise IOError(f"Failed to read the first frame from {video_path}")

        first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
        self.fade_in_effect(first_frame)

        while should_run.value:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame)
            self.screen.blit(pygame.transform.rotate(pygame.transform.flip(frame_surface, True, False), 90), (0, 0))
            pygame.display.update()

        cap.release()

    def fade_in_effect(self, final_frame, duration=2):
        fade_in_steps = 30
        for alpha in np.linspace(0, 255, fade_in_steps):
            fade_frame = cv2.addWeighted(final_frame, alpha / 255, np.zeros_like(final_frame), 1 - alpha / 255, 0)
            frame_surface = pygame.surfarray.make_surface(fade_frame)
            self.screen.blit(pygame.transform.rotate(pygame.transform.flip(frame_surface, True, False), 90), (0, 0))
            pygame.display.update()
            pygame.time.delay(int((duration / fade_in_steps) * 1000))


class VideoSequence:
    def __init__(self, sequences):
        self.sequences = sequences
        self.should_run = Value('i', False)
        self.processes = []

    def start_sequence(self, sequence_key):
        if sequence_key not in self.sequences:
            raise ValueError(f"Sequence {sequence_key} not found.")

        videos = self.sequences[sequence_key]
        self.stop_sequence()  # Stop any currently running sequence
        self.should_run.value = True

        for monitor_number, video_path in enumerate(videos):
            p = Process(target=self.play_video_on_monitor, args=(video_path, monitor_number, self.should_run))
            p.start()
            self.processes.append(p)

    def stop_sequence(self):
        self.should_run.value = False
        for p in self.processes:
            p.join()
        self.processes = []

    @staticmethod
    def play_video_on_monitor(video_path, monitor_number, should_run):
        monitor = Monitor(monitor_number)
        monitor.play_video(video_path, should_run)


class Application:
    def __init__(self, sequences):
        self.video_sequence = VideoSequence(sequences)
        pygame.init()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode in self.video_sequence.sequences:
                        self.video_sequence.start_sequence(event.unicode)
                    elif event.unicode == '0':
                        self.video_sequence.stop_sequence()
                        self.display_black_screen()

    @staticmethod
    def display_black_screen():
        for monitor in get_monitors():
            pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN, display=monitor.number)
            pygame.display.get_surface().fill((0, 0, 0))
            pygame.display.update()
