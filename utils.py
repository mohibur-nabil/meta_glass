from reverse_image_search import GoogleReverseImageSearch
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# AIzaSyBAxvmdk40w79RyBKQCKRi7XvmqD2S5qpw
# AIzaSyA6YktiwkyhRTrNYvJ8Mms3xMbWtKfyrq4
# AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY


# def google_seach(url):
#     API_KEY = "AIzaSyBEP5xiyC30nceYKZqFkE1lHuobaQ01JE4"
#     SEARCH_ENGINE_ID = "a42052c32ac90420b"

#     # search_query = "https://business-cool.com/wp-content/uploads/2023/01/Elon_Musk_Royal_Society-e1681813122429.jpg"
#     url = "https://www.googleapis.com/customsearch/v1"
#     params = {"q": API_KEY,
#             "key": API_KEY, 
#             "cx": SEARCH_ENGINE_ID,
#             'seachType': 'image'
#             }
#     response = requests.get(url, params=params)
#     results = response.json()['items']

#     [print(f"{i+1}. {result['link']}") for i, result['link'] in enumerate(results)]
#     selected_link = int(input("enter the link number: "))
#     url = response_dict_list[selected_link - 1]["link"]
#     print(f"selected link: {url}")
#     return url




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
    prompt = '\n"Summarize the main person mentioned in the provided content in no more than 200 words. Focus on their professional journey, including notable workplaces and achievements, as well as their estimated net worth. If multiple individuals are referenced, prioritize the most prominent figure and disregard the others. Ensure the summary is comprehensive and highlights key aspects of their career, works and financial standing."'
    genai.configure(api_key="AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        text
        + prompt
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


def google_search(search_query):
    API_KEY = "AIzaSyBEP5xiyC30nceYKZqFkE1lHuobaQ01JE4"  # Replace with your API key
    SEARCH_ENGINE_ID = "a42052c32ac90420b"  # Replace with your search engine ID

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_query,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        # Uncomment this for image search
        # 'searchType': 'image'
    }

    try:
        response = requests.get(url, params=params)
        results = response.json()['items']

        if not results:
            print("No results found.")
            return None

        # Display search results
        for i, result in enumerate(results):
            print(f"{i+1}. {result['link']}")

        # User selects a link
        selected_link = int(input("Enter the link number: "))
        if 1 <= selected_link <= len(results):
            url = results[selected_link - 1]["link"]
            print(f"Selected link: {url}")
            return url
        else:
            print("Invalid selection. Please try again.")
            return None

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except KeyError:
        print("Unexpected response format from the API.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    return None

