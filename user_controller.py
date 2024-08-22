import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('API_BASE_URL')

def register_user(username, password, email):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password,
        "email": email
    }
    response = requests.post(url, json=payload)
    return response.json()

def login_user(username, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response.json()

def fetch_user_details(username):
    token = login_user(username, password)['token']
    headers = {'Authorization': f'Bearer {token}'}
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=headers)
    return response.json()

def create_note(username, password, title, content):
    token = login_user(username, password)['token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "title": title,
        "content": content
    }
    url = f"{BASE_URL}/notes"
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    username = 'exampleUser'
    password = 'examplePass'
    email = 'user@example.com'
    title = 'My First Note'
    content = 'This is the content of my first note.'

    print(create_note(username, password, title, content))