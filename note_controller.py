import requests
from os import getenv
from dotenv import load_dotenv
from time import sleep
import threading

# Initialize environment variables
load_dotenv()

API_BASE_URL = getenv("API_BASE_URL")

# Local cache to store notes, reducing the need for GET requests
local_notes_cache = {}

def create_or_update_notes(batch):
    """
    Accepts a list of notes to create or update. Each item in the batch
    is a dictionary with the necessary information.
    """
    successful_ops = []
    for note in batch:
        if 'id' in note:
            # This is an update operation
            response = requests.put(f"{API_BASE_URL}/notes/{note['id']}", json=note)
        else:
            # This is a create operation
            response = requests.post(f"{API_BASE_URL}/notes", json=note)
        
        if response.status_code in [200, 201]:  # Assuming these are success status codes
            result = response.json()
            # Update local cache
            local_notes_cache[result['id']] = result
            successful_ops.append(result)
        else:
            print("Error with operation: ", note)
    
    return successful_ops

def create_note(title, text):
    # Instead of directly creating a note, we prepare it for batching
    note_data = {"title": title, "content": text}
    # Here you could add this to a queue/batch which is periodically sent
    # For simplicity, we're calling the method directly
    return create_or_update_notes([note_data])

def get_note_by_id(note_id):
    # Firstly, check if note is in cache
    if note_id in local_notes_cache:
        return local_notes_cache[note_id]
    
    # If not in cache, fetch it and update cache
    response = requests.get(f"{API_BASE_URL}/notes/{note_id}")
    if response.status_code == 200:
        note = response.json()
        local_notes_cache[note_id] = note
        return note
    return response.json()  # Returning API response directly in case of an error

def update_note_by_id(note_id, new_title=None, new_content=None):
    updated_data = {"id": note_id}
    if new_title:
        updated_data["title"] = new_title
    if new_content:
        updated_data["content"] = new_content
    
    # Here we prepare for batching, similarly to create
    return create_or_update_notes([updated_data])

def delete_note_by_id(note_id):
    response = requests.delete(f"{API_BASE_URL}/notes/{note_id}")
    # On successful deletion, remove from local cache
    if response.status_code == 200:
        local_notes_cache.pop(note_id, None)
    return response.json()