import requests
import json

# The URL where our API is running
url = 'http://127.0.0.1:5000/predict'

# Sample data to send for prediction.
# Let's predict for a Tuesday (day_of_week=1) in October.
test_data = {
    'day_of_week': 1,
    'month': 10,
    'day': 14,
    'year': 2025
}

# Send the POST request with the data as JSON
print("Sending request to the API...")
response = requests.post(url, json=test_data)

# Print the prediction we received from the server
print("\n--- API Response ---")
print(f"Status Code: {response.status_code}") # Should be 200 for success
print(f"Prediction: {response.json()}")