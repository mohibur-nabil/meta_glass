import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime
import re

class EmailCodeExtractor:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.imap_server = "imap.gmail.com"

    def get_latest_code(self, domain, folder="INBOX"):
        """
        Get the latest verification code from emails matching the specified domain.
        
        Args:
            domain (str): Email domain to search for
            folder (str): Email folder to search in (default: "INBOX")
            
        Returns:
            str: Latest verification code or None if not found
        """
        imap = imaplib.IMAP4_SSL(self.imap_server)
        
        try:
            # Login
            imap.login(self.email_address, self.password)
            
            # Select the mailbox/folder
            imap.select(folder)
            
            # Search for all emails
            _, message_numbers = imap.search(None, "ALL")
            
            # Store only the latest matching email
            latest_email = None
            latest_date = None
            
            for num in message_numbers[0].split():
                _, msg_data = imap.fetch(num, "(RFC822)")
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                from_header = email_message["From"]
                if domain.lower() in from_header.lower():
                    date_str = email_message["Date"]
                    email_date = datetime.strptime(date_str.split(' +')[0].strip(), '%a, %d %b %Y %H:%M:%S')
                    
                    if latest_date is None or email_date > latest_date:
                        body = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = email_message.get_payload(decode=True).decode()

                        code = None
                        if body:
                            code_match = re.search(r'Your unique code:\s*(\d{6})', body)
                            if code_match:
                                code = code_match.group(1)

                        latest_date = email_date
                        latest_email = {
                            "from": self.email_address,
                            "subject": email_message["Subject"],
                            "date": date_str,
                            "body": body,
                            "verification_code": code
                        }
            
            return latest_email["verification_code"] if latest_email else None
        
        finally:
            try:
                imap.logout()
            except:
                print("Error logging out from IMAP server")

# Example usage (only runs if script is run directly)
if __name__ == "__main__":
    EMAIL = "pimeyestest2@gmail.com"
    PASSWORD = "yovm pnrs iesm xrid"
    DOMAIN = "no-reply@mg.pimeyes.com"
    
    extractor = EmailCodeExtractor(EMAIL, PASSWORD)
    code = extractor.get_latest_code(DOMAIN)
    
    print(f"Latest verification code: {code}")