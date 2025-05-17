# email_sender.py
# Module to export the Google Doc to PDF and send via Gmail API
import base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from googleapiclient.discovery import build

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_doc_via_email(doc_id: str, pdf_name: str, recipient: str, creds):
    gmail = build('gmail', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)

    # export to PDF
    pdf_data = drive.files().export(fileId=doc_id, mimeType='application/pdf').execute()

    # build message
    msg = MIMEMultipart()
    msg['to'] = recipient
    msg['subject'] = 'Weekly Spelling List'
    msg.attach(MIMEText('Please find attached the spelling list for next week.', 'plain'))

    part = MIMEBase('application', 'pdf')
    part.set_payload(pdf_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{pdf_name}.pdf"')
    msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gmail.users().messages().send(userId='me', body={'raw': raw}).execute()
