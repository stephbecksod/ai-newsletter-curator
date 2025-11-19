# Newsletter Curator - Progress Summary
**Date:** November 15, 2025
**Status:** Phase 1 (Extraction) - Paused due to token optimization needed

---

## Current Situation

We're currently working on **Step 1: Newsletter Extraction** from the workflow. We've successfully extracted news stories from **8 newsletters** and saved **43 news stories** to the raw stories JSON file. However, we've identified a **critical scalability issue** that needs to be addressed before continuing.

### Token Usage Problem ⚠️

- **Total newsletters in date range (Nov 3-10):** 40 newsletters
- **Newsletters successfully read:** 22+ (55%)
- **Newsletters that hit token limits:** 7+ (mostly Axios AI+ and TechCrunch)
- **Token usage so far:** 140,118 tokens (70% of 200K budget)
- **Projected token usage for 40 newsletters:** 200K+ tokens

**The Problem:** Many newsletters (especially Axios AI+ and TechCrunch) are HTML-heavy and exceed the 25,000 token limit per read_email call. Processing 40 newsletters per week using the current approach is not sustainable.

**Status:** We need to brainstorm token reduction strategies before continuing extraction.

---

## What We've Completed

### ✅ Infrastructure Setup
- [x] Gmail MCP server installed and configured
- [x] Python environment with dependencies (anthropic, pyyaml, python-dotenv)
- [x] Project structure created (config.yaml, requirements.txt, .env.example)
- [x] Newsletter sources configured (6 senders)
- [x] Reference documents loaded (workflow, style guide, examples)
- [x] Main orchestration script (newsletter_curator.py) created

### ✅ Step 1: Extraction (Partial)
- [x] Gmail search query tested (found 40 newsletters for Nov 3-10)
- [x] Successfully read 22+ newsletters
- [x] Extracted 43 news stories from 8 newsletters
- [x] Saved to: `outputs/raw_stories_2025-11-03_to_2025-11-10.json`

**Sources processed:**
- The Rundown AI (multiple dates)
- Superhuman (Nov 10)
- TechCrunch (Nov 10)
- Startup Intros (Nov 10, Nov 6, Nov 3)
- That Startup Guy (Nov 7, Nov 5, Nov 4)

**Stories extracted include:**
- OpenAI-AWS $38B partnership
- Perplexity-Snap $400M deal
- Adobe MAX 2025 AI announcements
- Meta $600B AI infrastructure investment
- Google-Anthropic investment talks at $350B valuation
- Multiple product launches (Firefly Image Model 5, Hailuo 2.3, etc.)
- And 30+ more stories

---

## Newsletters That Hit Token Limits

These newsletters exceeded the 25,000 token limit for `read_email`:

1. **Axios AI+ (4 emails):**
   - Nov 10: 30,792 tokens
   - Nov 8: 27,523 tokens
   - Nov 7: 28,531 tokens
   - Nov 6: 26,831 tokens

2. **TechCrunch (3 emails):**
   - Nov 9: 25,305 tokens
   - Nov 8: 27,006 tokens
   - Nov 7: 26,899 tokens

**Common pattern:** HTML-heavy newsletters with embedded images, formatting, and ads.

---

## Next Steps (When We Resume)

### Immediate Priority: Token Optimization Strategy

Before continuing extraction, we need to brainstorm and implement token reduction strategies. Options to explore:

1. **Preprocessing approaches:**
   - Strip HTML and extract plain text before passing to Claude
   - Use Gmail API to get text/plain part only
   - Implement client-side HTML-to-text conversion

2. **Batching strategies:**
   - Process fewer newsletters per session
   - Incremental extraction with checkpointing
   - Split large newsletters into chunks

3. **Smart filtering:**
   - Extract headlines/links first, then fetch full content only for relevant items
   - Use lighter model for initial filtering before detailed extraction

4. **Alternative extraction approaches:**
   - Use search within email body to find news sections
   - Pattern matching for common newsletter structures
   - Custom parsers for each newsletter source

5. **Caching/Deduplication:**
   - Store parsed newsletter content to avoid re-reading
   - Implement resume capability for interrupted sessions

### After Token Optimization

