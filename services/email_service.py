import os
import logging
import httpx
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@example.com")


class EmailService:
    @staticmethod
    def send_email(subject: str, body: str, recipient: str):
        """Send email via MailerSend API."""
        if not all([MAILERSEND_API_KEY, recipient]):
            error_msg = "Missing MailerSend API key or recipient email"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Attempting to send email to {recipient} via MailerSend")

        url = "https://api.mailersend.com/v1/email"
        headers = {
            "Authorization": f"Bearer {MAILERSEND_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "from": {"email": EMAIL_FROM},
            "to": [{"email": recipient}],
            "subject": subject,
            "text": body,
        }

        try:
            with httpx.Client(timeout=15) as client:
                resp = client.post(url, json=payload, headers=headers)

            if resp.status_code in (200, 202):
                logger.info(f"Email sent successfully to {recipient}")
                return
            else:
                error_detail = resp.text
                logger.error(f"MailerSend API error ({resp.status_code}): {error_detail}")
                raise Exception(f"MailerSend returned {resp.status_code}: {error_detail}")
        except httpx.RequestError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            raise
