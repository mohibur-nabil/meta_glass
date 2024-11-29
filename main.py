import utils

image_url = input("enter the image url: ")
url= utils.google_search(image_url)
html_name=utils.html_download(url)
text=utils.extract_text_from_html(html_name)
summary=utils.get_summary(text)
print('\n\n')
print('-'*100)
print('-'*100)
print(f"\n\nsummary: \n\n{summary}\n")
print('-'*100)
print('-'*100)
#code ends here