Once we have a sustainable extraction strategy:

1. **Complete Step 1:** Extract all 40 newsletters from Nov 3-10
2. **Update raw_stories JSON:** Add remaining stories to the file
3. **Implement Step 2:** Deduplication and ranking
4. **Implement Step 3:** Human review interface
5. **Implement Step 4:** Research top 5 stories
6. **Implement Steps 5-8:** Formatting and output

---

## File Locations

### Input Files
- `config.yaml` - Newsletter sources and settings
- `docs/Newsletter Copy Creation Workflow.md` - Workflow specification
- `docs/Newsletter Style Guide.md` - Writing style guide
- `docs/Newsletter Stories Example.md` - Historical examples

### Output Files (Created)
- `outputs/raw_stories_2025-11-03_to_2025-11-10.json` - Extracted stories (43 stories from 8 newsletters)

### Output Files (Pending)
- `outputs/ranked_stories_2025-11-03_to_2025-11-10.json` - After Step 2
- `outputs/newsletter_2025-11-03_to_2025-11-10.md` - Final formatted output

---

## Technical Details

### Gmail Search Query Used
```
(from:superhuman@mail.joinsuperhuman.ai OR from:ai.plus@axios.com OR from:newsletters@techcrunch.com OR from:thatstartupguy@mail.beehiiv.com OR from:news@daily.therundown.ai OR from:startupintros@mail.beehiiv.com) AND after:2025-11-03 before:2025-11-10
```

### Claude API Configuration
- Model: `claude-sonnet-4-5-20250929`
- Max tokens: 16,000
- Temperature: 0.7

### Newsletter Sources
1. Superhuman (`superhuman@mail.joinsuperhuman.ai`)
2. Axios AI+ (`ai.plus@axios.com`)
3. TechCrunch (`newsletters@techcrunch.com`)
4. That Startup Guy (`thatstartupguy@mail.beehiiv.com`)
5. The Rundown AI (`news@daily.therundown.ai`)
6. Startup Intros (`startupintros@mail.beehiiv.com`)

---

## Questions to Address

1. **Token reduction:** What's the best approach to handle HTML-heavy newsletters without hitting token limits?
2. **Extraction quality:** Can we maintain extraction quality while reducing token usage?
3. **Scalability:** How do we ensure this works for 40+ newsletters per week long-term?
4. **Error recovery:** Should we implement retry logic for failed newsletter reads?
5. **Incremental processing:** Should we save progress after each newsletter or batch?

---

## How to Resume Work

1. **Review this document** and the current state in `outputs/raw_stories_2025-11-03_to_2025-11-10.json`
2. **Brainstorm token reduction strategies** (user requested this specifically)
3. **Implement chosen strategy** for handling large/HTML-heavy newsletters
4. **Test with one of the failed newsletters** (e.g., Axios AI+ from Nov 10)
5. **Continue extraction** for remaining 32 newsletters once strategy is validated
6. **Complete Step 1** and move to Step 2 (deduplication and ranking)

---

## Key Insights from Work So Far

### Newsletter Characteristics
- **The Rundown AI:** Clean, well-structured, easy to extract
- **Superhuman:** Moderate size, good news density
- **That Startup Guy:** Smaller newsletters, focused content
- **Startup Intros:** Mixed content (news + investor intros)
- **Axios AI+:** HTML-heavy, exceeds token limits
- **TechCrunch:** HTML-heavy, exceeds token limits

### Story Types Found
- Major partnerships and deals (OpenAI-AWS, Perplexity-Snap)
- Fundraising and valuations (Gamma $2.1B, Scribe $1.3B)
- Product launches (Adobe Firefly, Hailuo 2.3, Cursor Composer)
- Company announcements (Meta $600B investment)
- Regulatory news (EU AI Act changes)
- Market movements (Tech stocks lose $1T)

### Extraction Quality
- Headlines are clear and descriptive
- Summaries capture key details (1-3 sentences)
- Sources are consistently named
- Dates are properly formatted (YYYY-MM-DD)
- URLs preserved where available

---

**Remember:** The goal is to process 40 newsletters per week sustainably. Token optimization is critical for long-term viability.
