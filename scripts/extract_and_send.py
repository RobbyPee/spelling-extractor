# scripts/extract_and_send.py
import argparse
from pathlib import Path
from spelling_extractor.pdf_parser import extract_text_from_pdf
from spelling_extractor.llm_interface import run_phi_and_get_block
from spelling_extractor.google_docs import create_spelling_doc, get_credentials
from spelling_extractor.email_sender import send_doc_via_email


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('pdf_path', help='Path to newsletter PDF')
    parser.add_argument('--to', default='robinp2@gmail.com', help='Recipient email')
    args = parser.parse_args()

    # Extract text and block of spellings
    text = extract_text_from_pdf(args.pdf_path)
    block = run_phi_and_get_block(text)

    pdf_name = Path(args.pdf_path).name

    # Unified credentials for Docs, Drive, and Gmail
    scopes = [
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/gmail.send'
    ]
    creds = get_credentials(scopes, token_file='token.json')

    # Create Google Doc and send via email using the same creds
    doc_id = create_spelling_doc(pdf_name, block, creds)
    send_doc_via_email(doc_id, pdf_name, args.to, creds)

if __name__ == '__main__':
    main()
