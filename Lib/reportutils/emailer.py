"""emailer.py -- Emailing class.
Author: Garin Wally; 

This class provides a config-driven utility to send emails to a list of addresses.
"""
import tomllib
from pathlib import Path
from email import encoders
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from smtplib import SMTP

AUTHOR_EMAIL = "wallyg@ci.missoula.mt.us"
EMAIL_SERVER = "ci-missoula-mt-us.mail.protection.outlook.com"
EMAIL_PORT = 25


class Emailer():
    """Config-based email controller."""
    def __init__(self, filepath, config_file: str|None = None):
        self.config = {}
        # If a configuration file is provided / suppies email data
        if config_file:
            # The 'filepath' parameter is the path of the Python script file 
            #  using the Emailer utility
            path =  Path(filepath).parent.joinpath(config_file)
            with path.open("rb") as f:
                self.config = tomllib.load(f)
        
        # The constructed email object to be sent
        self.email = None
        # Email data
        self.subject = self.config.get("subject", "")
        self.body = self.config.get("body", "")
        self.to_addrs = self.config.get("to", [])
        self.cc_addrs = self.config.get("cc", [])
        self.bcc_addrs = self.config.get("bcc", [])
        self.importance = self.config.get("importance", False)
        # Only sends emails if debug mode is False
        self.debug = False

    @property
    def to(self):
        """Properly formats the list of to addresses as a comma-seperated string."""
        return ", ".join(self.to_addrs)

    @property
    def cc(self):
        """Properly formats the list of cc addresses as a comma-seperated string."""
        return ", ".join(self.cc_addrs)

    @property
    def bcc(self):
        """Properly formats the list of bcc addresses as a comma-seperated string."""
        return ", ".join(self.bcc_addrs)

    def set_debug(self, debug=True):
        """Sets debug mode."""
        self.debug = debug
        return

    def build(self):
        """Build the email object using the email data as attributes."""
        msg = MIMEMultipart()
        # Body
        msg.attach(MIMEText(self.body))
        # Attrs
        msg["Subject"] = self.subject
        msg["From"] = AUTHOR_EMAIL
        msg["To"] = self.to

        if self.cc:
            msg["CC"] = self.cc
        if self.bcc:
            msg["BCC"] = self.bcc
        
        self.email = msg
        return

    def attach(self, filepath):
        """Attach a document to the email object."""
        # Attachments
        with open(filepath) as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{Path(filepath).name}"'
            )
        self.email.attach(attachment)
        return

    def send(self):
        """Send the email object."""
        if self.debug:
            return False
        s = SMTP(EMAIL_SERVER, EMAIL_PORT)
        s.ehlo()
        s.starttls()
        s.send_message(self.email)
        s.quit()
        return True


class ErrorEmail(Emailer):
    def __init__(self, script, logfile_to_attach):
        """An email object pre-configured to send to the author/programmer."""
        super().__init__()
        self.to_addrs = [AUTHOR_EMAIL]
        self.subject = f"Failed Script: {script}"
        self.body = f"Script failure:\n    {script}\nSee attached log"
        
        self.build()
        self.attach(logfile_to_attach)
