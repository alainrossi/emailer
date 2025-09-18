"""
Emailer - A Python package for sending automated emails.

This package provides a simple interface for sending emails from various email providers,
with support for attachments, HTML content, and email templates.
"""

from .emailer import EmailSender
from .config import get_config, load_from_env, load_from_json, load_from_ini, load_from_dotenv

__version__ = '0.1.0'
__author__ = 'Your Name'