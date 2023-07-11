"""
This module contains general functions for the marketplace.
"""

import logging
import sys
import yaml

try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    logging.error("config.yaml not found. please create one.")
    sys.exit(1)
