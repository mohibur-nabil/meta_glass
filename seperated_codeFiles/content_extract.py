import requests


url = 'http://ece.northsouth.edu/people/dr-nabeel-mohammed/'

try:

    response = requests.get(url)
   
    response.raise_for_status()

    
    html_content = response.text

   
    with open('selected.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("HTML content downloaded successfully.")

except requests.exceptions.RequestException as e:
   
    print(f"An error occurred: {e}")
