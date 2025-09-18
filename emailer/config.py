"""
Configuration module for the emailer package.

This module provides utilities for loading email credentials from environment variables
or configuration files to avoid hardcoding sensitive information in scripts.
"""

import os
import json
import configparser
from typing import Dict, Optional, Tuple


def load_from_env(prefix: str = "EMAIL_") -> Dict[str, str]:
    """
    Load email configuration from environment variables.
    
    Expected environment variables:
    - {prefix}ADDRESS: Email address
    - {prefix}PASSWORD: Email password or app password
    - {prefix}SMTP_SERVER: SMTP server address (optional)
    - {prefix}SMTP_PORT: SMTP server port (optional)
    
    Args:
        prefix: Prefix for environment variables (default: "EMAIL_")
        
    Returns:
        Dict containing email configuration
    """
    config = {}
    
    # Required fields
    email = os.environ.get(f"{prefix}ADDRESS")
    password = os.environ.get(f"{prefix}PASSWORD")
    
    if email:
        config["email"] = email
    if password:
        config["password"] = password
    
    # Optional fields
    smtp_server = os.environ.get(f"{prefix}SMTP_SERVER")
    smtp_port = os.environ.get(f"{prefix}SMTP_PORT")
    
    if smtp_server:
        config["smtp_server"] = smtp_server
    if smtp_port:
        try:
            config["smtp_port"] = int(smtp_port)
        except ValueError:
            pass
    
    return config


def load_from_json(file_path: str) -> Dict[str, str]:
    """
    Load email configuration from a JSON file.
    
    Expected JSON structure:
    {
        "email": "your.email@example.com",
        "password": "your-password",
        "smtp_server": "smtp.example.com",
        "smtp_port": 587
    }
    
    Args:
        file_path: Path to the JSON configuration file
        
    Returns:
        Dict containing email configuration
    """
    if not os.path.isfile(file_path):
        return {}
    
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        
        # Convert smtp_port to int if it exists
        if "smtp_port" in config and isinstance(config["smtp_port"], str):
            try:
                config["smtp_port"] = int(config["smtp_port"])
            except ValueError:
                pass
        
        return config
    except (json.JSONDecodeError, IOError):
        return {}


def load_from_ini(file_path: str, section: str = "email") -> Dict[str, str]:
    """
    Load email configuration from an INI file.
    
    Expected INI structure:
    [email]
    email = your.email@example.com
    password = your-password
    smtp_server = smtp.example.com
    smtp_port = 587
    
    Args:
        file_path: Path to the INI configuration file
        section: Section name in the INI file (default: "email")
        
    Returns:
        Dict containing email configuration
    """
    if not os.path.isfile(file_path):
        return {}
    
    config = {}
    parser = configparser.ConfigParser()
    
    try:
        parser.read(file_path)
        if section in parser:
            for key, value in parser[section].items():
                config[key] = value
            
            # Convert smtp_port to int if it exists
            if "smtp_port" in config:
                try:
                    config["smtp_port"] = int(config["smtp_port"])
                except ValueError:
                    pass
    except configparser.Error:
        pass
    
    return config


def load_from_dotenv(file_path: str, prefix: str = "EMAIL_") -> Dict[str, str]:
    """
    Load email configuration from a .env file.
    
    Expected .env file format:
    EMAIL_ADDRESS=your.email@example.com
    EMAIL_PASSWORD=your-password
    EMAIL_SMTP_SERVER=smtp.example.com
    EMAIL_SMTP_PORT=587
    
    Args:
        file_path: Path to the .env file
        prefix: Prefix for environment variables (default: "EMAIL_")
        
    Returns:
        Dict containing email configuration
    """
    if not os.path.isfile(file_path):
        return {}
    
    config = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Support both KEY=value and KEY:value formats
                if '=' in line:
                    key, value = line.split('=', 1)
                elif ':' in line:
                    key, value = line.split(':', 1)
                else:
                    continue
                
                # Check if the key has the expected prefix
                if key.startswith(prefix):
                    # Remove prefix and convert to expected config key
                    config_key = key[len(prefix):].lower()
                    
                    # Map ADDRESS to email, etc.
                    if config_key == "address":
                        config_key = "email"
                    
                    config[config_key] = value
        
        # Convert smtp_port to int if it exists
        if "smtp_port" in config:
            try:
                config["smtp_port"] = int(config["smtp_port"])
            except ValueError:
                pass
                
        return config
    except IOError:
        return {}


def get_config(env_prefix: str = "EMAIL_", 
              json_path: Optional[str] = None,
              ini_path: Optional[str] = None,
              dotenv_path: Optional[str] = None,
              ini_section: str = "email") -> Dict[str, str]:
    """
    Get email configuration from multiple sources with priority:
    1. Environment variables
    2. JSON file (if provided)
    3. .env file (if provided)
    4. INI file (if provided)
    
    Args:
        env_prefix: Prefix for environment variables (default: "EMAIL_")
        json_path: Path to JSON configuration file (optional)
        ini_path: Path to INI configuration file (optional)
        dotenv_path: Path to .env configuration file (optional)
        ini_section: Section name in the INI file (default: "email")
        
    Returns:
        Dict containing email configuration
    """
    config = {}
    
    # Load from INI file (lowest priority)
    if ini_path:
        config.update(load_from_ini(ini_path, ini_section))
    
    # Load from .env file (medium-low priority)
    if dotenv_path:
        config.update(load_from_dotenv(dotenv_path, env_prefix))
    
    # Load from JSON file (medium-high priority)
    if json_path:
        config.update(load_from_json(json_path))
    
    # Load from environment variables (highest priority)
    config.update(load_from_env(env_prefix))
    
    return config