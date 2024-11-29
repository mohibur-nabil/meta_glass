import os
import subprocess
import time
from datetime import datetime
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image

def download_extract_faceDetect(live_stream_url, output_dir="live_streams", frames_dir="frames", sleep_interval=10):
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
            "-f", "bv",  # Specifies best video-only format
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

    
    def face_detection(timestamp):

        model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
        model = YOLO(model_path)

        
        detected_faces_dir = 'detected_faces'
        os.makedirs(detected_faces_dir, exist_ok=True)

    
        padding = 40
        face_count = 0

        
        for subdir, _, files in os.walk(os.path.join(frames_dir, f"frames_{timestamp}")):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(subdir, file)
                    try:
                        image = Image.open(image_path)
                        output = model(image)
                        results = Detections.from_ultralytics(output[0])

                        for bbox in results.xyxy:
                            x_min, y_min, x_max, y_max = bbox
                            
                            x_min_padded = max(0, x_min - padding)
                            y_min_padded = max(0, y_min - padding + 20)
                            x_max_padded = min(image.width, x_max + padding)
                            y_max_padded = min(image.height, y_max + padding + 20)

                            cropped_face = image.crop((x_min_padded, y_min_padded, x_max_padded, y_max_padded))
                            
                            face_path = os.path.join(detected_faces_dir, f"detected_face_{timestamp}_{face_count}.jpg")
                            cropped_face.save(face_path)
                            face_count += 1

                        print(f"Processed {image_path} and saved detected faces.")
                    except Exception as e:
                        print(f"Error processing {image_path}: {e}")



    try:
        while True:
            video_file, timestamp = download_live_stream()
            if os.path.exists(video_file):
                extract_frames(video_file, timestamp)
                face_detection(timestamp=timestamp)
            print(f"Sleeping for {sleep_interval} seconds...")
            time.sleep(sleep_interval)
    except KeyboardInterrupt:
        print("Process stopped by user.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__": 
   live_url = str(input("enter the facebook live url: "))
   download_extract_faceDetect(live_url)