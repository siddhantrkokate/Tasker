import requests
import json
import os

def load_api_keys():
    """Load API keys from config file."""
    config_file = "api_keys.txt"
    keys = {
        'blackbox_api_key': '',
        'gemini_api_key': '',
        'krutrim_api_key': ''
    }
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    keys[key.strip()] = value.strip()
    
    return keys

def save_api_keys(keys):
    """Save API keys to config file."""
    config_file = "api_keys.txt"
    with open(config_file, 'w') as f:
        for key, value in keys.items():
            f.write(f"{key}={value}\n")

def setup_api_keys():
    """Prompt user for API keys if not already configured."""
    keys = load_api_keys()
    needs_setup = False
    
    # Check if Krutrim API key is missing
    if not keys.get('krutrim_api_key'):
        needs_setup = True
    
    if needs_setup:
        print("=" * 60)
        print("FIRST-TIME API KEYS SETUP")
        print("=" * 60)
        print("Please enter your Krutrim API key (used for AI functions).\n")
        
        krutrim_key = input("Enter Krutrim API Key: ").strip()
        if krutrim_key:
            keys['krutrim_api_key'] = krutrim_key
            save_api_keys(keys)
            print("\n✓ API key saved successfully!")
            print("=" * 60)
            print("\n")
        else:
            print("\n⚠ Warning: No API key provided. AI features may not work.")
            print("=" * 60)
            print("\n")
    
    return keys

def generate_text(text):
    keys = load_api_keys()
    url = "https://api.blackbox.ai/chat/completions"
    user_api_key = keys.get('blackbox_api_key', '')
    
    if not user_api_key:
        return "Error: Blackbox API key not configured. Please run setup_api_keys() first."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_api_key}"
    }

    data = {
        "model": "blackboxai/anthropic/claude-sonnet-4",
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    # Convert JSON response to Python dict
    response_dict = response.json()

    # Extract only the assistant's message text
    realReturn = str(response_dict['choices'][0]['message']['content'])
    return realReturn

def gemini(user_input, system_instructions=None):
    keys = load_api_keys()
    GEMINI_API_KEY = keys.get('gemini_api_key', '')
    
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured. Please run setup_api_keys() first."
    
    MODEL_ID = "gemini-2.0-flash"
    GENERATE_CONTENT_API = "generateContent"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:{GENERATE_CONTENT_API}?key={GEMINI_API_KEY}"

    parts = []
    
    if system_instructions:
        parts.append({"text": system_instructions})
    
    parts.append({"text": user_input})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ],
        "generationConfig": {
            "responseMimeType": "text/plain",
            "maxOutputTokens": 10000
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

    try:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, json.JSONDecodeError):
        print("Failed to parse response.")
        return response.text

def llama(text):
    keys = load_api_keys()
    api_key = keys.get('krutrim_api_key', '')
    
    if not api_key:
        return "Error: Krutrim API key not configured. Please run setup_api_keys() first."
    
    model_name = "Llama-3.3-70B-Instruct"
    messages = [
        {"role": "user", "content": text}
    ]
    url = "https://cloud.olakrutrim.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model_name,
        "messages": messages,
        "frequency_penalty": 0,
        "logprobs": True,
        "top_logprobs": 2,
        "max_tokens": 5000,
        "n": 1,
        "presence_penalty": 0,
        "response_format": {"type": "text"},
        "stream": False,
        "temperature": 0,
        "top_p": 1
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as exc:
        return f"Exception: {exc}"

import requests
import json

def gpt_curl(user_message, system_message):
    keys = load_api_keys()
    final = "user input: " +user_message + "\n. Instructions for you: " + system_message
    api_key = keys.get('krutrim_api_key', '')
    
    if not api_key:
        return "Error: Krutrim API key not configured. Please run setup_api_keys() first."
    
    url = "https://cloud.olakrutrim.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-oss-120b",
        "messages": [
            {"role": "user", "content": final}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as exc:
        return f"Exception: {exc}"
