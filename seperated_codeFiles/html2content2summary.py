from bs4 import BeautifulSoup
import google.generativeai as genai
# AIzaSyBAxvmdk40w79RyBKQCKRi7XvmqD2S5qpw
# AIzaSyA6YktiwkyhRTrNYvJ8Mms3xMbWtKfyrq4
# AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY
genai.configure(api_key='AIzaSyBsPtYQHgQLVf3Xw_USVU1CK4T5K9bgjQY')
model = genai.GenerativeModel("gemini-1.5-flash")

file_name = input('enter the file name: ')
with open(file_name, "r", encoding="utf-8") as file:
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
print(response.text)