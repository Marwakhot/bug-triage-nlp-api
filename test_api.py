import requests
import json

# Configuration
API_URL = "http://127.0.0.1:8080/predict"

# Sample Data
# A dictionary with sample bug report data.
bug_report_data = {
    "sd": "Code completion fails and throws a null pointer exception after the latest update.",
    "pd": "JDT",
    "os": "Windows",
    "bs": "critical"
}

# Send Request and Print Response
try:
    print("Sending data to the API...")
    
    # Send the data as a POST request with a JSON payload
    response = requests.post(API_URL, json=bug_report_data)
    
    # Raise an exception if the API returned an error status code (e.g., 400, 500)
    response.raise_for_status()

    print("\n Success! API Response:")
    # .json() automatically parses the JSON response into a Python dictionary
    print(response.json())

except requests.exceptions.ConnectionError:
    print("\n Error: Could not connect to the API.")
    print("Please ensure the Flask server (app.py) is running.")
except requests.exceptions.HTTPError:
    print(f"\n Error: The API returned a non-200 status code: {response.status_code}")
    print("Server response:", response.text)
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")