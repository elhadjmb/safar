from logic import start_video_playback

if __name__ == "__main__":
    videos = ["video1.mp4", "video2.mp4"]
    processes = []

    for i, video in enumerate(videos):
        process = start_video_playback(video, i)
        processes.append(process)

    for process in processes:
        process.join()

