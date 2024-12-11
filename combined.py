from email_script import EmailCodeExtractor
from scrap import login
from google_search_for_conbinedSystem import *
# Initialize the extractor
print("Initializing EmailCodeExtractor.....")
extractor = EmailCodeExtractor(
    email_address='pimeyestest2@gmail.com',
    password="yovm pnrs iesm xrid"
)

email = 'pimeyestest2@gmail.com'
password = 'ft*RgNsgvN3T5>KdHU>u'
image_path = "/home/nabil/meta_glass/images/shafinsir.jpg" 

login('https://pimeyes.com/en', email, password, extractor, image_path)


#read_urls
urls_list=[]
pimeyes_urls_file = '/home/nabil/meta_glass/extracted_urls.txt'
with open(pimeyes_urls_file,'r') as urls:
    for url in urls:
         urls_list.append(url)
#read urls ends here and saved in the urls_list list.

#for now lets take the 2nd result. As I know it works. 
image_url = urls_list[1]
print(image_url)
# seach in the google seach module for base link of the image
page_url = get_google_rev_search_results(image_url)




