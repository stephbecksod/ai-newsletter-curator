# AI Newsletter Curator - Project Status

**Last Updated:** November 20, 2025

## Project Overview

Complete Claude Code skill for automated AI newsletter curation from Gmail. Reads newsletters from specific senders, extracts news stories, deduplicates overlapping coverage, ranks by weighted editorial criteria, and outputs formatted copy ready for weekly AI news decks.

### Usage
```
Ask Claude Code: "Curate newsletter from [start-date] to [end-date]"
```

### Architecture
- **Claude Code Skill** - Automated 8-step workflow with human-in-the-loop review
- **Gmail MCP Server** - Direct Gmail access via Model Context Protocol
- **Claude API** - AI-powered extraction, deduplication, ranking, and formatting
- **Python Scripts** - Newsletter extraction and story ranking automation

---

## ✅ Project Complete - Fully Operational

### Phase 1: Infrastructure Setup ✅
- [x] Gmail MCP server installed and configured
- [x] Python environment and dependencies
- [x] Anthropic API integration
- [x] OAuth authentication for Gmail
- [x] Project structure and configuration

### Phase 2: Core Scripts ✅
- [x] `extract_all_newsletters.py` - Newsletter extraction with Claude API
- [x] `deduplicate_and_rank.py` - Story deduplication and weighted ranking
- [x] `gmail_text_extractor.py` - Gmail API helper
- [x] Command line arguments for date ranges
- [x] Auto-detection of latest files
- [x] Dynamic output filename generation

### Phase 3: Workflow Development ✅
- [x] Step 1: Newsletter extraction from Gmail
- [x] Step 2: Deduplication and ranking with weighted editorial criteria
- [x] Step 3: Human review and approval (mandatory)
- [x] Step 4: Research top 5 stories with web searches
- [x] Step 5: Format top 5 stories with character count enforcement
- [x] Step 6: Format secondary 5 stories with emojis
- [x] Step 7: Format launches list
- [x] Step 8: Generate final newsletter markdown

### Phase 4: Claude Code Skill ✅
- [x] Created `.claude/skills/newsletter-curator/` directory
- [x] `SKILL.md` - Skill definition with YAML frontmatter
- [x] `workflow-guide.md` - Detailed 585-line workflow guide
- [x] `examples.md` - Complete usage examples and troubleshooting
- [x] Skill tested end-to-end successfully

### Phase 5: Documentation ✅
- [x] `SETUP.md` - Comprehensive setup guide for new users
- [x] `README.md` - Updated with skill-based usage
- [x] Workflow documentation with ranking criteria
- [x] Style guide with character count targets
- [x] Newsletter examples for reference

### Phase 6: Testing & Validation ✅
- [x] Tested with Nov 3-10, 2025 (352 stories → 125 unique)
- [x] Tested with Nov 17-20, 2025 (218 stories → 122 unique)
- [x] Fixed script bugs (timeout, file paths)
- [x] Validated weighted editorial ranking
- [x] Confirmed character count enforcement
- [x] Human review workflow validated

---

## 📊 Current Status: Production Ready

### Latest Test Run (Nov 17-20, 2025)
- **Extraction:** 218 stories from 18 newsletters
- **Deduplication:** 122 unique stories (96 merged)
- **Categorization:**
  - Top 5 stories
  - Secondary 5 stories
  - Top 20 launches
  - 12 other launches
- **Output:** `newsletter_2025-11-17_to_2025-11-20.md`

### Key Features Validated
✅ Gmail MCP integration working
✅ Plain text extraction (92% token reduction)
✅ Weighted editorial ranking (strategic significance over mention count)
✅ Controversy boost for safety/regulatory stories
✅ Launch vs news distinction
✅ Human review with approval before research
✅ Web research for top 5 stories
✅ Character count enforcement (50/233/124)
✅ Proper markdown formatting with bolding
✅ Complete automation via skill

---

## 🎯 Ranking Criteria (Weighted Editorial Approach)

### Priority Order:
1. **"Why it matters" strength** - Strategic significance
2. **Story type weighting:**
   - HIGH: Platform battles, controversy/safety, moonshots, market structure
   - MEDIUM: Major launches, large funding, enterprise adoption
   - LOW: Infrastructure capex, corporate governance, incremental updates
