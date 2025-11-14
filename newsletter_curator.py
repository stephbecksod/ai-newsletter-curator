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
        - Identifies actual news stories (not tips, tools, tutorials)
        - Extracts headline, source, date, summary, URL
        - Creates raw unranked list

        Args:
            email_data: Email query information

        Returns:
            List of extracted news stories
        """
        print("\n📰 Phase 1: Extracting news stories...")

        # Create prompt for Claude API
        system_prompt = f"""You are an AI assistant helping to extract news stories from newsletters.

Reference the following workflow document:
{self.workflow_docs['workflow']}

Your task is to:
1. Review newsletters from the specified senders and date range
2. Extract ONLY news stories (new partnerships, products, features, fundraising, valuations)
3. Skip tips, tools, tutorials, and opinion content
4. For each story, extract: headline, source, date, summary, URL (if available)

Remember: This is Step 1 from the workflow - raw extraction only, no deduplication or ranking yet."""

        user_prompt = f"""Please extract all news stories from newsletters matching this Gmail query:
{email_data['query']}

Date range: {email_data['start_date']} to {email_data['end_date']}
Sources: {', '.join(email_data['sources'])}

Use the Gmail MCP tools to search and read these emails, then extract all news stories into a structured list.

Output format (JSON):
{{
  "stories": [
    {{
      "headline": "Story headline",
      "source": "Newsletter name",
      "date": "YYYY-MM-DD",
      "summary": "1-3 sentence summary",
      "url": "https://... (if available, otherwise null)"
    }}
  ]
}}"""

        print("Calling Claude API for news extraction...")
        print("(This will use Gmail MCP server to fetch and read emails)")

        # Note: This is a placeholder for the actual API call
        # In a real implementation, this would make the API call with MCP tools
        print("\n⚠️  Implementation Note:")
        print("This phase requires Claude API to have access to Gmail MCP tools.")
        print("Currently in development - manual email processing needed.")

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
