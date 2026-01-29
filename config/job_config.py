import json
import os

_job_roles = None

def load_job_roles():
    """
    Loads job roles from the JSON file.
    Caches the data after the first read to avoid repeated file I/O.
    """
    global _job_roles
    if _job_roles is not None:
        return _job_roles

    try:
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(dir_path, 'job_roles.json')
        
        with open(json_path, 'r') as f:
            _job_roles = json.load(f)
        return _job_roles
    except FileNotFoundError:
        print("Error: config/job_roles.json not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Could not decode config/job_roles.json.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while loading job roles: {e}")
        return {}

# You can also provide a constant that pre-loads the data
JOB_ROLES = load_job_roles()
