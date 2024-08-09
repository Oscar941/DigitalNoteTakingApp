import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv("BASE_URL")

def create_note(title, content):
    payload = {"title": title, "content": content}
    response = requests.post(f"{BASE_URL}/notes", json=payload)
    return response.json()

def read_note(note_id):
    response = requests.get(f"{BASE_URL}/notes/{note_id}")
    return response.json()

def update_note(note_id, title=None, content=None):
    payload = {}
    if title:
        payload["title"] = title
    if content:
        payload["content"] = content

    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=payload)
    return response.json()

def delete_note(note_id):
    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    return response.json()