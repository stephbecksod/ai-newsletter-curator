#!/usr/bin/env python3
"""
Gmail Plain Text Extractor
Fetches emails from Gmail and extracts only the plain text content (no HTML, images, or formatting).
"""

import base64
import os
import pickle
from pathlib import Path
from typing import Dict, List, Optional
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

try:
    from bs4 import BeautifulSoup
    HTML_PARSING_AVAILABLE = True
except ImportError:
    HTML_PARSING_AVAILABLE = False


# Gmail API scopes - read-only access to Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailTextExtractor:
    """Extract plain text from Gmail messages."""

    def __init__(self, credentials_dir: str = ".gmail_credentials", use_mcp_token: bool = True):
        """
        Initialize the Gmail text extractor.

        Args:
            credentials_dir: Directory to store OAuth credentials
            use_mcp_token: If True, try to reuse MCP server OAuth token
        """
        self.credentials_dir = Path(credentials_dir)
        self.credentials_dir.mkdir(exist_ok=True)
        self.use_mcp_token = use_mcp_token
        self.service = None

    def authenticate(self, credentials_file: str = "credentials.json"):
        """
        Authenticate with Gmail API using OAuth 2.0.

        Tries to reuse MCP server token first, then falls back to standard OAuth.

        Args:
            credentials_file: Path to OAuth client credentials JSON file
        """
        creds = None

        # Try to load MCP token first
        if self.use_mcp_token:
            mcp_token_path = Path.home() / ".gmail-mcp" / "gmail-token.json"
            if mcp_token_path.exists():
                try:
                    import json
                    with open(mcp_token_path, 'r') as f:
                        token_data = json.load(f)

                    # Create credentials from MCP token
                    creds = Credentials(
                        token=token_data.get('token'),
                        refresh_token=token_data.get('refresh_token'),
                        token_uri=token_data.get('token_uri'),
                        client_id=token_data.get('client_id'),
                        client_secret=token_data.get('client_secret'),
                        scopes=token_data.get('scopes')
                    )
                    print("[OK] Loaded credentials from MCP server token")
                except Exception as e:
                    print(f"[WARNING] Could not load MCP token: {e}")
                    print("Falling back to standard OAuth flow...")
                    creds = None

        # Fall back to standard token path
        if not creds:
            token_path = self.credentials_dir / "token.pickle"
            if token_path.exists():
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                print("Refreshing expired token...")
                creds.refresh(Request())
            else:
                # New authentication flow
                if not os.path.exists(credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {credentials_file}\n"
                        "Please download OAuth credentials from Google Cloud Console.\n"
                        "See GMAIL_API_SETUP.md for setup instructions."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save token for future use
            token_path = self.credentials_dir / "token.pickle"
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
        print("[OK] Authenticated with Gmail API")

    def search_emails(self, query: str, max_results: int = 100) -> List[Dict]:
        """
        Search for emails matching a query.

        Args:
            query: Gmail search query (e.g., "from:sender@example.com after:2025-11-01")
            max_results: Maximum number of results to return

        Returns:
            List of email metadata dictionaries
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        print(f"Searching Gmail: {query}")

        results = []
        page_token = None

        while len(results) < max_results:
            # Search for messages
            response = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=min(100, max_results - len(results)),
                pageToken=page_token
            ).execute()

            messages = response.get('messages', [])
            if not messages:
                break

            # Get metadata for each message
            for msg in messages:
                metadata = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()

                # Extract headers
                headers = {h['name']: h['value'] for h in metadata.get('payload', {}).get('headers', [])}

                results.append({
                    'id': msg['id'],
                    'from': headers.get('From', ''),
                    'subject': headers.get('Subject', ''),
                    'date': headers.get('Date', '')
                })

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        print(f"[OK] Found {len(results)} emails")
        return results

    def get_plain_text(self, message_id: str) -> str:
        """
        Extract plain text content from an email message.

        This extracts only the text/plain MIME part, ignoring HTML, images, and formatting.

        Args:
            message_id: Gmail message ID

        Returns:
            Plain text content of the email
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        # Fetch the full message
        message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        # Extract plain text from MIME parts
        plain_text = self._extract_text_from_payload(message.get('payload', {}))

        return plain_text

    def _extract_text_from_payload(self, payload: Dict) -> str:
        """
        Recursively extract text content from email payload.
        Tries text/plain first, falls back to converting HTML to text.

        Args:
            payload: Email payload from Gmail API

        Returns:
            Plain text content
        """
        text_parts = []
        html_parts = []

        # Check if this part is text/plain or text/html
        mime_type = payload.get('mimeType', '')

        if mime_type == 'text/plain':
            # This is plain text - decode it
            body_data = payload.get('body', {}).get('data', '')
            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                text_parts.append(decoded)

        elif mime_type == 'text/html':
            # This is HTML - save for later conversion if no plain text found
            body_data = payload.get('body', {}).get('data', '')
            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                html_parts.append(decoded)

        elif mime_type.startswith('multipart/'):
            # This is a multipart message - check all parts
            parts = payload.get('parts', [])
            for part in parts:
                # Recursively extract from each part
                part_text, part_html = self._extract_text_and_html_from_payload(part)
                if part_text:
                    if isinstance(part_text, list):
                        text_parts.extend(part_text)
                    else:
                        text_parts.append(part_text)
                if part_html:
                    if isinstance(part_html, list):
                        html_parts.extend(part_html)
                    else:
                        html_parts.append(part_html)

        # If we found plain text, use it
        if text_parts:
            return '\n\n'.join(text_parts)

        # Otherwise, convert HTML to text
        if html_parts and HTML_PARSING_AVAILABLE:
            converted_text = []
            for html in html_parts:
                text = self._html_to_text(html)
                if text:
                    converted_text.append(text)
            return '\n\n'.join(converted_text)

        return '\n\n'.join(text_parts)

    def _extract_text_and_html_from_payload(self, payload: Dict) -> tuple:
        """Helper method that returns both text and HTML parts."""
        text_parts = []
        html_parts = []

        mime_type = payload.get('mimeType', '')

        if mime_type == 'text/plain':
            body_data = payload.get('body', {}).get('data', '')
            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                text_parts.append(decoded)

        elif mime_type == 'text/html':
            body_data = payload.get('body', {}).get('data', '')
            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                html_parts.append(decoded)

        elif mime_type.startswith('multipart/'):
            parts = payload.get('parts', [])
            for part in parts:
                part_text, part_html = self._extract_text_and_html_from_payload(part)
                text_parts.extend(part_text) if isinstance(part_text, list) else text_parts.append(part_text) if part_text else None
                html_parts.extend(part_html) if isinstance(part_html, list) else html_parts.append(part_html) if part_html else None

        return (text_parts, html_parts)

    def _html_to_text(self, html: str) -> str:
        """
        Convert HTML to plain text, removing formatting but keeping content.

        Args:
            html: HTML content

        Returns:
            Plain text version
        """
        if not HTML_PARSING_AVAILABLE:
            # Fallback: simple regex-based HTML stripping
            text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

        # Use BeautifulSoup for better HTML parsing
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for element in soup(['script', 'style', 'head', 'meta', 'link']):
            element.decompose()

        # Get text
        text = soup.get_text(separator='\n')

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]  # Remove empty lines
        text = '\n'.join(lines)

        return text

    def get_email_with_text(self, message_id: str) -> Dict:
        """
        Get email metadata and plain text content.

        Args:
            message_id: Gmail message ID

        Returns:
            Dictionary with email metadata and plain text content
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        # Get metadata
        metadata = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()

        # Extract headers
        headers = {h['name']: h['value'] for h in metadata.get('payload', {}).get('headers', [])}

        # Get plain text content
        plain_text = self.get_plain_text(message_id)

        return {
            'id': message_id,
            'from': headers.get('From', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'text': plain_text
        }


def main():
    """Test the Gmail text extractor."""
    extractor = GmailTextExtractor()

    # Authenticate
    extractor.authenticate()

    # Search for one Axios AI+ email
    results = extractor.search_emails(
        query="from:ai.plus@axios.com after:2025-11-09 before:2025-11-11",
        max_results=1
    )

    if results:
        email = results[0]
        # Handle Unicode characters in email subject
        subject = email['subject'].encode('ascii', 'replace').decode('ascii')
        print(f"\nFetching email: {subject}")
        print(f"From: {email['from']}")
        print(f"Date: {email['date']}")

        # Get plain text
        email_data = extractor.get_email_with_text(email['id'])
        plain_text = email_data['text']

        print(f"\n[OK] Extracted plain text: {len(plain_text)} characters")
        print(f"Estimated tokens: ~{len(plain_text) // 4}")
        print("\n--- First 500 characters ---")
        print(plain_text[:500])
        print("...")
    else:
        print("No emails found")


if __name__ == "__main__":
    main()
