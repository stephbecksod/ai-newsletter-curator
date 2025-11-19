#!/usr/bin/env python3
"""
Extract news stories from all newsletters in a date range.
Uses Gmail API with plain text extraction + Claude API for story extraction.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import yaml
from dotenv import load_dotenv
from anthropic import Anthropic

from gmail_text_extractor import GmailTextExtractor

# Load environment variables
load_dotenv()


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_workflow_docs() -> str:
    """Load the workflow document."""
    try:
        with open('docs/Newsletter Copy Creation Workflow.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def extract_stories_from_newsletters(
    newsletters: List[Dict[str, Any]],
    config: Dict[str, Any],
    workflow_doc: str
) -> List[Dict[str, Any]]:
    """
    Extract news stories from newsletter text using Claude API.

    Args:
        newsletters: List of newsletter data with plain text
        config: Configuration dictionary
        workflow_doc: Workflow documentation

    Returns:
        List of extracted news stories
    """
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    all_stories = []

    for i, newsletter in enumerate(newsletters, 1):
        # Handle Unicode in output
        subject = newsletter['subject'][:50].encode('ascii', 'replace').decode('ascii')
        print(f"\n[{i}/{len(newsletters)}] Extracting stories from: {subject}...")
        print(f"  From: {newsletter['from']}")
        print(f"  Date: {newsletter['date']}")
        print(f"  Text length: {len(newsletter['text'])} characters (~{len(newsletter['text']) // 4} tokens)")

        # Skip if no text content
        if not newsletter['text'] or len(newsletter['text']) < 100:
            print("  [SKIP] No meaningful text content")
            continue

        # Create extraction prompt
        system_prompt = f"""You are an AI assistant helping to extract news stories from AI newsletters.

IMPORTANT WORKFLOW REFERENCE:
{workflow_doc}

Your task for Step 1:
1. Read through the newsletter content carefully
2. Identify and extract ONLY actual news stories
3. News includes: new partnerships, products, features, fundraising, valuations, company announcements
4. SKIP: tips, tools, tutorials, prompts, how-to guides, opinion pieces, commentary, ads, sponsored content

For each news story you find, extract:
- headline: Clear, descriptive headline (use newsletter's or write your own)
- source: Newsletter name (use consistent naming)
- date: Newsletter date (YYYY-MM-DD format)
- summary: 1-3 sentence summary of what happened
- url: Link to the full story if provided (null if not available)

Output ONLY valid JSON in this exact format:
{{
  "stories": [
    {{
      "headline": "Story headline here",
      "source": "Newsletter name",
      "date": "YYYY-MM-DD",
      "summary": "Brief summary here",
      "url": "https://example.com or null"
    }}
  ]
}}

This is raw extraction - do NOT deduplicate or rank yet. Extract everything that qualifies as news."""

        # Determine source name from email address
        from_email = newsletter['from'].lower()
        if 'superhuman' in from_email:
            source_name = 'Superhuman'
        elif 'axios' in from_email:
            source_name = 'Axios AI+'
        elif 'techcrunch' in from_email:
            source_name = 'TechCrunch'
        elif 'thatstartupguy' in from_email:
            source_name = 'That Startup Guy'
        elif 'rundown' in from_email:
            source_name = 'The Rundown AI'
        elif 'startupintros' in from_email:
            source_name = 'Startup Intros'
        else:
            source_name = newsletter['from']

        # Parse date
        try:
            # Try to parse the date from the email
            date_str = newsletter['date']
            # This is a simple approximation - you might want to use proper date parsing
            newsletter_date = datetime.strptime(newsletter['date'][:16], '%a, %d %b %Y').strftime('%Y-%m-%d')
        except:
            newsletter_date = datetime.now().strftime('%Y-%m-%d')

        user_prompt = f"""Extract all news stories from this newsletter:

Newsletter: {source_name}
Date: {newsletter_date}
Subject: {newsletter['subject']}

Content:
{newsletter['text']}

Extract all news stories and return them as JSON."""

        try:
            # Call Claude API for extraction
            response = anthropic_client.messages.create(
                model=config['claude']['model'],
                max_tokens=config['claude']['max_tokens'],
                temperature=config['claude']['temperature'],
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Parse response
            response_text = response.content[0].text

            # Extract JSON from response (handle markdown code blocks)
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                # Try to find raw JSON
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(0)
                else:
                    json_text = response_text

            # Parse JSON
            result = json.loads(json_text)
            stories = result.get('stories', [])

            print(f"  [OK] Extracted {len(stories)} stories")
            all_stories.extend(stories)

        except json.JSONDecodeError as e:
            print(f"  [ERROR] Failed to parse JSON response: {e}")
            print(f"  Response preview: {response_text[:200]}...")
            continue
        except Exception as e:
            print(f"  [ERROR] Failed to extract stories: {e}")
            continue

    return all_stories


def main():
    """Main extraction workflow."""
    print("=" * 70)
    print("NEWSLETTER EXTRACTION - Plain Text Approach")
    print("=" * 70)

    # Load configuration
    config = load_config()
    workflow_doc = load_workflow_docs()

    # Initialize Gmail extractor
    print("\n[1] Initializing Gmail text extractor...")
    extractor = GmailTextExtractor()
    extractor.authenticate()

    # Build search query
    start_date = "2025-11-03"
    end_date = "2025-11-10"

    sender_queries = [f"from:{sender}" for sender in config['newsletter_sources']]
    sender_query = " OR ".join(sender_queries)
    query = f"({sender_query}) AND after:{start_date} before:{end_date}"

    # Search for newsletters
    print(f"\n[2] Searching for newsletters from {start_date} to {end_date}...")
    email_list = extractor.search_emails(query, max_results=100)

    print(f"\n[3] Fetching plain text from {len(email_list)} newsletters...")
    newsletters = []
    for i, email in enumerate(email_list, 1):
        try:
            # Handle Unicode in subject line
            subject = email['subject'][:50].encode('ascii', 'replace').decode('ascii')
            print(f"  [{i}/{len(email_list)}] Fetching: {subject}...")
            email_data = extractor.get_email_with_text(email['id'])
            newsletters.append(email_data)
        except Exception as e:
            print(f"  [ERROR] Failed to fetch email: {e}")
            continue

    print(f"\n[OK] Successfully fetched {len(newsletters)} newsletters")

    # Extract stories using Claude API
    print(f"\n[4] Extracting news stories with Claude API...")
    stories = extract_stories_from_newsletters(newsletters, config, workflow_doc)

    print(f"\n[OK] Extracted {len(stories)} total news stories")

    # Save to JSON
    output_file = f"outputs/raw_stories_{start_date}_to_{end_date}_COMPLETE.json"
    output_data = {
        "extraction_date": datetime.now().strftime("%Y-%m-%d"),
        "date_range": {
            "start": start_date,
            "end": end_date
        },
        "newsletters_processed": len(newsletters),
        "total_newsletters_found": len(email_list),
        "stories": stories,
        "notes": "Complete extraction using Gmail API plain text + Claude API. All newsletters processed."
    }

    Path("outputs").mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Saved {len(stories)} stories to: {output_file}")

    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE!")
    print("=" * 70)
    print(f"Newsletters processed: {len(newsletters)}/{len(email_list)}")
    print(f"Stories extracted: {len(stories)}")
    print(f"Output file: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
