import requests

API_KEY = "AIzaSyBEP5xiyC30nceYKZqFkE1lHuobaQ01JE4"
SEARCH_ENGINE_ID = "a42052c32ac90420b"

search_query = "https://business-cool.com/wp-content/uploads/2023/01/Elon_Musk_Royal_Society-e1681813122429.jpg"
url = "https://www.googleapis.com/customsearch/v1"
params = {"q": search_query,
           "key": API_KEY, 
           "cx": SEARCH_ENGINE_ID,
           'seachType': 'image'
           }
response = requests.get(url, params=params)
results = response.json()['items']

for items in results:
    print(items["link"])
