import requests

# Define the two code snippets you want to compare
data = {
    "code1": "def add(a, b):\n    return a + b",
    "code2": "def add(x, y):\n    return x + y"
}

# Send the request to your Flask API
response = requests.post("http://127.0.0.1:5000/compare", json=data)

# Print the response from the API
print("API Response:", response.json())
