# AI Newsletter Curator

Automated tool to process weekly AI newsletters from Gmail, extract news stories, deduplicate overlapping coverage, rank by importance, and generate formatted copy for your weekly AI news deck.

## Overview

This tool uses:
- **Gmail MCP Server** - Direct access to Gmail via Model Context Protocol
- **Claude API** - AI-powered extraction, deduplication, ranking, and formatting
- **Python** - Workflow orchestration and output management

## Features

- ✉️ Reads newsletters from specific Gmail senders within a date range
- 📰 Extracts only actual news stories (filters out tips, tools, tutorials)
- 🔄 Deduplicates overlapping stories across multiple newsletters
- 📊 Ranks stories by importance using multiple criteria
- ✍️ Generates formatted copy in your specific writing style
- 📝 Outputs ready-to-paste content for presentation decks

## Prerequisites

- **Python 3.8+**
- **Node.js** (for Gmail MCP server)
- **Anthropic API Key** (for Claude access)
- **Gmail Account** (with newsletters)

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

On first use, the Gmail MCP server will:
1. Open your browser for Google OAuth authentication
2. Store credentials securely in `~/.gmail-mcp/`
3. Use saved credentials automatically for future requests

## Usage

### Basic Command

```bash
python newsletter_curator.py --start 2025-11-04 --end 2025-11-10
```

### Command Arguments

- `--start` (required): Start date in YYYY-MM-DD format
- `--end` (required): End date in YYYY-MM-DD format

### Example: Process Last Week's Newsletters

```bash
python newsletter_curator.py --start 2025-11-04 --end 2025-11-10
```

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
├── docs/                           # Reference documentation
│   ├── Newsletter Copy Creation Workflow.md
│   ├── Newsletter Style Guide.md
│   └── Newsletter Stories Example.md
├── outputs/                        # Generated newsletters (gitignored)
├── .env                           # API keys (gitignored)
├── .env.example                   # Environment template
├── .gitignore                     # Git exclusions
├── config.yaml                    # Configuration settings
├── newsletter_curator.py          # Main script
├── PROJECT_STATUS.md              # Development progress tracker
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Development Status

See `PROJECT_STATUS.md` for current development progress and next steps.

## License

[Your License Here]

## Support

For issues or questions, please open an issue on GitHub.
