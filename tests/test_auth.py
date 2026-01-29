import pytest
from unittest.mock import MagicMock, patch
from views.signup import render_signup
import re

# Mock the Streamlit module as it is imported in views.signup
@pytest.fixture
def mock_streamlit_module():
    with patch('views.signup.st') as mock_st:
        # Make mock_st.form behave as a context manager
        mock_st.form.return_value.__enter__.return_value = MagicMock()
        mock_st.form.return_value.__exit__.return_value = None

        # Directly mock the functions used within render_signup
        mock_st.text_input = MagicMock()
        mock_st.form_submit_button = MagicMock()
        mock_st.error = MagicMock()
        mock_st.success = MagicMock()

        yield mock_st

# Mock the database function add_user
@pytest.fixture
def mock_add_user():
    with patch('views.signup.add_user') as mock_add_user_func:
        yield mock_add_user_func

def test_signup_successful(mock_streamlit_module, mock_add_user):
    """Test successful user signup with valid credentials."""
    mock_streamlit_module.text_input.side_effect = ["test@example.com", "password123", "password123"]
    mock_streamlit_module.form_submit_button.return_value = True
    mock_add_user.return_value = True

    render_signup()

    mock_streamlit_module.success.assert_called_once_with("You have successfully signed up! Please go to the Sign In page to log in.")
    mock_add_user.assert_called_once_with("test@example.com", "password123")

def test_signup_empty_fields(mock_streamlit_module, mock_add_user):
    """Test signup with empty fields."""
    mock_streamlit_module.text_input.side_effect = ["", "", ""] # Empty email, password, confirm
    mock_streamlit_module.form_submit_button.return_value = True

    render_signup()

    mock_streamlit_module.error.assert_called_once_with("All fields are required.")
    mock_add_user.assert_not_called()

def test_signup_invalid_email_format(mock_streamlit_module, mock_add_user):
    """Test signup with an invalid email format."""
    mock_streamlit_module.text_input.side_effect = ["invalid-email", "password123", "password123"]
    mock_streamlit_module.form_submit_button.return_value = True

    render_signup()

    mock_streamlit_module.error.assert_called_once_with("Invalid email format. Please enter a valid email address.")
    mock_add_user.assert_not_called()

def test_signup_password_too_short(mock_streamlit_module, mock_add_user):
    """Test signup with a password shorter than 8 characters."""
    mock_streamlit_module.text_input.side_effect = ["test@example.com", "short", "short"]
    mock_streamlit_module.form_submit_button.return_value = True

    render_signup()

    mock_streamlit_module.error.assert_called_once_with("Password is too short. It must be at least 8 characters long.")
    mock_add_user.assert_not_called()

def test_signup_passwords_do_not_match(mock_streamlit_module, mock_add_user):
    """Test signup when password and confirm password do not match."""
    mock_streamlit_module.text_input.side_effect = ["test@example.com", "password123", "different"]
    mock_streamlit_module.form_submit_button.return_value = True

    render_signup()

    mock_streamlit_module.error.assert_called_once_with("Passwords do not match.")
    mock_add_user.assert_not_called()

def test_signup_email_already_exists(mock_streamlit_module, mock_add_user):
    """Test signup when the email already exists in the database."""
    mock_streamlit_module.text_input.side_effect = ["existing@example.com", "password123", "password123"]
    mock_streamlit_module.form_submit_button.return_value = True
    mock_add_user.return_value = False # Simulate email already exists

    render_signup()

    mock_streamlit_module.error.assert_called_once_with("Email already exists. Please try a different email.")
    mock_add_user.assert_called_once_with("existing@example.com", "password123")