3. **Multiple mentions** - 2+ for high-priority, 3+ for others
4. **Headline appearance**
5. **Major AI company involvement** (not sufficient alone)

### Special Rules:
- **Controversy Boost:** +1-2 tiers for lawsuits, safety, regulatory action
- **Launch vs News:** Products within 3 months = launch; research/visions = news
- **Infrastructure Context:** Large deals secondary unless strategic shift

---

## 📁 File Outputs

Each curation run generates:
```
outputs/
├── raw_stories_YYYY-MM-DD_to_YYYY-MM-DD_COMPLETE.json    # All extracted stories
├── ranked_stories_YYYY-MM-DD_to_YYYY-MM-DD.json          # Ranked/deduplicated
├── newsletter_YYYY-MM-DD_to_YYYY-MM-DD.md                # Final formatted output
└── debug_dedup_response.txt                               # API debug log
```

---

## 🛠️ Technical Implementation

### Newsletter Sources (config.yaml)
- superhuman@mail.joinsuperhuman.ai
- ai.plus@axios.com
- newsletters@techcrunch.com
- thatstartupguy@mail.beehiiv.com
- news@daily.therundown.ai
- startupintros@mail.beehiiv.com

### Character Count Targets
- **Headlines:** ~50 characters (42-62 range)
- **Summaries:** ~233 characters (202-288 range)
- **Why it matters:** ~124 characters (85-165 range)

### Cost per Weekly Curation
- Extraction: ~$2-5 (Claude API)
- Ranking: ~$1-2 (Claude API)
- Research: ~$0.50-1 (Web searches)
- **Total:** ~$3.50-8 per week

---

## 📚 Documentation

### User Documentation
- **SETUP.md** - Complete setup guide for new users
- **README.md** - Quick start and project overview
- **.claude/skills/newsletter-curator/examples.md** - Usage examples

### Workflow Documentation
- **docs/Newsletter Copy Creation Workflow.md** - Complete 8-step process
- **docs/Newsletter Style Guide.md** - Voice, tone, formatting rules
- **docs/Newsletter Stories Example.md** - Historical examples

### Technical Documentation
- **.claude/skills/newsletter-curator/workflow-guide.md** - 585-line detailed guide
- **.claude/skills/newsletter-curator/SKILL.md** - Skill definition

---

## 🔄 Recent Changes (Nov 20, 2025)

### Commits
1. **Implement Steps 1-2:** Newsletter extraction and deduplication/ranking
2. **Enhance ranking system:** Weighted editorial approach and character limits
3. **Add newsletter-curator skill:** Complete workflow automation
4. **Add command line arguments:** Script improvements for skill integration
5. **Add comprehensive setup guide:** Documentation for new users

### Bug Fixes
- Fixed Anthropic API timeout (added 600s timeout)
- Fixed hardcoded date ranges in extraction script
- Fixed hardcoded file paths in ranking script
- Added auto-detection of latest raw stories file
- Added dynamic output filename generation

---

## ✨ Next Steps (Future Enhancements)

### Potential Improvements
- [ ] Add support for customizable character count targets per user
- [ ] Implement newsletter source management UI
- [ ] Add story preview/draft mode before final formatting
- [ ] Create analytics dashboard for story trends
- [ ] Add support for multiple newsletter topics beyond AI
- [ ] Implement caching to reduce API costs
- [ ] Add export to other formats (PDF, HTML, Notion)

### Community Contributions
- [ ] Add more newsletter source templates
- [ ] Create alternative ranking criteria presets
- [ ] Add multilingual newsletter support
- [ ] Create integration with presentation tools (Google Slides, PowerPoint)

---

## 🎉 Project Milestones

- **Nov 14, 2025:** Project initiated, infrastructure setup
- **Nov 18, 2025:** Steps 1-2 implemented (extraction and ranking)
- **Nov 19, 2025:** Complete 8-step workflow tested
- **Nov 20, 2025:** Claude Code skill created and tested
- **Nov 20, 2025:** Comprehensive documentation completed
- **Nov 20, 2025:** **PROJECT COMPLETE - PRODUCTION READY**

---

**Status:** ✅ Production Ready - Fully automated newsletter curation via Claude Code skill
