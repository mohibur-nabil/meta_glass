from email_script import EmailCodeExtractor
from scrap import login
import utils
import os
import time
from face_book_download import *

# Start the timer
start_time = time.time()


def main():
    print("start.......")
    LIVE_STREAM_URL = input('enter the fb live link: ')
    try:
        while True:
            video_file, timestamp = download_live_stream(LIVE_STREAM_URL)
            
            if os.path.exists(video_file):
                fram_dir = extract_frames(video_file, timestamp)
                face_count = utils.face_detection(fram_dir)
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
                image_path = "/detected_faces/detected_face_0.jpg"
               
                login("https://pimeyes.com/en", email, password, extractor, image_path)

                # read_urls
                urls_list = []
                pimeyes_urls_file = "extracted_urls.txt"
                with open(pimeyes_urls_file, "r") as urls:
                    for url in urls:
                        urls_list.append(url)
            
                image_url = urls_list[0]
                print(image_url)
                page_url = utils.google_search(image_url)
                html_name = utils.html_download(page_url)
                text = utils.extract_text_from_html(html_name)
                summary = utils.get_summary(text)
                print(summary)
            
            end_time = time.time()
            runtime = end_time - start_time
            print(f"Script runtime: {runtime} seconds")
            print(f"Sleeping for {SLEEP_INTERVAL} seconds...")
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("Process stopped by user.")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()

