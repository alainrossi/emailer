# Emailer

A Python package for sending automated emails from your own mailbox.

## Features

- Send plain text or HTML emails
- Support for attachments
- Template-based emails with variable substitution
- Support for CC and BCC recipients
- Compatible with various email providers (Gmail, Outlook, Yahoo, etc.)

## Installation

```bash
pip install emailer
```

Or install from source:

```bash
git clone https://github.com/yourusername/emailer.git
cd emailer
pip install -e .
```

## Usage

### Command-Line Script

The package includes a command-line script for sending emails directly from the terminal:

```bash
# On Unix-like systems
./send_email.py --to recipient@example.com --subject "Hello" --body "This is a test email"

# On Windows
send_email.bat --to recipient@example.com --subject "Hello" --body "This is a test email"
```

Additional options:

```
--config-file CONFIG_FILE  Path to a JSON or INI configuration file
--html                     Send the email as HTML
--cc CC                    Carbon copy recipient(s), comma-separated
--bcc BCC                  Blind carbon copy recipient(s), comma-separated
--attachment FILE          File to attach (can be used multiple times)
```

Example with multiple recipients and attachments:

```bash
send_email.bat --to "recipient1@example.com,recipient2@example.com" --subject "Meeting Notes" --body "Please find attached the meeting notes." --attachment "notes.pdf" --attachment "presentation.pptx" --cc "manager@example.com"
```

The script will look for email credentials in the following order:
1. Environment variables (EMAIL_ADDRESS and EMAIL_PASSWORD)
2. A `.env` file in the current directory
3. A configuration file specified with --config-file

Example configuration files are provided in the repository:
- `email_config_example.json` - JSON format example
- `email_config_example.ini` - INI format example

You can also create a `.env` file with the following format:
```
EMAIL_ADDRESS=your.email@example.com
EMAIL_PASSWORD=your-password
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=587
```

Notes:
- If your provider requires implicit SSL on port 465 (e.g., IONOS), set EMAIL_SMTP_PORT=465. The script will automatically use SSL for 465 and STARTTLS for 587.
- If you use port 587, STARTTLS is used after EHLO. For 465, an SSL connection is established immediately.

To use a configuration file:

```bash
# Using JSON configuration
send_email.bat --to recipient@example.com --subject "Hello" --body "Test email" --config-file email_config_example.json

# Using INI configuration
send_email.bat --to recipient@example.com --subject "Hello" --body "Test email" --config-file email_config_example.ini

# Using .env configuration
send_email.bat --to recipient@example.com --subject "Hello" --body "Test email" --config-file .env
```

Make sure to update these files with your actual email credentials before using them.

Note: If you place a `.env` file in the same directory as the script, it will be used automatically if no configuration file is specified.

### Basic Usage

```python
from email_automation.emailer import EmailSender

# Initialize the email sender
# For Gmail, you'll need to use an App Password if 2FA is enabled
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
```

### Sending HTML Emails

```python
html_content = """
<html>
<body>
    <h1>Hello from Emailer</h1>
    <p>This is a <b>HTML</b> email sent using the Emailer package.</p>
    <p>You can include <a href="https://example.com">links</a> and other HTML elements.</p>
</body>
</html>
"""

sender.send_html_email(
    to_emails="recipient@example.com",
    subject="HTML Email Example",
    html_body=html_content
)
```

### Sending Emails with Attachments

```python
sender.send_email(
    to_emails="recipient@example.com",
    subject="Email with Attachment",
    body="Please find the attached document.",
    attachments=["path/to/document.pdf", "path/to/image.jpg"]
)
```

### Using Templates with Variable Substitution

```python
template = """
Hello {name},

Thank you for your {product} order. Your order number is {order_number}.

Best regards,
The {company} Team
"""

sender.send_template_email(
    to_emails="customer@example.com",
    subject="Your Order Confirmation",
    template=template,
    template_vars={
        "name": "John Doe",
        "product": "Premium Widget",
        "order_number": "ORD-12345",
        "company": "Acme Inc"
    },
    html=False  # This is a plain text template
)
```

### HTML Templates

```python
html_template = """
<html>
<body>
    <h1>Hello {name}!</h1>
    <p>Thank you for your <b>{product}</b> order.</p>
    <p>Your order number is: <b>{order_number}</b></p>
    <p>
        Best regards,<br>
        The {company} Team
    </p>
</body>
</html>
"""

sender.send_template_email(
    to_emails="customer@example.com",
    subject="Your Order Confirmation",
    template=html_template,
    template_vars={
        "name": "John Doe",
        "product": "Premium Widget",
        "order_number": "ORD-12345",
        "company": "Acme Inc"
    },
    html=True  # This is an HTML template
)
```

### Multiple Recipients, CC, and BCC

```python
sender.send_email(
    to_emails=["recipient1@example.com", "recipient2@example.com"],
    subject="Announcement",
    body="Important announcement for all team members.",
    cc="manager@example.com",
    bcc=["admin1@example.com", "admin2@example.com"]
)
```

## Email Provider Settings

### Gmail

```python
sender = EmailSender(
    email="your.email@gmail.com",
    password="your-app-password",  # Use App Password if 2FA is enabled
    smtp_server="smtp.gmail.com",
    smtp_port=587
)
```

### Outlook/Hotmail

```python
sender = EmailSender(
    email="your.email@outlook.com",
    password="your-password",
    smtp_server="smtp-mail.outlook.com",
    smtp_port=587
)
```

### Yahoo

```python
sender = EmailSender(
    email="your.email@yahoo.com",
    password="your-app-password",  # Use App Password
    smtp_server="smtp.mail.yahoo.com",
    smtp_port=587
)
```

## Security Considerations

- Never hardcode your email password in your scripts. Use environment variables or a secure configuration file.
- For Gmail and many other providers, you'll need to use an App Password if you have 2-Factor Authentication enabled.
- Consider using a dedicated email account for automated emails rather than your personal account.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.