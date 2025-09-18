#!/usr/bin/env python
"""
A simple executable script to send emails using the emailer package.

Usage:
    python send_email.py --to recipient@example.com --subject "Hello" --body "This is a test email"
    
    Additional options:
    --config-file CONFIG_FILE  Path to a JSON, INI, or .env configuration file
    --html                     Send the email as HTML
    --cc CC                    Carbon copy recipient(s)
    --bcc BCC                  Blind carbon copy recipient(s)
    --attachment FILE          File to attach (can be used multiple times)
"""

import argparse
import os
import sys
from typing import List, Optional

from emailer import EmailSender, get_config


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Send an email using the emailer package.")
    
    # Required arguments
    parser.add_argument("--to", required=True, help="Recipient email address(es), comma-separated")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body content")
    
    # Optional arguments
    parser.add_argument("--config-file", help="Path to a JSON or INI configuration file")
    parser.add_argument("--html", action="store_true", help="Send the email as HTML")
    parser.add_argument("--cc", help="Carbon copy recipient(s), comma-separated")
    parser.add_argument("--bcc", help="Blind carbon copy recipient(s), comma-separated")
    parser.add_argument("--attachment", action="append", help="File to attach (can be used multiple times)")
    
    return parser.parse_args()


def get_email_config(config_file: Optional[str] = None) -> dict:
    """
    Get email configuration from environment variables or config file.
    
    Args:
        config_file: Path to a JSON, INI, or .env configuration file
        
    Returns:
        Dict containing email configuration
    """
    config = {}
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    # Determine file type and load configuration
    if config_file:
        if config_file.lower().endswith('.json'):
            config = get_config(json_path=config_file)
        elif config_file.lower().endswith('.ini'):
            config = get_config(ini_path=config_file)
        elif config_file.lower().endswith('.env'):
            config = get_config(dotenv_path=config_file)
        else:
            print(f"Unsupported configuration file format: {config_file}")
            print("Supported formats: .json, .ini, .env")
            sys.exit(1)
    else:
        # Check if .env file exists in the current directory
        if os.path.isfile(dotenv_path):
            config = get_config(dotenv_path=dotenv_path)
        else:
            # Try to load from environment variables
            config = get_config()
    
    # Check if we have the required configuration
    if not config.get('email') or not config.get('password'):
        print("Error: Missing email credentials.")
        print("Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables,")
        print("create a .env file in the current directory,")
        print("or provide a configuration file with --config-file.")
        sys.exit(1)
    
    return config


def main():
    """Main function to send an email."""
    args = parse_args()
    
    # Get email configuration
    config = get_email_config(args.config_file)
    
    # Initialize the email sender
    sender = EmailSender(**config)
    
    # Prepare email parameters
    email_params = {
        "to_emails": [email.strip() for email in args.to.split(",")],
        "subject": args.subject,
        "body": args.body,
        "html": args.html
    }
    
    # Add CC if provided
    if args.cc:
        email_params["cc"] = [email.strip() for email in args.cc.split(",")]
    
    # Add BCC if provided
    if args.bcc:
        email_params["bcc"] = [email.strip() for email in args.bcc.split(",")]
    
    # Add attachments if provided
    if args.attachment:
        # Verify that all attachment files exist
        for file_path in args.attachment:
            if not os.path.isfile(file_path):
                print(f"Error: Attachment file not found: {file_path}")
                sys.exit(1)
        
        email_params["attachments"] = args.attachment
    
    # Send the email
    success = sender.send_email(**email_params)
    
    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
        sys.exit(1)


if __name__ == "__main__":
    main()