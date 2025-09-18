"""
Test script to verify that the load_from_dotenv function can load configuration from a .env file.
"""

from emailer import load_from_dotenv

def main():
    print("Testing loading configuration from .env file...")
    
    config = load_from_dotenv('.env')
    
    print(f"Loaded email: {config.get('email')}")
    print(f"Loaded SMTP server: {config.get('smtp_server')}")
    print(f"Loaded SMTP port: {config.get('smtp_port')}")
    
    if config.get('email') and config.get('password') and config.get('smtp_server') and config.get('smtp_port'):
        print("SUCCESS: All required configuration values were loaded from the .env file.")
    else:
        print("ERROR: Some required configuration values were not loaded from the .env file.")
        print("Missing values:")
        if not config.get('email'):
            print("- email")
        if not config.get('password'):
            print("- password")
        if not config.get('smtp_server'):
            print("- smtp_server")
        if not config.get('smtp_port'):
            print("- smtp_port")

if __name__ == "__main__":
    main()