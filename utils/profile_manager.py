import json
import os

PROFILE_DIR = 'user_profiles'

def save_profile(email, form_data):
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    safe_email = "".join([c if c.isalnum() else "_" for c in email])
    file_path = os.path.join(PROFILE_DIR, f"{safe_email}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(form_data, f)

def load_profile(email):
    safe_email = "".join([c if c.isalnum() else "_" for c in email])
    file_path = os.path.join(PROFILE_DIR, f"{safe_email}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return None
