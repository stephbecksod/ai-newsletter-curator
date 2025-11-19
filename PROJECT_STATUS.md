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
- [x] Restarted Claude Code and tested Gmail connectivity
- [x] Successfully searched Gmail and retrieved newsletters

### Phase 2: Project Structure
- [x] `newsletter_curator.py` - Main orchestration script created
- [x] `config.yaml` - Newsletter sources and formatting settings configured
- [x] `requirements.txt` - Python dependencies listed
- [x] `.env.example` - Template for API keys created
- [x] `README.md` - Setup and usage instructions written
- [x] `outputs/` directory - Created with .gitkeep
- [x] All reference documents loaded and integrated

### Phase 3: Step 1 - Newsletter Extraction ✅ COMPLETE
- [x] Gmail search query tested (found 35 newsletters for Nov 3-10, 2025)
- [x] Implemented plain text extraction strategy (92% token reduction)
- [x] Successfully processed ALL 35 newsletters using Gmail API + Claude API
- [x] Extracted **352 news stories** from 35 newsletters
- [x] Saved complete dataset to `outputs/raw_stories_2025-11-03_to_2025-11-10_COMPLETE.json`
- [x] **SOLVED:** Token optimization via plain text extraction (no HTML/images/formatting)

**Progress:** 35 of 35 newsletters fully processed (100%) ✅

---

## 🚧 Current Phase: Step 3 - Human Review & Approval

### Phase 1 Complete! ✅ (Step 1: Extraction)
**Solution Implemented:** Plain text extraction via Gmail API
- 92% token reduction (28K → 2K tokens per newsletter)
- All 35 newsletters processed successfully
- 352 news stories extracted
- Output: `outputs/raw_stories_2025-11-03_to_2025-11-10_COMPLETE.json`

### Phase 2 Complete! ✅ (Step 2: Deduplication & Ranking)
**Completed:** November 18, 2025
- 352 raw stories → 114 deduplicated stories
- 238 stories successfully merged
- Categorized into: Top 5 (5), Secondary (5), Launches (51), Other (53)
- Output: `outputs/ranked_stories_2025-11-03_to_2025-11-10.json`

**Top 5 Stories Selected:**
1. OpenAI-AWS $38B cloud deal (6 mentions)
2. Apple-Google $1B/year Gemini for Siri (6 mentions)
3. Microsoft $25B+ AI infrastructure deals (6 mentions)
4. Anthropic $70B revenue projection by 2028 (4 mentions)
5. Tesla shareholders approve Musk's $1T pay package (3 mentions)

**Next Steps:**
1. **Human review:** Review and approve the ranked story list
2. If approved → Proceed to Step 4 (Research top 5 stories)
3. Then Steps 5-8 (Formatting & final output)

---

## 📋 Upcoming Phases

### Step 1: Newsletter Extraction (CONTINUATION)
**Reference:** `docs/Newsletter Copy Creation Workflow.md` (Step 1)

**Status:** 20% complete (8 of 40 newsletters processed)

Remaining tasks:
- [ ] Implement token optimization strategy for HTML-heavy newsletters
- [ ] Extract remaining 32 newsletters from Gmail
- [ ] Update `raw_stories_2025-11-03_to_2025-11-10.json` with all stories
- [ ] Verify all news stories extracted (not tips/tools/tutorials)

**Already Completed:**
- [x] Gmail search and email retrieval working
- [x] Claude API extraction working for well-formatted emails
- [x] 43 stories extracted from 8 newsletters
- [x] Raw JSON output structure established

### Step 2: Deduplication & Ranking
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

### Gmail Authentication & Credentials

**MCP OAuth Token Location (IMPORTANT):**
- `C:\Users\steph\.gmail-mcp\gmail-token.json`
- Contains OAuth access token, refresh token, client ID/secret
- Used by both MCP server AND Python Gmail text extractor

**First Use:** Browser opens for Google authentication, credentials saved automatically
**Subsequent Uses:** Saved credentials reused (no re-authentication needed)

**Python Gmail API:**
- The `gmail_text_extractor.py` script automatically loads MCP credentials
- No separate OAuth setup required
- Falls back to standard OAuth flow if MCP token not found

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
