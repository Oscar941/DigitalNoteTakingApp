import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = getenv("API_BASE_URL")

def create_note(title, text):
    data = {"title": title, "content": text}
    response = requests.post(f"{API_BASE_URL}/notes", json=data)
    return response.json()

def get_note_by_id(note_id):
    response = requests.get(f"{API_BASE_URL}/notes/{note_id}")
    return response.json()

def update_note_by_id(note_id, new_title=None, new_content=None):
    updated_data = {}
    if new_title:
        updated_data["title"] = new_title
    if new_content:
        updated_data["content"] = new_content

    response = requests.put(f"{API_BASE_URL}/notes/{note_id}", json=updated_data)
    return response.json()

def delete_note_by_id(note_id):
    response = requests.delete(f"{API_BASE_URL}/notes/{note_id}")
    return response.json()