import requests
import json

url = "http://localhost:8000/api/sorular/olustur"
payload = {
    "konu": "Açıklama",
    "yil": 2023,
    "soru_tipi": "cumlede"
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    questions = response.json()
    
    print(f"Received {len(questions)} questions.")
    
    is_mock = False
    for q in questions:
        print(f"- {q['soru_metni'][:50]}...")
        if "sistem çalışıyor" in q['soru_metni']:
            is_mock = True
    
    if is_mock:
        print("FAIL: Received MOCK data (API failed).")
    else:
        print("SUCCESS: Received GENERATED data.")

except Exception as e:
    print(f"Error: {e}")
