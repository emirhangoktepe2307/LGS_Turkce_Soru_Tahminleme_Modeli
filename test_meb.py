import requests
import json

url = "http://localhost:8000/api/meb-questions"
params = {"topic": "Söz Sanatları"}

try:
    print(f"Testing URL: {url} with topic: {params['topic']}")
    response = requests.get(url, params=params)
    response.raise_for_status()
    questions = response.json()
    
    print(f"Received {len(questions)} questions.")
    
    if len(questions) > 0:
        print("First Question Sample:")
        print(f"- {questions[0]['soru_metni']}")
    else:
        print("FAIL: No questions received.")

except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print(f"Response Body: {response.text}")
