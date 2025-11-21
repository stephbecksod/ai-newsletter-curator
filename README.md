# AI Newsletter Curator

Automated Claude Code skill for processing weekly AI newsletters from Gmail, extracting news stories, deduplicating overlapping coverage, ranking by strategic importance, and generating formatted copy for your weekly AI news deck.

## Overview

This project provides a **Claude Code skill** that automates the complete newsletter curation workflow using:
- **Claude Code** - Main interface and skill orchestration
- **Gmail MCP Server** - Direct access to Gmail via Model Context Protocol
- **Claude API** - AI-powered extraction, deduplication, ranking, and formatting
- **Python Scripts** - Newsletter extraction and ranking automation

## Features

- ✉️ Reads newsletters from specific Gmail senders within a date range
- 📰 Extracts only actual news stories (filters out tips, tools, tutorials)
- 🔄 Deduplicates overlapping stories across multiple newsletters
- 📊 Ranks stories using weighted editorial criteria (strategic significance over mention count)
- 🧠 AI-powered research for top 5 stories with web searches
- ✍️ Generates formatted copy with strict character count enforcement
- 📝 Outputs ready-to-paste content for presentation decks
- 👤 Human-in-the-loop review and approval before research

## Quick Start

**📘 See [SETUP.md](SETUP.md) for complete setup instructions**

### Prerequisites

- **Claude Code** installed and configured
- **Python 3.11+**
- **Node.js and npm** (for Gmail MCP server)
- **Anthropic API Key**
- **Gmail Account** with AI newsletters

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-newsletter-curator
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Gmail MCP Server

```bash
npm install -g @gongrzhe/server-gmail-autoauth-mcp
```

### 4. Configure MCP for Claude Code

Create or update `~/.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"]
    }
  }
}
```

**Important:** Restart Claude Code after creating this configuration file.

### 5. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Get your API key from: https://console.anthropic.com/

### 6. Gmail Authentication

**IMPORTANT: MCP OAuth Credentials Location**
- The Gmail MCP server stores OAuth credentials in: `C:\Users\steph\.gmail-mcp\gmail-token.json`
- The Python Gmail text extractor (`gmail_text_extractor.py`) automatically reuses these credentials
- No separate OAuth setup needed if MCP is already configured!

On first MCP use:
1. Browser opens for Google OAuth authentication
2. Credentials stored securely in `~/.gmail-mcp/`
3. Subsequent requests use saved credentials automatically

## Usage

### Using the Skill

Once set up, simply ask Claude Code to curate your newsletter:

```
Curate newsletter from November 24 to December 1, 2025
```

Or:

```
Create my AI newsletter for this week (Nov 24-Dec 1)
```

The skill will automatically:
1. Extract stories from Gmail newsletters
2. Deduplicate and rank using weighted editorial criteria
3. Present top 20 stories for your review
4. Wait for your approval
5. Research top 5 stories with web searches
6. Format everything with strict character counts
7. Generate final newsletter markdown

### Manual Script Usage

You can also run the Python scripts directly:

**Extract stories:**
```bash
python extract_all_newsletters.py --start-date 2025-11-17 --end-date 2025-11-20
```

**Deduplicate and rank:**
```bash
python deduplicate_and_rank.py
```

The skill uses these scripts automatically.

## Workflow

The tool follows an 8-step workflow:

### Phase 1: Newsletter Extraction
- Reads emails from configured senders within date range
- Extracts only news stories (not tips, tools, or tutorials)
- Outputs raw list with headline, source, date, summary, URL

### Phase 2: Deduplication & Ranking
- Groups overlapping stories across newsletters
- Tags launches (new products, features, partnerships)
- Ranks by importance criteria:
  - Multiple newsletter mentions
  - Headline appearance
  - Major AI company involvement
  - Overall significance
- Categorizes into: Top 5, Secondary 4-5, Launches, Other

### Phase 3: Human Review
- Presents ranked list for your approval
- Allows reordering before final formatting

### Phase 4: Research (Top 5 Stories)
- Reviews newsletter content and follows URLs
- Web searches for 1-2 additional articles per story
- Updates summaries with most critical insights

### Phase 5-7: Formatting
- **Top 5:** Headline + Summary + "Why it matters"
- **Secondary 4-5:** Emoji + Bold headline + 1-2 sentences
- **Launches:** Simple bullet list

### Phase 8: Output
- Saves formatted copy to `outputs/newsletter_YYYY-MM-DD_to_YYYY-MM-DD.md`
- Ready to paste into presentation deck

## Configuration

### Newsletter Sources

Edit `config.yaml` to customize:
- Email senders to monitor
- Major AI companies for ranking
- Story count targets
- Output formatting

Default sources:
- superhuman@mail.joinsuperhuman.ai
- ai.plus@axios.com
- newsletters@techcrunch.com
- thatstartupguy@mail.beehiiv.com
- news@daily.therundown.ai
- startupintros@mail.beehiiv.com

## Output

Generated files are saved to `outputs/` directory:

```
outputs/newsletter_2025-11-04_to_2025-11-10.md
```

Each file contains:
- Top 5 stories (fully formatted)
- Secondary stories (4-5 stories)
- Launches this week (bullet list)

## Reference Documents

- `docs/Newsletter Copy Creation Workflow.md` - Complete workflow specification
- `docs/Newsletter Style Guide.md` - Writing style and formatting rules
- `docs/Newsletter Stories Example.md` - Historical examples for reference

## Troubleshooting

### Gmail MCP Not Working

1. Verify installation: `npm list -g @gongrzhe/server-gmail-autoauth-mcp`
2. Check MCP config: `cat ~/.claude/mcp_settings.json`
3. Restart Claude Code after configuration changes
4. Check authentication: `ls -la ~/.gmail-mcp/`

### Claude API Errors

- Verify API key in `.env` file
- Check API key is valid at https://console.anthropic.com/
- Ensure sufficient API credits

### No Newsletters Found

- Verify date range covers newsletter send dates
- Check sender email addresses match exactly
- Use Gmail web interface to confirm newsletters exist

## Project Structure

```
ai-newsletter-curator/
├── .claude/
│   └── skills/
│       └── newsletter-curator/     # Claude Code skill
│           ├── SKILL.md            # Skill definition
│           ├── workflow-guide.md   # Detailed workflow steps
│           └── examples.md         # Usage examples
├── docs/                           # Reference documentation
│   ├── Newsletter Copy Creation Workflow.md
│   ├── Newsletter Style Guide.md
│   └── Newsletter Stories Example.md
├── outputs/                        # Generated newsletters (gitignored)
├── .env                           # API keys (gitignored)
├── .gitignore                     # Git exclusions
├── config.yaml                    # Configuration settings
├── extract_all_newsletters.py     # Newsletter extraction script
├── deduplicate_and_rank.py        # Story ranking script
├── gmail_text_extractor.py        # Gmail API helper
├── PROJECT_STATUS.md              # Development progress
├── SETUP.md                       # Complete setup guide
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Development Status

See `PROJECT_STATUS.md` for current development progress and next steps.

## License

[Your License Here]

## Support

For issues or questions, please open an issue on GitHub.
