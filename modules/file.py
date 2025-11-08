import os
import re

def append_to_file(file_path, data):
    # Create parent directories if they don't exist
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'a') as file:
        file.write(data)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def empty_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            file.truncate(0)
            file.seek(0)  # Move the file pointer to the beginning

def extract_python_code(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

import re

def process_string(s):
    """
    Remove whitespace and convert to lowercase.

    Args:
        s (str): The string to process.

    Returns:
        str: The processed string.
    """
    return re.sub(r"\s+", "", s).lower()