#!/usr/bin/env python3
"""
AI Newsletter Curator
Processes weekly AI newsletters from Gmail, extracts news, deduplicates, ranks, and formats.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import yaml
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()


class NewsletterCurator:
    """Main orchestrator for newsletter curation workflow."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the curator with configuration."""
        self.config = self._load_config(config_path)
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.workflow_docs = self._load_workflow_docs()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_workflow_docs(self) -> Dict[str, str]:
        """Load reference documents for workflow."""
        docs = {}
        doc_files = {
            'workflow': 'docs/Newsletter Copy Creation Workflow.md',
            'style_guide': 'docs/Newsletter Style Guide.md',
            'examples': 'docs/Newsletter Stories Example.md'
        }

        for key, path in doc_files.items():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    docs[key] = f.read()
            except FileNotFoundError:
                print(f"Warning: Could not find {path}")
                docs[key] = ""

        return docs

    def fetch_newsletters(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Fetch newsletters from Gmail using MCP.

        Note: This requires the Gmail MCP server to be running and authenticated.
        In the current implementation, this method prepares the query but actual
        MCP communication happens through Claude API calls.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of email data dictionaries
        """
        print(f"\n📧 Fetching newsletters from {start_date} to {end_date}...")

        # Build Gmail search query for all configured senders
        sender_queries = [f"from:{sender}" for sender in self.config['newsletter_sources']]
        sender_query = " OR ".join(sender_queries)
        date_query = f"after:{start_date} before:{end_date}"
        full_query = f"({sender_query}) AND {date_query}"

        print(f"Gmail query: {full_query}")
        print("\nNote: Email fetching will use Gmail MCP server through Claude API")
        print("This requires Claude Code to be running with MCP configured.")

        # Return query info that will be used in Claude API calls
        return {
            'query': full_query,
            'start_date': start_date,
            'end_date': end_date,
            'sources': self.config['newsletter_sources']
        }

    def extract_news_stories(self, email_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Phase 1: Extract news stories from newsletters using Claude API.

        This phase:
        1. Fetches newsletters from Gmail using MCP
        2. Extracts entire newsletter content
        3. Identifies actual news stories (not tips, tools, tutorials)
        4. Extracts headline, source, date, summary, URL
        5. Creates raw unranked list

        Args:
            email_data: Email query information

        Returns:
            List of extracted news stories
        """
        print("\n📰 Phase 1: Extracting news stories...")
        print(f"Searching Gmail for newsletters...")
        print(f"Query: {email_data['query']}")

        # Step 1: Search for newsletters using Gmail MCP
        try:
            # Import Gmail MCP tools at runtime
            from mcp__gmail__search_emails import mcp__gmail__search_emails
            from mcp__gmail__read_email import mcp__gmail__read_email

            # Search for all newsletters in date range
            search_results = mcp__gmail__search_emails(
                query=email_data['query'],
                maxResults=100  # Get up to 100 newsletters
            )

            if not search_results or len(search_results) == 0:
                print("⚠️  No newsletters found for the specified date range.")
                return []

            print(f"✓ Found {len(search_results)} newsletters")

            # Step 2: Read each newsletter and collect full content
            newsletters = []
            for i, email_summary in enumerate(search_results, 1):
                print(f"Reading newsletter {i}/{len(search_results)}: {email_summary.get('Subject', 'No subject')}")

                email_content = mcp__gmail__read_email(messageId=email_summary['ID'])
                newsletters.append({
                    'id': email_summary['ID'],
                    'subject': email_summary.get('Subject', ''),
                    'from': email_summary.get('From', ''),
                    'date': email_summary.get('Date', ''),
                    'content': email_content
                })

        except ImportError:
            print("\n⚠️  Gmail MCP tools not available in Python runtime.")
            print("Note: This implementation expects to run within Claude Code environment")
            print("with MCP tools available. Returning empty list for now.")
            return []
        except Exception as e:
            print(f"\n❌ Error fetching newsletters: {e}")
            return []

        # Step 3: Use Claude API to extract news stories from all newsletters
        print(f"\n🤖 Analyzing {len(newsletters)} newsletters with Claude API...")

        # Prepare newsletter content for Claude
        newsletters_text = ""
        for nl in newsletters:
            newsletters_text += f"\n\n--- Newsletter from {nl['from']} ---\n"
            newsletters_text += f"Date: {nl['date']}\n"
            newsletters_text += f"Subject: {nl['subject']}\n"
            newsletters_text += f"Content:\n{nl['content']}\n"
            newsletters_text += "--- End Newsletter ---\n"

        # Create extraction prompt
        system_prompt = f"""You are an AI assistant helping to extract news stories from AI newsletters.

IMPORTANT WORKFLOW REFERENCE:
{self.workflow_docs['workflow']}

Your task for Step 1:
1. Read through ALL the newsletter content carefully
2. Identify and extract ONLY actual news stories
3. News includes: new partnerships, products, features, fundraising, valuations, company announcements
4. SKIP: tips, tools, tutorials, prompts, how-to guides, opinion pieces, commentary

For each news story you find, extract:
- headline: Clear, descriptive headline (use newsletter's or write your own)
- source: Newsletter name (use consistent naming: "Superhuman", "Axios AI+", "TechCrunch", "That Startup Guy", "The Rundown AI", "Startup Intros")
- date: Email received date (YYYY-MM-DD format)
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

        user_prompt = f"""Extract all news stories from these newsletters:

Date range: {email_data['start_date']} to {email_data['end_date']}
Newsletter sources: {', '.join(email_data['sources'])}

Here are the newsletters:
{newsletters_text}

Extract all news stories and return them as JSON."""

        try:
            # Call Claude API for extraction
            response = self.anthropic_client.messages.create(
                model=self.config['claude']['model'],
                max_tokens=self.config['claude']['max_tokens'],
                temperature=self.config['claude']['temperature'],
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

            print(f"✓ Extracted {len(stories)} news stories")

            return stories

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print(f"Response text: {response_text[:500]}...")
            return []
        except Exception as e:
            print(f"❌ Error calling Claude API: {e}")
            return []

    def deduplicate_and_rank(self, stories: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Phase 2: Deduplicate overlapping stories and rank by importance.

        This phase:
        - Groups duplicate stories across newsletters
        - Tags launches
        - Ranks by importance criteria
        - Categorizes into Top 5, Secondary, Launches, Other

        Args:
            stories: Raw list of news stories

        Returns:
            Categorized and ranked stories
        """
        print("\n🔄 Phase 2: Deduplicating and ranking stories...")

        # Implementation will use Claude API with workflow guidance
        return {
            'top_stories': [],
            'secondary_stories': [],
            'launches': [],
            'other': []
        }

    def research_top_stories(self, top_stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Phase 3: Research top 5 stories for better context.

        This phase:
        - Reviews newsletter content and URLs
        - Does web search for 1-2 additional articles
        - Updates summaries with critical insights

        Args:
            top_stories: Top 5 ranked stories

        Returns:
            Enhanced stories with research
        """
        print("\n🔬 Phase 3: Researching top 5 stories...")

        # Implementation will use Claude API with web search
        return top_stories

    def format_output(self, categorized_stories: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Phase 4: Format stories according to style guide.

        This phase:
        - Formats Top 5 with headline, summary, why it matters
        - Formats Secondary with emoji + headline + summary
        - Formats Launches as bullet list

        Args:
            categorized_stories: Categorized story dictionary

        Returns:
            Fully formatted markdown copy
        """
        print("\n✍️  Phase 4: Formatting final output...")

        system_prompt = f"""You are an AI assistant formatting newsletter copy.

Reference documents:
WORKFLOW: {self.workflow_docs['workflow']}
STYLE GUIDE: {self.workflow_docs['style_guide']}
EXAMPLES: {self.workflow_docs['examples']}

Your task is to format the provided stories following the exact style guide specifications."""

        # Implementation will use Claude API with style guide
        return "# Newsletter Copy\n\n(Formatted output will appear here)"

    def save_output(self, content: str, start_date: str, end_date: str) -> str:
        """
        Save formatted newsletter to output file.

        Args:
            content: Formatted newsletter content
            start_date: Start date string
            end_date: End date string

        Returns:
            Path to saved file
        """
        output_dir = Path(self.config['output']['directory'])
        output_dir.mkdir(exist_ok=True)

        filename = self.config['output']['filename_format'].format(
            start_date=start_date,
            end_date=end_date
        )
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ Newsletter saved to: {output_path}")
        return str(output_path)

    def run(self, start_date: str, end_date: str) -> str:
        """
        Run the complete newsletter curation workflow.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Path to generated newsletter file
        """
        print("=" * 60)
        print("AI NEWSLETTER CURATOR")
        print("=" * 60)
        print(f"Date range: {start_date} to {end_date}")
        print(f"Sources: {len(self.config['newsletter_sources'])} newsletters")
        print("=" * 60)

        # Phase 1: Fetch newsletters from Gmail
        email_data = self.fetch_newsletters(start_date, end_date)

        # Phase 2: Extract news stories
        stories = self.extract_news_stories(email_data)

        if not stories:
            print("\n⚠️  No stories extracted. Please check Gmail MCP configuration.")
            print("See README.md for setup instructions.")
            return None

        print(f"✓ Extracted {len(stories)} news stories")

        # Phase 3: Deduplicate and rank
        categorized = self.deduplicate_and_rank(stories)

        print(f"✓ Categorized stories:")
        print(f"  - Top stories: {len(categorized['top_stories'])}")
        print(f"  - Secondary: {len(categorized['secondary_stories'])}")
        print(f"  - Launches: {len(categorized['launches'])}")
        print(f"  - Other: {len(categorized['other'])}")

        # Phase 4: Research top stories
        categorized['top_stories'] = self.research_top_stories(categorized['top_stories'])

        # Phase 5: Format output
        formatted_content = self.format_output(categorized)

        # Phase 6: Save to file
        output_path = self.save_output(formatted_content, start_date, end_date)

        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETE!")
        print("=" * 60)

        return output_path


def validate_date(date_string: str) -> str:
    """Validate date format YYYY-MM-DD."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")


def main():
    """Main entry point for the newsletter curator."""
    parser = argparse.ArgumentParser(
        description="AI Newsletter Curator - Process and format weekly AI newsletters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python newsletter_curator.py --start 2025-11-04 --end 2025-11-10
  python newsletter_curator.py --start 2025-11-04 --end 2025-11-10 --config custom_config.yaml

For more information, see README.md
        """
    )

    parser.add_argument(
        '--start',
        required=True,
        type=validate_date,
        help='Start date in YYYY-MM-DD format'
    )

    parser.add_argument(
        '--end',
        required=True,
        type=validate_date,
        help='End date in YYYY-MM-DD format'
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    args = parser.parse_args()

    # Validate API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please create .env file with your API key (see .env.example)")
        sys.exit(1)

    # Create curator and run workflow
    try:
        curator = NewsletterCurator(config_path=args.config)
        output_path = curator.run(args.start, args.end)

        if output_path:
            print(f"\n📄 Newsletter ready: {output_path}")
            sys.exit(0)
        else:
            print("\n❌ Newsletter generation failed")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: Configuration file not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
