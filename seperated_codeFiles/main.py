from reverse_image_search import GoogleReverseImageSearch
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
# AIzaSyBAxvmdk40w79RyBKQCKRi7XvmqD2S5qpw
# AIzaSyA6YktiwkyhRTrNYvJ8Mms3xMbWtKfyrq4
# AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY
genai.configure(api_key='AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY')
model = genai.GenerativeModel("gemini-1.5-flash")


#code for google reverse serach start here
request = GoogleReverseImageSearch()
image_url = input("enter the image url: ")
response = request.response(
    query="Example Query",
    image_url=image_url,
    max_results=5
)

response=str(response)
response_list=response.split('---\n')
response_list = response_list[1::2]
response_dict_list = [{'title':result.split('\n')[0].split('Title:')[1].strip(), 'link':result.split('\n')[1].split('Link:')[1].strip()} for result in response_list]
[print(f"{i+1}. {result}") for i, result in enumerate(response_dict_list)]

selected_link=  int(input("enter the link number: "))
url = response_dict_list[selected_link-1]['link']
print(f"selected link: {url}")
# code for google reverse serach end here

# code to download the html file
html_name = 'selected.html'
try:
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    with open(html_name, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print("HTML content downloaded successfully.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
# code to download the html file end here

with open(html_name, "r", encoding="utf-8") as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, "html.parser")


text_content = soup.get_text()


lines = text_content.splitlines()

text=''
for line in lines:
    cleaned_line = line.strip() 
    if cleaned_line:  
        text+=' '+cleaned_line          
response = model.generate_content(text+" \n write a summary for the above content about the person with in 200words max")
print('summary:')
print(response.text)
