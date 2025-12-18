from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_search():
    payload = {
        "query": "python tutorial",
        "max_results": 2
    }
    response = client.post("/api/v1/recommendations/search", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    try:
        test_search()
        print("Test passed!")
    except Exception as e:
        print(f"Test failed: {e}")
