import requests

response = requests.get("https://gutendex.com/books/11")
data = response.json()

print(data)