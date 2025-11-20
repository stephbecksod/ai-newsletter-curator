#!/usr/bin/env python3
"""
Deduplicate and rank news stories from extracted newsletters.
Uses Claude API to group overlapping stories, tag launches, and rank by importance.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import yaml
from dotenv import load_dotenv
from anthropic import Anthropic

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


def load_style_guide() -> str:
    """Load the style guide document."""
    try:
        with open('docs/Newsletter Style Guide.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def load_example_stories() -> str:
    """Load the example stories document."""
    try:
        with open('docs/Newsletter Stories Example.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def deduplicate_and_rank_stories(
    raw_stories: List[Dict[str, Any]],
    config: Dict[str, Any],
    workflow_doc: str,
    style_guide: str,
    example_stories: str
) -> Dict[str, Any]:
    """
    Deduplicate, tag launches, and rank stories using Claude API.

    Args:
        raw_stories: List of raw extracted stories
        config: Configuration dictionary
        workflow_doc: Workflow documentation
        style_guide: Style guide documentation
        example_stories: Example stories for reference

    Returns:
        Dictionary with categorized and ranked stories
    """
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    print(f"\n{'='*70}")
    print(f"STEP 2: DEDUPLICATION & RANKING")
    print(f"{'='*70}")
    print(f"\nProcessing {len(raw_stories)} raw stories...")

    # Create system prompt with workflow context
    major_companies = ", ".join(config['major_ai_companies'])

    system_prompt = f"""You are an AI assistant helping to deduplicate and rank news stories for a weekly AI newsletter.

WORKFLOW REFERENCE:
{workflow_doc}

STYLE GUIDE REFERENCE:
{style_guide}

EXAMPLE STORIES FOR REFERENCE:
{example_stories}

Your task is Step 2: Deduplication & Ranking.

You will receive {len(raw_stories)} raw news stories extracted from newsletters. You must:

1. DEDUPLICATE:
   - Group overlapping stories that report on the same underlying event
   - When merging duplicates, keep:
     * Combined list of sources
     * Count of how many newsletters mentioned it
     * Whether it was a headline in any newsletter
     * A clean final headline
     * A unified summary (combining best information from all sources)
     * All URLs from different sources
     * The earliest date among the duplicates

2. TAG LAUNCHES:
   - Mark each story as "is_launch: true" if it's a launch (new model, company, product, feature, integration, partnership)
   - Keywords: launch, release, announce, unveil, introduce, debut, roll out, new model/product/feature/integration/partnership

3. RANK STORIES:
   Use a WEIGHTED, EDITORIAL APPROACH that prioritizes strategic significance over mechanical metrics.

   PRIMARY RANKING CRITERIA (in priority order):
   a) "Why it matters" strength - Does this signal something bigger about AI's future, platform power, market structure, or societal impact?
   b) Story type weighting - Apply category-specific priorities (see below)
   c) Multiple newsletter mentions - 2+ for high-priority types, 3+ for others
   d) Headline appearance - Was it featured as a headline?
   e) Major AI company involvement: {major_companies} - But not sufficient alone for top ranking

   STORY TYPE PRIORITIES:

   HIGH-PRIORITY (boost ranking even with fewer mentions):
   - Platform/ecosystem battles (e.g., Amazon blocking Perplexity, API restrictions)
   - Controversy & safety (model removals, lawsuits, ethical concerns, regulatory action)
   - Strategic moonshots (long-term visions like space data centers, AGI timelines, research breakthroughs)
   - Market structure changes (new business models, pricing disruptions, competitive shifts)

   MEDIUM-PRIORITY (standard newsworthiness):
   - Major product launches (significant new capabilities from leading companies)
   - Funding & valuations ($100M+ rounds or notable valuations)
   - Enterprise adoption (major companies adopting AI transformatively)

   LOWER-PRIORITY (require more mentions):
   - Infrastructure capex (pure GPU/datacenter/cloud spending - unless strategic shifts)
   - Corporate governance (exec comp, board changes - unless AI-related)
   - Incremental updates (evolutionary features, not revolutionary)

   SPECIAL RULES:
   - CONTROVERSY BOOST: Stories with controversy, lawsuits, safety concerns, model removals, or regulatory action get +1-2 ranking tiers automatically
   - LAUNCH vs NEWS: Research projects/long-term visions (like Project Suncatcher) are NEWS, not launches. Launches = products available now or within 3 months
   - INFRASTRUCTURE CONTEXT: Large deals ($25B+) should be secondary unless they signal strategic shifts (e.g., diversification). Dollar amount alone ≠ newsworthy

4. CATEGORIZE:
   NEWS STORIES (Top 20):
   - Top 5 stories (most important)
   - Secondary 5 stories (next 5 highest-ranked)
   - Next 10 stories (ranked 11-20, for human review)

   LAUNCHES (Top 20):
   - Top 20 launches ranked using the SAME weighted approach as news stories
   - Apply same ranking criteria: strategic significance, mention count, major companies
   - Focus on launches with most significant impact on AI ecosystem
   - Include why_it_matters for each

   OTHER:
   - Remaining launches (not in top 20)
   - Other stories (everything else - just count, no details)

OUTPUT FORMAT (JSON):
{{
  "top_stories": [
    {{
      "headline": "Clean, compelling headline",
      "summary": "2-3 sentence summary of what happened",
      "why_it_matters": "One sentence explaining the strategic significance",
      "sources": ["Newsletter 1", "Newsletter 2"],
      "mention_count": 2,
      "was_headline": true,
      "date": "YYYY-MM-DD",
      "urls": ["url1", "url2"],
      "is_launch": false,
      "involves_major_company": true,
      "companies_mentioned": ["OpenAI", "Google"]
    }}
  ],
  "secondary_stories": [ /* same format with why_it_matters */ ],
  "next_10_stories": [ /* same format with why_it_matters - stories ranked 11-20 */ ],
  "top_20_launches": [ /* same format with why_it_matters - top 20 launches ranked by importance */ ],
  "other_launches": [ /* remaining launches - same format but no why_it_matters needed */ ],
  "other_stories_count": 0,
  "deduplication_summary": {{
    "original_story_count": {len(raw_stories)},
    "deduplicated_story_count": 0,
    "stories_merged": 0
  }}
}}

