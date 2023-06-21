import requests

# Define the URL of the Flask endpoint
url = 'http://localhost:5000/generate_video'

# Define the JSON payload
payload = {
    "qa_array": [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "What is the capital of Japan?", "answer": "Tokyo"}
    ],
    "language": "en"
}

# Send the POST request
response = requests.post(url, json=payload)

# Check if the response is successful
if response.status_code == 200:
    # Save the response content as a file
    with open('qa_video.mp4', 'wb') as f:
        f.write(response.content)
    print("Video file saved as qa_video.mp4")
else:
    print("Error: {response.status_code} - {response.text}")
