# Gmail API Setup Guide

This guide walks you through setting up Gmail API access for plain text extraction.

## ⚡ Quick Start: Reusing MCP Credentials (RECOMMENDED)

**If you already have the Gmail MCP server configured, you're done!**

The `gmail_text_extractor.py` script automatically reuses the OAuth credentials from your MCP setup:
- **MCP credentials location:** `C:\Users\steph\.gmail-mcp\gmail-token.json`
- **No additional setup required** - the Python script loads these credentials automatically
- **Test it:** Run `python gmail_text_extractor.py` to verify

---

## Why This Approach?

The Gmail MCP server returns full HTML content with images and formatting, which exceeds token limits for large newsletters (28K+ tokens). By using the Gmail API directly with HTML-to-text conversion, we can extract **only the plain text** content, reducing token usage by ~92% (from 28K to 2K tokens).

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Newsletter Curator" (or any name)
4. Click "Create"

### 2. Enable Gmail API

1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and click "Enable"

### 3. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: "Newsletter Curator"
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Leave default (we'll set in code)
   - Test users: Add your Gmail address
   - Click "Save and Continue" through remaining screens

4. Create OAuth Client ID:
   - Application type: **Desktop app**
   - Name: "Newsletter Curator Desktop"
   - Click "Create"

5. Download credentials:
   - Click the download icon (⬇) next to your newly created OAuth client
   - Save as `credentials.json` in this project directory

### 4. First Run Authentication

When you first run the script:
1. A browser window will open
2. Sign in with your Gmail account
3. Click "Continue" on the warning screen (app not verified - this is normal for personal projects)
4. Grant read-only access to Gmail
5. Credentials will be saved to `.gmail_credentials/token.pickle`

Future runs will use the saved token automatically.

## Security Notes

- `credentials.json` contains your OAuth client secrets (safe to store, but don't share publicly)
- `.gmail_credentials/token.pickle` contains your access token (gitignored, keep private)
- The app only requests **read-only** access to Gmail
- You can revoke access anytime at [Google Account Security](https://myaccount.google.com/permissions)

## Testing

Run the test script to verify setup:

```bash
python gmail_text_extractor.py
```

This will:
- Authenticate with Gmail
- Fetch one Axios AI+ email from Nov 10
- Extract plain text only
- Show character count and estimated token usage

## Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the project root directory
- Re-download from Google Cloud Console if needed

### "Access blocked: This app's request is invalid"
- Make sure you added your Gmail address to "Test users" in OAuth consent screen
- Try creating a new OAuth client ID

### "Token has been expired or revoked"
- Delete `.gmail_credentials/token.pickle`
- Re-run the script to re-authenticate

## Confirmed Token Reduction

**Before (MCP with HTML):**
- Axios AI+ Nov 10: **28,111 tokens** ❌ (exceeds 25K limit)

**After (Plain text from HTML conversion):**
- Axios AI+ Nov 10: **~2,187 tokens** ✅ (92% reduction!)
- 40 newsletters/week: **~87,480 tokens** (well within 200K budget)

This approach makes weekly processing fully sustainable.
