---
name: newsletter-curator
description: Automates the complete AI newsletter curation workflow including extraction from Gmail newsletters, deduplication, ranking with editorial criteria, human review/approval, research, and final formatting. Use this skill when the user wants to curate their weekly AI newsletter from email sources for a specific date range.
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch, TodoWrite, mcp__gmail__search_emails, mcp__gmail__read_email]
---

# Newsletter Curator Skill

## Overview
This skill automates the complete 8-step newsletter curation workflow from Gmail extraction through final formatted output, including a mandatory human review/approval step. The skill processes newsletters using weighted editorial criteria to prioritize strategic significance over mechanical metrics.

## Required Input
Before starting, collect from the user:
- **Start date** (format: YYYY-MM-DD)
- **End date** (format: YYYY-MM-DD)

Example: "Curate newsletter from November 3 to November 10, 2025"

## Workflow Steps

### STEP 1: Extract Stories from Gmail Newsletters

1. **Search Gmail** for newsletters within the specified date range using `mcp__gmail__search_emails`
2. **Read newsletter emails** using `mcp__gmail__read_email` for each newsletter found
3. **Parse and extract stories** by running `extract_newsletters.py` with the date range
4. **Save extracted stories** to `outputs/raw_stories_{start_date}_to_{end_date}.json`
5. **Report results** to user: "Extracted X stories from Y newsletters"

