import configparser
import os
import pytest
import logging

def load_credentials():
    config = configparser.ConfigParser()
    if not os.path.exists('credentials.properties'):
        logging.error("Missing credentials.properties file.")
        pytest.fail("Missing credentials.properties file.")

    config.read('credentials.properties')
    try:
        return config['creds']['username'], config['creds']['password']
    except KeyError as e:
        logging.error(f"Missing key in credentials file: {e}")
        pytest.fail(f"Missing key in credentials file: {e}")
