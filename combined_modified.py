from email_script import EmailCodeExtractor
from scrap import login
from google_search_for_conbinedSystem import *
import utils
import os
import subprocess
import time
from datetime import datetime
from utils import face_detection

# Define constants
from face_book_download import *

LIVE_STREAM_URL = "https://fb.watch/wqtvDznziC/"


def main():
    print("start.......")
    try:
        while True:
            video_file, timestamp = download_live_stream(LIVE_STREAM_URL)
            if os.path.exists(video_file):
                fram_dir = extract_frames(video_file, timestamp)
                face_count = face_detection(fram_dir)
                if not face_count > 0:
                    continue
                # Initialize the extractor
                print("got faces")
                print("Initializing EmailCodeExtractor.....")
                extractor = EmailCodeExtractor(
                    email_address="pimeyestest2@gmail.com",
                    password="yovm pnrs iesm xrid",
                )

                email = "pimeyestest2@gmail.com"
                password = "ft*RgNsgvN3T5>KdHU>u"
                image_path = "/home/nabil/Desktop/meta_glass/detected_faces/nm.jpg"

                login("https://pimeyes.com/en", email, password, extractor, image_path)

                # read_urls
                urls_list = []
                pimeyes_urls_file = "/home/nabil/Desktop/meta_glass/extracted_urls.txt"
                with open(pimeyes_urls_file, "r") as urls:
                    for url in urls:
                        urls_list.append(url)
                # read urls ends here and saved in the urls_list list.

                # for now lets take the 2nd result. As I know it works.
                image_url = urls_list[0]
                print(image_url)
                # seach in the google seach module for base link of the image
                page_url = utils.google_search(image_url)
                html_name = utils.html_download(page_url)
                text = utils.extract_text_from_html(html_name)
                summary = utils.get_summary(text)
                print(summary)

            print(f"Sleeping for {SLEEP_INTERVAL} seconds...")
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("Process stopped by user.")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()


# # Initialize the extractor
# print("Initializing EmailCodeExtractor.....")
# extractor = EmailCodeExtractor(
#     email_address="pimeyestest2@gmail.com", password="yovm pnrs iesm xrid"
# )

# email = "pimeyestest2@gmail.com"
# password = "ft*RgNsgvN3T5>KdHU>u"
# image_path = "/home/nabil/Desktop/meta_glass/images/nm.jpg"

# login("https://pimeyes.com/en", email, password, extractor, image_path)


# # read_urls
# urls_list = []
# pimeyes_urls_file = "/home/nabil/Desktop/meta_glass/extracted_urls.txt"
# with open(pimeyes_urls_file, "r") as urls:
#     for url in urls:
#         urls_list.append(url)
# # read urls ends here and saved in the urls_list list.

# # for now lets take the 2nd result. As I know it works.
# image_url = urls_list[0]
# print(image_url)
# # seach in the google seach module for base link of the image
# page_url = utils.google_search(image_url)
# html_name=utils.html_download(page_url)
# text=utils.extract_text_from_html(html_name)
# summary=utils.get_summary(text)
# print(summary)
