"""
Basic example of sending an email using the emailer package.
"""

from email_automation.emailer import EmailSender

def main():
    # Initialize the email sender
    # Replace with your actual email credentials
    sender = EmailSender(
        email="your.email@gmail.com",
        password="your-password-or-app-password",
        smtp_server="smtp.gmail.com",  # Default for Gmail
        smtp_port=587  # Default TLS port
    )
    
    # Send a simple email
    success = sender.send_email(
        to_emails="recipient@example.com",
        subject="Hello from Emailer",
        body="This is a test email sent using the Emailer package."
    )
    
    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")

if __name__ == "__main__":
    main()