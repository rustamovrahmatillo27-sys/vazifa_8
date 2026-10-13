import requests
import json
 
resources = ["posts", "comments", "albums", "photos", "todos", "users"]
 

data = {}
 
for name in resources:
    url = f"https://jsonplaceholder.typicode.com/{name}"
    response = requests.get(url)
 
    if response.status_code == 200:
        data[name] = response.json()
        print(f"{name}: {len(data[name])} ta ma'lumot olindi")
    else:
        print(f"{name}: xato, status kodi {response.status_code}")
 
    
with open("data.json", "w", encoding="utf- 8") as file:
    json.dump(data, file, indent = 4)
 
