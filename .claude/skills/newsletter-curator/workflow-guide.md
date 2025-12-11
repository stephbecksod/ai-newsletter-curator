# Newsletter Curator Workflow Guide

This document provides detailed step-by-step instructions for the newsletter curation skill.

## Prerequisites

✅ **Gmail MCP server** configured and authenticated
✅ **Project documentation** available in `docs/` directory
✅ **Python scripts** available in project root
✅ **Outputs directory** exists (created automatically if needed)

## Detailed Workflow

---

### STEP 1: Extract Stories from Gmail Newsletters

#### Purpose
Collect all story mentions from AI newsletters received during the specified date range.

#### Process

1. **Get date range from user**
   - Format: YYYY-MM-DD to YYYY-MM-DD
   - Example: "2025-11-03 to 2025-11-10"

2. **Search Gmail for newsletters**
   ```
   Use mcp__gmail__search_emails with query:
   "subject:(newsletter OR weekly OR digest) after:YYYY/MM/DD before:YYYY/MM/DD"
   ```

3. **Identify relevant newsletters**
   - Common senders: TechCrunch, The Rundown AI, Superhuman, Axios AI+, etc.
   - Look for newsletters with AI/tech content

4. **Extract stories from each newsletter**
   - Run: `python extract_newsletters.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD`
   - Script uses Claude API to parse each newsletter
   - Extracts: headline, summary, date, source, URLs

5. **Save raw output**
   - File: `outputs/raw_stories_YYYY-MM-DD_to_YYYY-MM-DD_COMPLETE.json`
   - Structure:
     ```json
     {
       "extraction_date": "YYYY-MM-DD",
       "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
       "newsletters_processed": 35,
       "stories": [
         {
           "headline": "Story headline",
           "summary": "Story summary",
           "source": "Newsletter name",
           "date": "YYYY-MM-DD",
           "urls": ["url1", "url2"]
         }
       ]
     }
     ```

6. **Report to user**
   - "Extracted 352 stories from 35 newsletters"
   - Show breakdown by newsletter if helpful

#### Common Issues

- **No newsletters found**: Verify date range and Gmail search query
- **Parsing errors**: Some newsletters have unusual formatting - skip and continue
- **Rate limits**: If hitting API limits, process in batches

---

### STEP 2: Deduplicate and Rank Stories

#### Purpose
Merge duplicate stories and rank by strategic importance using weighted editorial criteria.

#### Ranking Criteria (in priority order)

1. **"Why it matters" strength** - Strategic significance beats mechanical metrics
2. **Story type weighting:**
   - **HIGH PRIORITY** (boost ranking even with fewer mentions):
     - Platform/ecosystem battles (e.g., Amazon blocking Perplexity)
     - Controversy & safety (model removals, lawsuits, regulatory action)
     - Strategic moonshots (space data centers, AGI timelines, research breakthroughs)
     - Market structure changes (new business models, pricing disruptions)
   - **MEDIUM PRIORITY**:
     - Major product launches from leading companies
     - Large funding rounds ($100M+) or notable valuations
     - Enterprise adoption stories
   - **LOW PRIORITY** (require more mentions):
     - Infrastructure capex (pure GPU/datacenter spending)
     - Corporate governance (exec comp, board changes)
     - Incremental updates
3. **Multiple newsletter mentions** - 2+ for high-priority types, 3+ for others
4. **Headline appearance** - Was it featured as a headline?
5. **Major AI company involvement** - But not sufficient alone

#### Special Rules

**CONTROVERSY BOOST**: Stories with controversy, lawsuits, safety concerns, model removals, or regulatory action get +1-2 ranking tiers automatically.

**LAUNCH vs NEWS**:
- NOT a launch: Research projects, long-term visions (Project Suncatcher), strategic partnerships
- IS a launch: Products/features available now or within 3 months

**INFRASTRUCTURE CONTEXT**: Large deals ($25B+) are secondary unless they signal strategic shifts (e.g., diversification from single provider).

#### Process

1. **Run deduplication script**
   ```bash
   python deduplicate_and_rank.py
   ```

2. **Script automatically:**
   - Loads raw stories from Step 1 output
   - Loads style guide and examples for reference
   - Calls Claude API with ranking instructions
   - Applies deduplication logic (merge similar stories)
   - Applies weighted ranking criteria
   - Categorizes into: Top 5, Secondary 5, Next 10, Top 20 Launches, Other

