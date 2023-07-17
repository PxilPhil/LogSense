import pytest
import re
from db_access.helper import is_valid_email

def test_valid_email():
    email = "test@example.com"
    assert is_valid_email(email) is True

def test_invalid_email():
    email = "invalid_email"
    assert is_valid_email(email) is False

def test_empty_email():
    email = ""
    assert is_valid_email(email) is False

def test_no_at_symbol():
    email = "testexample.com"
    assert is_valid_email(email) is False

def test_no_domain():
    email = "test@"
    assert is_valid_email(email) is False

def test_no_tld():
    email = "test@example"
    assert is_valid_email(email) is False

# Run the tests
pytest.main()
