# google_docs.py
# Module to create a formatted Google Doc containing the spelling block
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'gdocs_token.json'


def get_credentials(scopes, token_file=TOKEN_FILE, cred_file=CREDENTIALS_FILE):
    """
    Obtain OAuth2 credentials via local server flow.
    """
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import os, pickle

    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as t:
            creds = pickle.load(t)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, scopes)
            creds = flow.run_local_server(port=12083)
        with open(token_file, 'wb') as t:
            pickle.dump(creds, t)
    return creds


def create_spelling_doc(pdf_name: str, block_text: str, creds=None) -> str:
    """
    Creates a Google Doc titled after the PDF filename, inserts the block_text,
    applies 34pt font, centers title (first line). Returns the document ID.
    """
    creds = get_credentials(SCOPES)
    docs = build('docs', 'v1', credentials=creds)

    # Create new document
    title = f"Spelling List - {pdf_name}"
    doc = docs.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    # Prepare lines, skipping any blank lines
    raw_lines = block_text.splitlines()
    lines = [line for line in raw_lines if line.strip()]

    requests = []
    index = 1  # initial index into document body

    for i, line in enumerate(lines):
        length = len(line)
        # Insert text line
        requests.append({
            'insertText': {
                'location': {'index': index},
                'text': line + ' '
            }
        })
        # Only style non-empty ranges
        if length > 0:
            # Set 34pt font
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': index, 'endIndex': index + length},
                    'textStyle': {'fontSize': {'magnitude': 34, 'unit': 'PT'}},
                    'fields': 'fontSize'
                }
            })
            # Center the first line (title line of block)
            if i == 0:
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': index, 'endIndex': index + length},
                        'paragraphStyle': {'alignment': 'CENTER'},
                        'fields': 'alignment'
                    }
                })
        # Move index past this line and newline
        index += length + 1

    # Execute all requests
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return doc_id