3. **Output structure**
   ```json
   {
     "ranking_date": "YYYY-MM-DD",
     "top_stories": [5 stories],
     "secondary_stories": [5 stories],
     "next_10_stories": [10 stories],
     "top_20_launches": [20 launches],
     "other_launches": [remaining launches],
     "other_stories_count": 186
   }
   ```

4. **Each story includes:**
   - headline
   - summary
   - why_it_matters
   - sources (list)
   - mention_count
   - was_headline (boolean)
   - date
   - urls
   - is_launch (boolean)
   - involves_major_company (boolean)
   - companies_mentioned (list)

#### Deduplication Logic

Stories are merged if they:
- Cover the same event/announcement
- Have similar headlines (>80% similarity)
- Are from the same date or adjacent dates
- Mention the same companies/products

When merging:
- Keep the most complete summary
- Combine all sources
- Sum mention counts
- Keep all unique URLs

---

### STEP 3: Human Review and Approval

#### Purpose
Allow user to review rankings and make adjustments before expensive research phase.

#### Process

1. **Present Top 20 News Stories** in formatted layout:
   ```
   TOP 5 STORIES:
   1. Headline
      Summary: ...
      Why it matters: ...
      Mentions: X | Sources: A, B, C

   SECONDARY 5:
   6. Headline
      ...

   NEXT 10 (for review):
   11. Headline
       Why it matters: ...
   ```

2. **Present Top 20 Launches** in bullet list

3. **Ask for review:**
   - "Please review the ranked stories above."
   - "The Top 5 will be researched in depth."
   - "Would you like to make any changes?"

4. **Offer modification options:**
   - Swap stories between categories
   - Reorder within categories
   - Remove stories
   - Add specific stories from "Next 10" to top sections
   - Adjust summaries or "why it matters"

5. **Wait for explicit approval**
   - User must type something like: "approve", "looks good", "proceed", "yes"
   - DO NOT proceed without clear approval
   - If user makes changes, apply them to the JSON file

6. **Apply requested changes**
   - If user wants to swap stories, update the JSON file
   - Save updated ranking to the same file
   - Confirm changes with user

7. **Final confirmation**
   - "Ready to proceed to research and formatting?"
   - Wait for "yes" before continuing

#### Why This Step Is Critical

- **Saves API costs**: Research is expensive, only do it for approved stories
- **User preference**: User may have editorial reasons for different rankings
- **Quality control**: User can catch errors or missing stories
- **Context**: User may know about stories not captured in newsletters

**NEVER SKIP THIS STEP**

---

### STEP 4: Research Top 5 Stories

#### Purpose
Enrich the Top 5 stories with additional context, accurate details, and stronger "why it matters" sections.

#### Process for Each Top 5 Story

1. **Review original newsletter content**
   - Check all newsletters that mentioned this story
   - Note specific details, quotes, numbers

2. **Follow URLs from newsletters**
   - If story has URLs in the data, read them with WebFetch
   - Extract key facts, dates, exact numbers

3. **Gather key information:**
   - Exact dollar amounts, percentages, dates
   - Company statements or quotes
   - Strategic implications
   - Industry reaction
   - Technical details that matter

4. **Update story fields:**
   - **Summary**: Make more accurate with research findings
   - **Why it matters**: Strengthen with insights from research
   - Keep character counts in mind for later formatting

5. **Save updated data** back to ranked JSON file

#### Research Example

**Before research:**
```
Headline: Amazon blocks Perplexity's shopping agents
Summary: Amazon sent legal threats about Perplexity's Comet AI agent...
Why it matters: Platform battle over AI agent access...
```

**After research:**
```
Headline: Amazon blocks Perplexity's shopping agents
Summary: Amazon accused Perplexity of committing computer fraud as its Comet
browser agent disguises itself as a regular Chrome browser to circumvent
Amazon's security measures. Perplexity argues agents should be given the same
access as humans.
Why it matters: Are we about to see the first legal battle that determines
whether platforms can ban AI shopping agents to protect their ad business?
```

#### Research Quality Checks

✅ Numbers are accurate (not approximate)
✅ Company names are correct
✅ Dates are specific
✅ Strategic implications are clear
✅ "Why it matters" is thought-provoking

---

### STEP 5: Format Top 5 Stories

#### Purpose
Apply style guide formatting with strict character count enforcement.

