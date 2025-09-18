"""
Example of using the configuration module to load email credentials.
"""

import os
from email_automation.emailer import EmailSender, get_config, load_from_json, load_from_ini, load_from_dotenv

def example_env_vars():
    """Example of loading credentials from environment variables."""
    print("Loading credentials from environment variables...")
    
    # In a real scenario, you would set these in your environment
    # For demonstration, we're setting them programmatically
    os.environ["EMAIL_ADDRESS"] = "env.example@gmail.com"
    os.environ["EMAIL_PASSWORD"] = "env-password"
    os.environ["EMAIL_SMTP_SERVER"] = "smtp.gmail.com"
    os.environ["EMAIL_SMTP_PORT"] = "587"
    
    # Load configuration from environment variables
    config = get_config()
    
    print(f"Loaded email: {config.get('email')}")
    print(f"Loaded SMTP server: {config.get('smtp_server')}")
    
    # Create EmailSender using the loaded configuration
    sender = EmailSender(**config)
    
    # Now you can use sender to send emails
    # (commented out to avoid actual sending)
    """
    sender.send_email(
        to_emails="recipient@example.com",
        subject="Email from Environment Variables",
        body="This email was configured using environment variables."
    )
    """
    
    # Clean up environment variables
    del os.environ["EMAIL_ADDRESS"]
    del os.environ["EMAIL_PASSWORD"]
    del os.environ["EMAIL_SMTP_SERVER"]
    del os.environ["EMAIL_SMTP_PORT"]


def create_example_config_files():
    """Create example configuration files for demonstration."""
    # Create example JSON config
    json_config = {
        "email": "json.example@gmail.com",
        "password": "json-password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    }
    
    import json
    with open("email_config.json", "w") as f:
        json.dump(json_config, f, indent=4)
    
    # Create example INI config
    ini_content = """[email]
email = ini.example@gmail.com
password = ini-password
smtp_server = smtp.gmail.com
smtp_port = 587
"""
    
    with open("email_config.ini", "w") as f:
        f.write(ini_content)
    
    # Create example .env config
    env_content = """EMAIL_ADDRESS=dotenv.example@gmail.com
EMAIL_PASSWORD=dotenv-password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
"""
    
    with open("email_config.env", "w") as f:
        f.write(env_content)
    
    print("Created example configuration files:")
    print("- email_config.json")
    print("- email_config.ini")
    print("- email_config.env")


def example_json_config():
    """Example of loading credentials from a JSON file."""
    print("\nLoading credentials from JSON file...")
    
    config = load_from_json("email_config.json")
    
    print(f"Loaded email: {config.get('email')}")
    print(f"Loaded SMTP server: {config.get('smtp_server')}")
    
    # Create EmailSender using the loaded configuration
    sender = EmailSender(**config)
    
    # Now you can use sender to send emails
    # (commented out to avoid actual sending)
    """
    sender.send_email(
        to_emails="recipient@example.com",
        subject="Email from JSON Config",
        body="This email was configured using a JSON configuration file."
    )
    """


def example_ini_config():
    """Example of loading credentials from an INI file."""
    print("\nLoading credentials from INI file...")
    
    config = load_from_ini("email_config.ini")
    
    print(f"Loaded email: {config.get('email')}")
    print(f"Loaded SMTP server: {config.get('smtp_server')}")
    
    # Create EmailSender using the loaded configuration
    sender = EmailSender(**config)
    
    # Now you can use sender to send emails
    # (commented out to avoid actual sending)
    """
    sender.send_email(
        to_emails="recipient@example.com",
        subject="Email from INI Config",
        body="This email was configured using an INI configuration file."
    )
    """


def example_dotenv_config():
    """Example of loading credentials from a .env file."""
    print("\nLoading credentials from .env file...")
    
    config = load_from_dotenv("email_config.env")
    
    print(f"Loaded email: {config.get('email')}")
    print(f"Loaded SMTP server: {config.get('smtp_server')}")
    
    # Create EmailSender using the loaded configuration
    sender = EmailSender(**config)
    
    # Now you can use sender to send emails
    # (commented out to avoid actual sending)
    """
    sender.send_email(
        to_emails="recipient@example.com",
        subject="Email from .env Config",
        body="This email was configured using a .env configuration file."
    )
    """


def example_priority():
    """Example demonstrating configuration priority."""
    print("\nDemonstrating configuration priority...")
    
    # Set environment variable (highest priority)
    os.environ["EMAIL_ADDRESS"] = "env.priority@gmail.com"
    
    # Load from all sources
    config = get_config(
        json_path="email_config.json",
        dotenv_path="email_config.env",
        ini_path="email_config.ini"
    )
    
    print(f"Final email (should be from env): {config.get('email')}")
    
    # Now remove the environment variable to see the next priority
    del os.environ["EMAIL_ADDRESS"]
    
    # Load from all sources except environment variables
    config = get_config(
        json_path="email_config.json",
        dotenv_path="email_config.env",
        ini_path="email_config.ini"
    )
    
    print(f"Final email (should be from json): {config.get('email')}")
    
    # Now remove the JSON file from the priority to see the next priority
    config = get_config(
        dotenv_path="email_config.env",
        ini_path="email_config.ini"
    )
    
    print(f"Final email (should be from dotenv): {config.get('email')}")
    
    # Now remove the .env file from the priority to see the lowest priority
    config = get_config(
        ini_path="email_config.ini"
    )
    
    print(f"Final email (should be from ini): {config.get('email')}")


def cleanup():
    """Remove example configuration files."""
    import os
    
    if os.path.exists("email_config.json"):
        os.remove("email_config.json")
    
    if os.path.exists("email_config.ini"):
        os.remove("email_config.ini")
    
    if os.path.exists("email_config.env"):
        os.remove("email_config.env")
    
    print("\nRemoved example configuration files.")


def main():
    # Example of loading from environment variables
    example_env_vars()
    
    # Create example configuration files
    create_example_config_files()
    
    # Example of loading from JSON
    example_json_config()
    
    # Example of loading from INI
    example_ini_config()
    
    # Example of loading from .env
    example_dotenv_config()
    
    # Example of configuration priority
    example_priority()
    
    # Clean up
    cleanup()


if __name__ == "__main__":
    main()