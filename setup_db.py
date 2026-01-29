import sys
import os

# Add the current directory to sys.path so we can import config
sys.path.append(os.getcwd())

from config.database import init_database, add_admin

print("Initializing database...")
init_database()
print("Database initialized.")

# Get credentials from environment variables
admin_email = os.getenv('ADMIN_EMAIL')
admin_password = os.getenv('ADMIN_PASSWORD')

# Validate that environment variables are set
if not all([admin_email, admin_password]):
    raise ValueError("ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set.")

print("Adding default admin...")
success = add_admin(admin_email, admin_password)
if success:
    print(f"Default admin added: {admin_email}")
else:
    print("Failed to add admin (might already exist).")
