import os
import subprocess
import time
from datetime import datetime

def download_and_extract_frames(live_stream_url, output_dir="live_streams", frames_dir="frames", sleep_interval=10):
    """
    Downloads live streams and extracts frames from the videos.

    Args:
        live_stream_url (str): URL of the live stream.
        output_dir (str): Directory to save downloaded live streams.
        frames_dir (str): Directory to save extracted frames.
        sleep_interval (int): Time to wait between downloads (in seconds).
    """

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    def download_live_stream():
        """Downloads the live stream using yt-dlp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"live_stream_{timestamp}.mp4")
        
        command = [
            "yt-dlp", 
            "--live-from-start", 
            "--hls-use-mpegts", 
            live_stream_url, 
            "-o", output_file
        ]
        print(f"Downloading live stream to {output_file}...")
        subprocess.run(command, check=False)
        return output_file, timestamp

    def extract_frames(video_file, timestamp):
        """Extracts frames from the video using FFmpeg, saving to a unique folder."""
        frame_dir = os.path.join(frames_dir, f"frames_{timestamp}")
        os.makedirs(frame_dir, exist_ok=True)
        
        print(f"Extracting frames from {video_file} to {frame_dir}...")
        command = [
            "ffmpeg", 
            "-i", video_file, 
            "-vf", "fps=1", 
            os.path.join(frame_dir, "frame_%04d.jpg")
        ]
        subprocess.run(command, check=False)

    try:
        while True:
            video_file, timestamp = download_live_stream()
            if os.path.exists(video_file):
                extract_frames(video_file, timestamp)
            print(f"Sleeping for {sleep_interval} seconds...")
            time.sleep(sleep_interval)
    except KeyboardInterrupt:
        print("Process stopped by user.")
    except Exception as e:
        print(f"Error occurred: {e}")
