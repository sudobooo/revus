# app/config.py

import os
import toml
from .logger import log_error, log_warning

_config_instance = None


def _load_config():
    config_path = os.path.join(os.getcwd(), "config.toml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as config_file:
                return toml.load(config_file)
        except Exception as e:
            log_error(f"Error loading configuration file: {e}")
            return {}
    else:
        log_warning("Configuration file not found, default values will be used.")
        return {}


def _get_config_instance():
    global _config_instance
    if _config_instance is None:
        _config_instance = _load_config()
    return _config_instance


def get_config(key, default=None):
    config = _get_config_instance()
    return config.get(key, default)


__all__ = ["get_config"]