**Script to run:**
```bash
python extract_newsletters.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

### STEP 2: Deduplicate and Rank Stories

1. **Load raw stories** from the JSON file created in Step 1
2. **Run deduplication and ranking** using `deduplicate_and_rank.py`
3. **Apply weighted editorial criteria:**
   - Prioritize strategic significance over mention count
   - Apply story type weightings (platform battles, controversy, moonshots = high priority)
   - Apply controversy boost for safety/regulatory stories
   - Distinguish launches from news stories
4. **Generate ranked output** with:
   - Top 5 stories
   - Secondary 5 stories
   - Next 10 stories (for review)
   - Top 20 launches (ranked)
   - Other launches
5. **Save ranked stories** to `outputs/ranked_stories_{start_date}_to_{end_date}.json`
6. **Report results**: "Deduplicated X stories to Y unique stories. Ranked into top 20 news + top 20 launches."

**Script to run:**
```bash
python deduplicate_and_rank.py
```

**Key files referenced:**
- `docs/Newsletter Copy Creation Workflow.md` - Ranking criteria
- `docs/Newsletter Style Guide.md` - Style guidelines
- `docs/Newsletter Stories Example.md` - Example stories for reference

### STEP 3: Human Review and Approval (CRITICAL - DO NOT SKIP)

1. **Present the top 20 stories** in a clear, readable format:
   - Top 5 stories (with headlines, summaries, why it matters)
   - Secondary 5 stories
   - Next 10 stories (for review)
2. **Present top 20 launches** in bullet format
3. **Ask user for review:**
   - "Please review the ranked stories above."
   - "Would you like to make any changes?"
   - Offer options: swap stories, change rankings, add/remove stories
4. **Wait for explicit approval** before proceeding
5. **Apply any requested changes** to the ranking
6. **Get final confirmation:** "Are you ready to proceed to research and formatting?"

**IMPORTANT:** Never skip this step. Always wait for user approval before continuing to Step 4.

### STEP 4: Research Top 5 Stories

1. **For each of the Top 5 stories:**
   - Review original newsletter content
   - Follow any URLs included in the story data
   - Perform web search using `WebSearch` for 1-2 additional articles
   - Use `WebFetch` to read key articles
2. **Update story summaries** with:
   - More accurate details from research
   - Critical insights not in original newsletters
   - Better "why it matters" sections
3. **Save updated stories** back to the ranked JSON file

**Research focus:**
- Find exact numbers, dates, and facts
- Understand strategic implications
- Identify "why it matters" angles
- Verify company names and key players

### STEP 5: Format Top 5 Stories

1. **Read style guide** from `docs/Newsletter Style Guide.md`
2. **Read examples** from `docs/Newsletter Stories Example.md`
3. **Format each Top 5 story** with:
   - **Headline** (~50 characters, 1-2 bold phrases)
   - **Summary** (~233 characters, 2 bold phrases)
   - **Why it matters** (~124 characters, no bolding)
4. **Apply proper formatting:**
   - Use markdown bold with `**text**`
   - Follow character count targets strictly
   - Match the voice and tone from examples

**Character count targets (CRITICAL):**
- Headlines: ~50 characters (range: 42-62)
- Summaries: ~233 characters (range: 202-288)
- Why it matters: ~124 characters (range: 85-165)

### STEP 6: Format Secondary 5 Stories

1. **Format each secondary story** with:
   - Emoji that fits the theme (💸 funding, 🧠 research, 🔬 science, 💼 jobs, 🛠️ tools, ⚙️ infrastructure, 🤝 partnerships, ⚖️ legal, 😡 controversy)
   - **Bold headline** (entire headline bolded, 4-8 words)
   - 1-2 sentence summary (no bolding, ~100-135 characters)
2. **Follow the format:**
   ```
   emoji **Headline in bold**
   One to two sentences describing the story without any bolding.
   ```

### STEP 7: Format Launches List

1. **Format top 20 launches** as simple bullet list
2. **Use format:** "Company launches/released/introduces product/feature"
3. **Keep concise:** One line per launch
4. **No emojis, no bolding**
5. **Past or present tense only**

Example:
```
- Adobe unveils unified AI strategy with all major models in one plan
- OpenAI launches Agent Mode for ChatGPT Atlas
- Cursor launches Composer agentic coding model
```

### STEP 8: Generate Final Output

1. **Compile all formatted content:**
   - Top 5 Stories (formatted)
   - Other Headlines / Secondary 5 (formatted)
   - Launches (formatted list)
2. **Create final markdown file** with proper structure:
   - Title with date range
   - Section headers
   - All formatted stories
3. **Save to:** `outputs/newsletter_{start_date}_to_{end_date}.md`
4. **Present to user:** "Newsletter complete! Saved to outputs/newsletter_{date}.md"

## Supporting Files

The skill automatically references these project files:

**Documentation:**
- `docs/Newsletter Copy Creation Workflow.md` - Complete workflow steps
- `docs/Newsletter Style Guide.md` - Formatting and voice guidelines
- `docs/Newsletter Stories Example.md` - Example stories for reference

**Scripts:**
- `extract_newsletters.py` - Extracts stories from Gmail
- `deduplicate_and_rank.py` - Deduplicates and ranks stories

**Outputs:**
- `outputs/raw_stories_{date}.json` - Extracted stories
- `outputs/ranked_stories_{date}.json` - Ranked stories
- `outputs/newsletter_{date}.md` - Final formatted newsletter

## Key Features

✅ **Integrated Gmail access** via configured MCP server
✅ **Weighted editorial ranking** prioritizing strategic significance
✅ **Human-in-the-loop** with mandatory review/approval
✅ **Web research** to enrich top stories
✅ **Character count enforcement** for proper slide formatting
✅ **Consistent voice** following style guide examples
✅ **Top 20 news + top 20 launches** for comprehensive coverage

## Usage Examples

**Simple usage:**
```
User: "Curate newsletter from November 3 to November 10"
```

**With context:**
```
User: "Use the newsletter-curator skill to create this week's newsletter from Nov 10-17"
```

The skill will automatically:
1. Extract stories from Gmail
2. Deduplicate and rank
3. Present for your review
4. Wait for your approval
5. Research top stories
6. Format everything
7. Generate final output

## Notes

- **Always wait for user approval** in Step 3 before proceeding
- **Character counts are critical** - the output must fit in slide layouts
- **Follow examples exactly** - they define the voice and style
- **Research improves quality** - don't skip web searches for top 5
- **Launches are separate** - don't mix launches with news stories
- Gmail MCP server must be configured and authenticated

## Error Handling

- If Gmail search returns no results: Ask user to verify date range or check Gmail filters
- If deduplication fails: Present raw stories and ask user to manually review
- If user doesn't approve rankings: Offer to rerank with different criteria or manual reordering
- If research fails: Continue with original summaries and note research was unavailable
- If formatting exceeds character limits: Edit ruthlessly to meet targets

---

For detailed step-by-step instructions, see `workflow-guide.md` in this skill directory.
For usage examples and expected outputs, see `examples.md` in this skill directory.
