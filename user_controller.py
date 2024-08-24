import requests
from dotenv import load_dotenv
import os
from requests.exceptions import RequestException

load_dotenv()

BASE_URL = os.getenv('API_BASE_URL')

def register_user(username, password, email):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password,
        "email": email
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except RequestException as e:
        return {"error": str(e)}
        
def login_user(username, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}

def fetch_user_details(username, password):
    login_response = login_user(username, password)
    if 'token' in login_response:
        token = login_response['token']
        headers = {'Authorization': f'Bearer {token}'}
        url = f"{BASE_URL}/users/{username}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}
    else:
        return login_response  # This will return the login error
        
def create_note(username, password, title, content):
    login_response = login_user(username, password)
    if 'token' in login_response:
        token = login_response['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "title": title,
            "content": content
        }
        url = f"{BASE_URL}/notes"

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}
    else:
        return login_response

if __name__ == "__main__":
    username = 'exampleUser'
    password = 'examplePass'
    email = 'user@example.com'
    title = 'My First Note'
    content = 'This is the content of my first note.'

    # Example for creating a note (consider checking and handling the error in the actual response)
    create_note_response = create_note(username, password, title, content)
    if 'error' not in create_note_response:
        print(create_note_response)
    else:
        print("An error occurred:", create_note_response['error'])