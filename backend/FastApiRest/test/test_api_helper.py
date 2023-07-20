import pytest
import string
import secrets
from api.helper import gen_salt

def test_gen_salt_length():
    salt = gen_salt()
    assert len(salt) == 64

def test_gen_salt_characters():
    salt = gen_salt()
    allowed_characters = string.ascii_letters + string.digits
    assert all(char in allowed_characters for char in salt)

def test_gen_salt_uniqueness():
    salts = [gen_salt() for _ in range(100)]
    assert len(set(salts)) == 100

# Run the tests
pytest.main()
