import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NOTEBOOK_API_URL")
API_KEY = os.getenv("NOTEBOOK_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def execute_request(method, url, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=HEADERS)
        elif method == 'POST':
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=HEADERS, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=HEADERS)
        
        response.raise_for_status()  
    except requests.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err} — Status code: {response.status_code}"}
    except requests.ConnectionError:
        return {"error": "Connection error occurred"}
    except requests.Timeout:
        return {"error": "The request timed out"}
    except requests.RequestException as err:
        return {"error": f"Request failed: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

    try:
        return response.json()
    except ValueError:
        return {"error": "JSON decoding failed"}

def create_notebook(data):
    url = f"{BASE_URL}/notebooks"
    return execute_request('POST', url, data=data)

def read_notebook(notebook_id):
    url = f"{BASE_URL}/notebooks/{notebook_id}"
    return execute_request('GET', url)

def update_notebook(notebook_id, data):
    url = f"{BASE_URL}/notebooks/{notebook_id}"
    return execute_request('PUT', url, data=data)

def delete_notebook(notebook_id):
    url = f"{BASE_URL}/notebooks/{notebook_id}"
    return execute_request('DELETE', url)