#### Character Count Targets

**CRITICAL - These must be followed exactly:**

- **Headlines:** ~50 characters (range: 42-62 characters)
- **Summaries:** ~233 characters (range: 202-288 characters) — **aim for lower end of range**
- **Why it matters:** ~124 characters (range: 85-165 characters)

#### Numbers and Metrics Guidelines

**Use restraint with specific numbers.** Include them only when critical to understanding the story:

✅ **Include when critical:**
- Major dollar amounts ($10B valuation, multibillion-dollar deal)
- Key timeframes (2026, mid November, within a decade)
- Scale that defines the story (2M+ robots, 30 organizations)

❌ **Avoid excessive specifics:**
- Exact benchmark scores (use "outperformed on benchmarks" not "95% vs 71% on AIME 2025")
- Precise percentages unless critical (use "significantly higher" not "15.3% higher")
- Technical benchmark names (use "coding benchmarks" not "GPQA Diamond")
- Exact Elo scores, model version numbers, or other technical metrics
- Multiple competing numbers in one sentence

**Default to narrative over numbers** — readers want the story, not a data sheet.

**Example - Before (too many numbers):**
```
Google launched Gemini 3 Pro on November 18—just six days after GPT-5.1—achieving
a record 1,501 Elo score on LMArena, the first model to cross the 1,500 threshold.
It outperformed GPT-5.1 on math (95% vs 71% on AIME 2025), reasoning (91.9% on
GPQA Diamond), and coding benchmarks.
```

**Example - After (narrative-focused):**
```
Google's Gemini 3 Pro and OpenAI's GPT-5.1 both launched mid November, and Gemini
outperformed on math, reasoning and coding benchmarks. In a leaked memo, Altman
warned of rough vibes and that Google's progress could create temporary economic
headwinds.
```

#### Formatting Rules

**Headlines:**
- Short, crisp, high-impact
- Active voice
- Bold 1-2 key phrases using `**text**`
- No emojis
- No questions
- Example: Amazon blocks Perplexity's **shopping agents**

**Summaries:**
- 1-3 sentences, totaling ~233 characters
- Bold 2 pivotal phrases
- Clear, factual, with subtle narrative texture
- Include key mechanics of the story
- Example bold phrases: **committing computer fraud**, **same access as humans**

**Why it matters:**
- 1-2 sentences, max 3
- ~124 characters
- NO bolding
- Reflective, insightful, slightly provocative
- Often a thoughtful question or sharp observation
- Never overconfident or absolute

#### Tone & Voice

- Smart, concise, news-forward
- Slightly conversational
- Lightly opinionated in a subtle way
- Never breathless or hyped
- Equal parts analytical and curious
- Skimmable but substantive

#### Process

1. **Read style guide** (`docs/Newsletter Style Guide.md`)
2. **Review examples** (`docs/Newsletter Stories Example.md`)
3. **For each Top 5 story:**
   - Draft headline with proper character count
   - Draft summary with proper character count
   - Draft "why it matters" with proper character count
   - Add markdown bolding
   - Count characters (including spaces, excluding markdown syntax)
   - Edit ruthlessly to meet targets

4. **Verify formatting:**
   - Count characters for each element
   - Check that bold phrases are meaningful, not generic
   - Ensure voice matches examples

#### Example Output

```markdown
### Story #1
Amazon blocks Perplexity's **shopping agents**

Amazon is accusing Perplexity of **committing computer fraud** as its Comet browser agent disguises itself as a regular Chrome browser to circumvent Amazon's security measures. Perplexity argues agents should be given the **same access as humans**.

Are we about to see the first legal battle that determines whether platforms can ban AI shopping agents to protect their ad business?
```

---

### STEP 6: Format Secondary 5 Stories

#### Purpose
Create concise secondary headlines with emoji visual anchors.

#### Format

```
emoji **Entire headline in bold**
One to two sentences describing the story. No bolding in summary.
```

#### Emoji Selection Guide

- 💸 Funding/valuation/financial
- 🧠 Research/knowledge/AI models
- 🔬 Science/medical/breakthrough
- 💼 Jobs/hiring/layoffs/corporate
- 🛠️ Tools/utilities
- ⚙️ Infrastructure/cloud/compute
- 🤝 Partnerships/deals/agreements
- ⚖️ Legal/lawsuits/regulation
- 😡 Controversy/backlash/criticism

