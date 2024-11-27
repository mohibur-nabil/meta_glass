from reverse_image_search import GoogleReverseImageSearch
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# AIzaSyBAxvmdk40w79RyBKQCKRi7XvmqD2S5qpw
# AIzaSyA6YktiwkyhRTrNYvJ8Mms3xMbWtKfyrq4
# AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY


def get_google_rev_search_results(image_url):
    # code for google reverse serach start here
    request = GoogleReverseImageSearch()
    response = request.response(
        query="Example Query", image_url=image_url, max_results=5
    )

    response = str(response)
    response_list = response.split("---\n")
    response_list = response_list[1::2]
    response_dict_list = [
        {
            "title": result.split("\n")[0].split("Title:")[1].strip(),
            "link": result.split("\n")[1].split("Link:")[1].strip(),
        }
        for result in response_list
    ]
    [print(f"{i+1}. {result}") for i, result in enumerate(response_dict_list)]
    selected_link = int(input("enter the link number: "))
    url = response_dict_list[selected_link - 1]["link"]
    print(f"selected link: {url}")
    return url


def html_download(url):
    html_name = "selected.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        with open(html_name, "w", encoding="utf-8") as file:
            file.write(html_content)
        print("HTML content downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return html_name


def extract_text_from_html(html_name):
    with open(html_name, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text()
    lines = text_content.splitlines()

    text = ""
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line:
            text += " " + cleaned_line
    return text


def get_summary(text):
    genai.configure(api_key="AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        text
        + " \n write a summary for the above content about the person with in 200words max"
    )
    return response.text


import os
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image

def face_detection(folder_path):

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
