"""
Core module for the emailer package.

This module provides the EmailSender class which handles the email sending functionality.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Optional, Dict, Union


class EmailSender:
    """
    A class to handle email sending functionality.
    
    This class provides methods to send emails with plain text or HTML content,
    attachments, and supports various email providers.
    """
    
    def __init__(self, email: str, password: str, smtp_server: str = "smtp.gmail.com", 
                 smtp_port: int = 587):
        """
        Initialize the EmailSender with email credentials and SMTP settings.
        
        Args:
            email: The sender's email address
            password: The password or app password for the email account
            smtp_server: The SMTP server address (default: smtp.gmail.com)
            smtp_port: The SMTP server port (default: 587)
        """
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    
    def send_email(self, to_emails: Union[str, List[str]], subject: str, 
                  body: str, html: bool = False, attachments: Optional[List[str]] = None,
                  cc: Optional[Union[str, List[str]]] = None, 
                  bcc: Optional[Union[str, List[str]]] = None) -> bool:
        """
        Send an email with the given parameters.
        
        Args:
            to_emails: Recipient email address(es)
            subject: Email subject
            body: Email body content
            html: Whether the body is HTML (default: False)
            attachments: List of file paths to attach (default: None)
            cc: Carbon copy recipient(s) (default: None)
            bcc: Blind carbon copy recipient(s) (default: None)
            
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        # Convert single email to list
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # Add CC if provided
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            msg['Cc'] = ', '.join(cc)
            to_emails.extend(cc)
        
        # Add BCC if provided
        if bcc:
            if isinstance(bcc, str):
                bcc = [bcc]
            to_emails.extend(bcc)
        
        # Attach body
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Attach files if any
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                    
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)
        
        # Send email
        try:
            context = ssl.create_default_context()
            # Use SSL directly for implicit SSL ports (commonly 465), otherwise STARTTLS
            if int(self.smtp_port) == 465:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.email, self.password)
                    server.sendmail(self.email, to_emails, msg.as_string())
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(self.email, self.password)
                    server.sendmail(self.email, to_emails, msg.as_string())
            return True
        except smtplib.SMTPAuthenticationError as e:
            print("Error sending email: Authentication failed. Please verify email/password or app-specific password.")
            print(f"SMTPAuthenticationError: {e}")
            return False
        except smtplib.SMTPServerDisconnected as e:
            print("Error sending email: Connection unexpectedly closed by the server. This often happens when using STARTTLS on port 465. Try port 465 with SSL or port 587 with STARTTLS.")
            print(f"SMTPServerDisconnected: {e}")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_html_email(self, to_emails: Union[str, List[str]], subject: str, 
                       html_body: str, attachments: Optional[List[str]] = None,
                       cc: Optional[Union[str, List[str]]] = None, 
                       bcc: Optional[Union[str, List[str]]] = None) -> bool:
        """
        Send an HTML email.
        
        This is a convenience method that calls send_email with html=True.
        
        Args:
            to_emails: Recipient email address(es)
            subject: Email subject
            html_body: HTML content for the email body
            attachments: List of file paths to attach (default: None)
            cc: Carbon copy recipient(s) (default: None)
            bcc: Blind carbon copy recipient(s) (default: None)
            
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        return self.send_email(to_emails, subject, html_body, html=True, 
                              attachments=attachments, cc=cc, bcc=bcc)
    
    def send_template_email(self, to_emails: Union[str, List[str]], subject: str, 
                           template: str, template_vars: Dict[str, str],
                           html: bool = True, attachments: Optional[List[str]] = None,
                           cc: Optional[Union[str, List[str]]] = None, 
                           bcc: Optional[Union[str, List[str]]] = None) -> bool:
        """
        Send an email using a template with variable substitution.
        
        Args:
            to_emails: Recipient email address(es)
            subject: Email subject
            template: Email template string with placeholders like {variable_name}
            template_vars: Dictionary of variables to substitute in the template
            html: Whether the template is HTML (default: True)
            attachments: List of file paths to attach (default: None)
            cc: Carbon copy recipient(s) (default: None)
            bcc: Blind carbon copy recipient(s) (default: None)
            
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        # Substitute variables in the template
        body = template
        for var_name, var_value in template_vars.items():
            body = body.replace(f"{{{var_name}}}", var_value)
        
        return self.send_email(to_emails, subject, body, html=html, 
                              attachments=attachments, cc=cc, bcc=bcc)