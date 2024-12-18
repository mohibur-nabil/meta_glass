import os
import subprocess
import time
from datetime import datetime
from utils import  face_detection
# Define constants
LIVE_STREAM_URL = "https://www.youtube.com/watch?v=61hkf-t-vOU"
OUTPUT_DIR = "live_streams"
FRAMES_DIR = "frames"
SLEEP_INTERVAL = 10  

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

def download_live_stream(LIVE_STREAM_URL):
    """Downloads the live stream using yt-dlp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"live_stream_{timestamp}.mp4")
    
    command = [
        "yt-dlp", 
        "--live-from-start", 
        "--hls-use-mpegts", 
        LIVE_STREAM_URL, 
        "-o", output_file
    ]
    print(f"Downloading live stream to {output_file}...")
    subprocess.run(command, check=False)
    return output_file, timestamp

def extract_frames(video_file, timestamp):
    """Extracts frames from the video using FFmpeg, saving to a unique folder."""
    frame_dir = os.path.join(FRAMES_DIR, f"frames_{timestamp}")
    os.makedirs(frame_dir, exist_ok=True)
    
    print(f"Extracting frames from {video_file} to {frame_dir}...")
    command = [
        "ffmpeg", 
        "-i", video_file, 
        "-vf", "fps=1", 
        os.path.join(frame_dir, "frame_%04d.jpg")
    ]
    subprocess.run(command, check=False)
    return frame_dir