#### Rules

- **Entire headline is bold**
- Headline is very short (4-8 words)
- Summary is 1-2 sentences (~100-135 characters)
- NO bolding in summary
- NO "why it matters"
- Purely descriptive

#### Examples

```markdown
⚙️ **OpenAI and Amazon ink $38B 7-year deal**
The recent Microsoft deal enabled the company to look elsewhere for compute, with OpenAI turning to Amazon to secure more.

🤝 **Microsoft announces three major strategic deals**
A $9.7B capacity purchase from IREN, approval to ship Nvidia GPUs to UAE, and a multi-billion-dollar infrastructure deal with Lambda.

⚖️ **Seven families sue OpenAI over ChatGPT suicides**
Seven additional families filed lawsuits alleging ChatGPT's involvement in suicides and psychological harm, including one case with a four-hour conversation before death.
```

---

### STEP 7: Format Launches List

#### Purpose
Create clean, scannable list of product/feature launches.

#### Format

```
- Company launches/released/introduces product/feature description
```

#### Rules

- Simple bullet list
- One line per launch
- Past tense or present tense active voice
- NO emojis
- NO bolding
- NO "why it matters"
- Must be one single, tight sentence
- Focus on what was launched, not commentary

#### Examples

```markdown
- Adobe unveils unified AI strategy with all major models in one plan
- Adobe launches Firefly Image Model 5 with 4MP resolution
- Google Maps integrates Gemini for conversational navigation
- OpenAI launches Agent Mode for ChatGPT Atlas
- Cursor launches Composer agentic coding model
- Perplexity launches AI-powered patent search
- ChatGPT introduces "interrupt" capability
- Gemini Canvas launches with full deck creation
```

#### What NOT to include

- Don't repeat launches already in Top 5 or Secondary stories
- Don't include research projects (those are news, not launches)
- Don't include partnerships (unless it's a product launch via partnership)
- Don't include funding announcements

---

### STEP 8: Generate Final Output

#### Purpose
Compile all formatted content into final newsletter markdown file.

#### File Structure

```markdown
# AI Newsletter - [Date Range]

## TOP 5 STORIES

### Story #1
[Headline]

[Summary]

[Why it matters]

---

### Story #2
...

---

## OTHER HEADLINES

emoji **Headline**
Summary

emoji **Headline**
Summary

---

## LAUNCHES

- Launch 1
- Launch 2
- ...
```

#### Process

1. **Compile all sections:**
   - Top 5 Stories (fully formatted)
   - Other Headlines (Secondary 5, formatted)
   - Launches (bullet list)

2. **Add proper markdown structure:**
   - Title with date range
   - Section headers (## for main sections, ### for stories)
   - Horizontal rules (---) between stories
   - Proper spacing

3. **Create file:**
   - Filename: `newsletter_YYYY-MM-DD_to_YYYY-MM-DD.md`
   - Location: `outputs/` directory

4. **Save and report:**
   - Save the file
   - Show user the file path
   - Optionally show a preview

#### Final Output Example

See `examples.md` for a complete example of final output.

---

## Quality Checklist

Before considering the workflow complete, verify:

✅ All dates are correct and match user's requested range
✅ Top 5 stories have proper character counts
✅ All formatting follows style guide exactly
✅ Bolding is applied correctly (markdown syntax)
✅ Emojis are appropriate for secondary stories
✅ Launches are distinct from news stories
✅ "Why it matters" sections are thought-provoking
✅ Voice and tone match examples
✅ No duplicate stories across sections
✅ File is saved in outputs/ directory
✅ User received the final file path

---

## Troubleshooting

**Character counts are too long:**
- Edit ruthlessly - every word must earn its place
- Remove unnecessary modifiers
- Use active voice (shorter than passive)
- Look at examples for guidance

**User wants different rankings:**
- Apply changes immediately
- Don't argue with editorial judgment
- Update JSON file with new order
- Proceed with user's preferred ranking

**Research finds conflicting information:**
- Use most authoritative source
- Note discrepancy if significant
- Default to most recent information

**Style doesn't match examples:**
- Re-read examples carefully
- Focus on sentence structure and rhythm
- Match the level of editorializing
- Avoid hype words and breathless tone

**Gmail returns too many results:**
- Narrow the query to specific senders
- Filter by subject line keywords
- Process in batches by date

---

For usage examples and complete output samples, see `examples.md`.
