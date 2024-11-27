import os
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image


def process_images_in_folder(folder_path):

    model_path = hf_hub_download(
        repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt"
    )
    model = YOLO(model_path)

    detected_faces_dir = "detected_faces"
    os.makedirs(detected_faces_dir, exist_ok=True)

    padding = 80
    face_count = 0

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".jpg", ".jpeg", ".png")):
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

                        cropped_face = image.crop(
                            (x_min_padded, y_min_padded, x_max_padded, y_max_padded)
                        )

                        face_path = os.path.join(
                            detected_faces_dir, f"detected_face_{face_count}.jpg"
                        )
                        cropped_face.save(face_path)
                        face_count += 1

                    print(f"Processed {image_path} and saved detected faces.")
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
