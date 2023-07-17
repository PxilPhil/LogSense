import configparser

import pytest
from unittest import mock

from db_access import get_database_config, generate_tables


#def test_generate_tables_success():
#    result = generate_tables(test_get_database_config('../config.ini'))
#    assert result is True
#
#def test_generate_tables_file_not_found():
#    with mock.patch('builtins.open', side_effect=FileNotFoundError):
#        result = generate_tables('localhost', 5432, 'mydb', 'user', 'password')
#        assert result is False
#
#def test_generate_tables_error():
#    with mock.patch('builtins.open', mock.mock_open(read_data='CREATE TABLE users (id SERIAL, name VARCHAR);')):
#        with mock.patch('psycopg2.connect', side_effect=Exception('Connection failed.')):
#            result = generate_tables('localhost', 5432, 'mydb', 'user', 'password')
#            assert result is False


#@pytest.fixture
#def config_file(tmp_path):
#    config_path = tmp_path / "config.ini"
#    config = configparser.ConfigParser()
#    config['Database'] = {
#        'db_host': 'localhost',
#        'db_port': '5432',
#        'db_name': 'mydb',
#        'db_user': 'user',
#        'db_password': 'password'
#    }
#    with open(config_path, 'w') as config_file:
#        config.write(config_file)
#    return config_path
#
#def test_get_database_config(config_file):
#    db_host, db_port, db_name, db_user, db_password = get_database_config(config_file)
#    assert db_host == 'localhost'
#    assert db_port == '5432'
#    assert db_name == 'mydb'
#    assert db_user == 'user'
#    assert db_password == 'password'