IMPORTANT:
- Be aggressive with deduplication - if stories cover the same event, merge them
- Use your judgment for ranking - follow the examples in the Newsletter Stories Example document
- Review the example stories to understand story selection and prioritization
- Include "why_it_matters" for top 20 stories (top 5 + secondary 5 + next 10) - explain strategic significance in one sentence
- For "other_stories_count", just provide the count - DO NOT list all other stories (saves tokens)
- Output ONLY valid JSON, no other text"""

    # Create user prompt with all stories
    stories_json = json.dumps(raw_stories, indent=2)

    user_prompt = f"""Here are the {len(raw_stories)} raw news stories to deduplicate and rank:

{stories_json}

Please deduplicate, tag launches, rank, and categorize these stories following the instructions.
Return your response as valid JSON only."""

    print("\n[1/2] Calling Claude API for deduplication and ranking...")
    print(f"      Input: {len(raw_stories)} raw stories")
    print(f"      Context: ~{len(stories_json) // 4} tokens")

    try:
        # Call Claude API with streaming for large responses
        response_text = ""

        with anthropic_client.messages.stream(
            model=config['claude']['model'],
            max_tokens=config['claude']['max_tokens'],
            temperature=config['claude']['temperature'],
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        ) as stream:
            for text in stream.text_stream:
                response_text += text

        print(f"      Response: ~{len(response_text) // 4} tokens")

        # Save raw response for debugging
        debug_file = "outputs/debug_dedup_response.txt"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"      Debug: Saved raw response to {debug_file}")

        # Extract JSON from response (handle markdown code blocks)
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

        # Save extracted JSON for debugging
        debug_json_file = "outputs/debug_dedup_json.txt"
        with open(debug_json_file, 'w', encoding='utf-8') as f:
            f.write(json_text)
        print(f"      Debug: Saved extracted JSON to {debug_json_file}")

        # Parse JSON
        result = json.loads(json_text)

        print("\n[2/2] Deduplication and ranking complete!")
        print(f"\n{'='*70}")
        print("RESULTS SUMMARY:")
        print(f"{'='*70}")
        print(f"Original stories:     {result.get('deduplication_summary', {}).get('original_story_count', len(raw_stories))}")
        print(f"After deduplication:  {result.get('deduplication_summary', {}).get('deduplicated_story_count', 0)}")
        print(f"Stories merged:       {result.get('deduplication_summary', {}).get('stories_merged', 0)}")
        print(f"\nCATEGORIZATION:")
        print(f"  Top 5 stories:      {len(result.get('top_stories', []))}")
        print(f"  Secondary 5:        {len(result.get('secondary_stories', []))}")
        print(f"  Next 10:            {len(result.get('next_10_stories', []))}")
        print(f"  Top 20 launches:    {len(result.get('top_20_launches', []))}")
        print(f"  Other launches:     {len(result.get('other_launches', []))}")
        print(f"  Other stories:      {result.get('other_stories_count', 0)}")
        print(f"{'='*70}")

        return result

    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Failed to parse JSON response: {e}")
        print(f"Response preview: {response_text[:500]}...")
        raise
    except Exception as e:
        print(f"\n[ERROR] Failed to deduplicate and rank: {e}")
        raise


def main():
    """Main deduplication and ranking workflow."""
    print(f"\n{'='*70}")
    print("AI NEWSLETTER CURATOR - STEP 2: DEDUPLICATION & RANKING")
    print(f"{'='*70}")

    # Load configuration
    config = load_config()
    workflow_doc = load_workflow_docs()
    style_guide = load_style_guide()
    example_stories = load_example_stories()

    # Load raw stories
    input_file = "outputs/raw_stories_2025-11-03_to_2025-11-10_COMPLETE.json"
    print(f"\n[1] Loading raw stories from: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    raw_stories = raw_data['stories']
    print(f"[OK] Loaded {len(raw_stories)} raw stories")

    # Deduplicate and rank
    ranked_data = deduplicate_and_rank_stories(
        raw_stories,
        config,
        workflow_doc,
        style_guide,
        example_stories
    )

    # Save ranked stories
    output_file = "outputs/ranked_stories_2025-11-03_to_2025-11-10.json"
    output_data = {
        "ranking_date": datetime.now().strftime("%Y-%m-%d"),
        "date_range": raw_data['date_range'],
        "original_story_count": len(raw_stories),
        "deduplication_summary": ranked_data.get('deduplication_summary', {}),
        "top_stories": ranked_data.get('top_stories', []),
        "secondary_stories": ranked_data.get('secondary_stories', []),
        "next_10_stories": ranked_data.get('next_10_stories', []),
        "top_20_launches": ranked_data.get('top_20_launches', []),
        "other_launches": ranked_data.get('other_launches', []),
        "other_stories_count": ranked_data.get('other_stories_count', 0),
        "notes": "Deduplicated and ranked stories ready for human review (Step 3). Top 20 stories and top 20 launches include 'why_it_matters' for editorial review."
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Saved ranked stories to: {output_file}")
    print(f"\n{'='*70}")
    print("NEXT STEP: Human review")
    print(f"{'='*70}")
    print("Review the ranked stories and approve before proceeding to formatting.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
