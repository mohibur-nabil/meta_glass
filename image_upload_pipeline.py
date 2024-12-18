from email_script import EmailCodeExtractor
from scrap import login
import utils
import os
import time
from utils import face_detection
from face_book_download import *

# Start the timer
start_time = time.time()

def main():
    print("start.......")
    image_path = "./detected_faces/nm.jpg"
    try:
        if os.path.exists(image_path):
            
          
            print("Initializing EmailCodeExtractor.....")
            extractor = EmailCodeExtractor(
                email_address="pimeyestest2@gmail.com",
                password="yovm pnrs iesm xrid",
            )

            email = "pimeyestest2@gmail.com"
            password = "ft*RgNsgvN3T5>KdHU>u"
            
            
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
        else:
            print('image path is not valid')
        
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Script runtime: {runtime} seconds")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()

