"""
Example of sending template-based emails using the emailer package.
"""

from email_automation.emailer import EmailSender

def main():
    # Initialize the email sender
    # Replace with your actual email credentials
    sender = EmailSender(
        email="your.email@gmail.com",
        password="your-password-or-app-password",
        smtp_server="smtp.gmail.com",
        smtp_port=587
    )
    
    # Plain text template example
    text_template = """
Hello {name},

Thank you for your {product} order. Your order number is {order_number}.

Best regards,
The {company} Team
"""
    
    # Send a plain text template email
    sender.send_template_email(
        to_emails="customer@example.com",
        subject="Your Order Confirmation",
        template=text_template,
        template_vars={
            "name": "John Doe",
            "product": "Premium Widget",
            "order_number": "ORD-12345",
            "company": "Acme Inc"
        },
        html=False  # This is a plain text template
    )
    
    # HTML template example
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
    
    # Send an HTML template email
    success = sender.send_template_email(
        to_emails="customer@example.com",
        subject="Your HTML Order Confirmation",
        template=html_template,
        template_vars={
            "name": "Jane Smith",
            "product": "Deluxe Widget",
            "order_number": "ORD-67890",
            "company": "Acme Inc"
        },
        html=True  # This is an HTML template
    )
    
    if success:
        print("Template emails sent successfully!")
    else:
        print("Failed to send template emails.")

if __name__ == "__main__":
    main()