import streamlit as st
import requests
import google.auth
from google.auth.transport.requests import Request

PROJECT_ID = "psyduck766"
LOCATION = "us-central1"

# Reasoning engine IDs
SESSION_ENGINE_ID = "3446170707635994624"
QUERY_ENGINE_ID = "3446170707635994624"

BASE_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}"

def get_token():
    creds, project = google.auth.default()
    print("Credential type:", type(creds))
    print("Project:", project)

    # Always refresh the credentials to get a valid token
    creds.refresh(Request())

    # Now creds.token is valid
    print("Token exists:", creds.token[:20], "...")
    return creds.token


def create_session(user_id: str):
    url = f"{BASE_URL}/reasoningEngines/{SESSION_ENGINE_ID}:query"

    payload = {
        "class_method": "create_session",
        "input": {
            "user_id": user_id
        }
    }

    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()

    # Response shape depends on your engine implementation
    # Typically:
    # { "output": { "session_id": "..." } }
    return r.json()["output"]["id"]

def query_agent(user_id: str, session_id: str, message: str):
    url = f"{BASE_URL}/reasoningEngines/{QUERY_ENGINE_ID}:streamQuery"

    payload = {
        "class_method": "async_stream_query",
        "input": {
            "user_id": user_id,
            "session_id": session_id,
            "message": message
        }
    }

    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    # NOTE:
    # We are NOT consuming SSE incrementally here.
    # This just reads the full response for simplicity.
    r = requests.post(url, headers=headers, json=payload, timeout=90)
    r.raise_for_status()
    return r.text
