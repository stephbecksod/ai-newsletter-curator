# AI Newsletter Curator - Project Status

**Last Updated:** November 14, 2025

## Project Overview

This tool reads AI newsletters from Gmail (specific senders, date range), extracts news stories, deduplicates overlapping coverage, ranks by importance, and outputs formatted copy ready for the weekly AI news deck.

### Command Structure
```bash
python newsletter_curator.py --start 2025-11-04 --end 2025-11-10
```

### Architecture
- **Gmail MCP Server** - Claude directly queries Gmail via MCP (Model Context Protocol)
- **Claude API** - Handles extraction, deduplication, ranking, and formatting
- **Python Orchestration** - Coordinates workflow and saves outputs

### Newsletter Sources (Gmail Senders)
- superhuman@mail.joinsuperhuman.ai
- ai.plus@axios.com
- newsletters@techcrunch.com
- thatstartupguy@mail.beehiiv.com
- news@daily.therundown.ai
- startupintros@mail.beehiiv.com

---

## ✅ Completed Tasks

### Phase 1: MCP Gmail Setup & Testing
- [x] Installed `@gongrzhe/server-gmail-autoauth-mcp` npm package globally
- [x] Created `~/.claude/mcp_settings.json` configuration file
- [x] Updated `.gitignore` to exclude outputs/, credentials, and sensitive files
- [ ] **PENDING:** Restart Claude Code and test Gmail connectivity (will do after building project structure)

---

## 🚧 Current Phase: Project Structure

### Phase 3: Create Project Files
**Status:** In Progress

Files to create:
- [ ] `newsletter_curator.py` - Main orchestration script
- [ ] `config.yaml` - Newsletter sources and formatting settings
- [ ] `requirements.txt` - Python dependencies
- [ ] `.env.example` - Template for API keys
- [ ] `README.md` - Setup and usage instructions
- [ ] `outputs/` directory - For generated newsletter copy (gitignored)

---

## 📋 Upcoming Phases

### Phase 2: Newsletter Extraction
**Reference:** `docs/Newsletter Copy Creation Workflow.md` (Step 1)

Tasks:
- [ ] Extract raw newsletter content from Gmail for date range
- [ ] Use Claude API to identify actual news (not tips/tools/tutorials)
- [ ] Store: headline, source, date, summary, URL (if available)
- [ ] Output: Raw list of all news stories (un-deduplicated, unranked)

**Key Requirements:**
- Extract ONLY news stories (partnerships, products, features, fundraising, valuations)
- No tips, tools, tutorials, or opinion content
- Create standalone list that doesn't get overridden by next steps

### Phase 3: Deduplication & Ranking
**Reference:** `docs/Newsletter Copy Creation Workflow.md` (Steps 2-3)

Tasks:
- [ ] Group overlapping stories across newsletters
- [ ] Merge duplicates (keep combined sources, earliest date, URLs)
- [ ] Tag launches (new model, company, product, feature, integration, partnership)
- [ ] Rank by criteria:
  - Multiple newsletter mentions
  - Headline appearance
  - Major AI company involvement
  - Significance judgment
  - Casual reader "caught up" test
- [ ] Output: Categorized list (Top 5, Secondary 4-5, Launches, Other)
- [ ] Present to user for approval before formatting

**Ranking Categories:**
- Top 5 stories
- Next 4-5 secondary stories
- Launch list (all launches not in top stories)
- Everything else

### Phase 4: Research & Formatting
**Reference:**
- `docs/Newsletter Copy Creation Workflow.md` (Steps 4-8)
- `docs/Newsletter Style Guide.md` (all sections)
- `docs/Newsletter Stories Example.md` (formatting examples)

Tasks:
- [ ] Research top 5 stories (review newsletters, follow URLs, web search 1-2 articles)
- [ ] Update summaries and "why it matters" based on research
- [ ] Format Top 5 stories (headline, summary, why it matters)
  - Follow bolding rules and slide layout constraints
- [ ] Format Secondary stories (emoji + headline + 1-2 sentences)
- [ ] Format Launches list (bullet list, one line per launch)
- [ ] Output: Fully formatted copy ready to paste into deck

**Formatting Rules:**
- **Top Stories:** Headline (3 lines), Summary (4-6 lines), Why it matters (2-3 lines)
- **Secondary Stories:** Emoji + bold headline (1 line) + 1-2 sentence summary
- **Launches:** Simple bullet list, no emojis, no bolding, past/present tense

### Phase 5: Polish & Repeatability
Tasks:
- [ ] Error handling and edge cases
- [ ] Validation that output matches example format
- [ ] Documentation for weekly use
- [ ] Git commit workflow
- [ ] Test with multiple historical date ranges

---

## Reference Documents

### 1. Newsletter Copy Creation Workflow.md
Complete step-by-step process from email ingestion to final output. Defines what to extract, how to deduplicate, ranking criteria, and exact formatting specifications.

### 2. Newsletter Style Guide.md
Writing tone, voice, and style preferences. Formatting rules for headlines, summaries, bullets. Use when Claude generates or formats any text.

### 3. Newsletter Stories Example.md
Historical examples of finished newsletters (week by week). Shows prioritization, categorization, and exact formatting in practice. Ground truth for "good output."

---

## Technical Notes

### Date Range Approach
- Allows testing with historical newsletters during development
- Enables re-running if something breaks
- Provides flexibility for different time periods
- No assumptions about "current week"

### Gmail MCP Authentication
**First Use:** Browser will open for Google authentication, credentials stored in `~/.gmail-mcp/`
**Subsequent Uses:** Saved credentials used automatically

### File Structure
```
ai-newsletter-curator/
├── docs/
│   ├── Newsletter Copy Creation Workflow.md
│   ├── Newsletter Style Guide.md
│   └── Newsletter Stories Example.md
├── outputs/               # gitignored
│   └── newsletter_YYYY-MM-DD.md
├── .env                   # gitignored
├── .env.example
├── .gitignore
├── config.yaml
├── newsletter_curator.py
├── PROJECT_STATUS.md
├── README.md
└── requirements.txt
```

---

## Next Steps

1. Create project structure files (config.yaml, requirements.txt, etc.)
2. Build main Python orchestration script
3. Restart Claude Code and test Gmail MCP connectivity
4. Test newsletter extraction with historical data (Nov 4-10, 2025)
5. Build and test each phase sequentially

---

**Development Philosophy:** Build in phases, test each component before moving to the next. Use real historical newsletter data for validation.
