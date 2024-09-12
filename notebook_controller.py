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

def create_notebook(data):
    response = requests.post(f"{BASE_URL}/notebooks", headers=HEADERS, json=data)
    return response.json()

def read_notebook(notebook_id):
    response = requests.get(f"{BASE_URL}/notebooks/{notebook_id}", headers=HEADERS)
    return response.json()

def update_notebook(notebook_id, data):
    response = requests.put(f"{BASE_URL}/notebooks/{notebook_id}", headers=HEADERS, json=data)
    return response.json()

def delete_notebook(notebook_id):
    response = requests.delete(f"{BASE_URL}/notebooks/{notebook_id}", headers=HEADERS)
    return response.json()