import requests

url = "https://test-flask-backend-a3hag0fcb7bxdtgq.northeurope-01.azurewebsites.net/classify"
image_path = "dog.jpg"

with open(image_path, "rb") as img:
    files = {"image": img}
    response = requests.post(url, files=files)

print(response.json())
