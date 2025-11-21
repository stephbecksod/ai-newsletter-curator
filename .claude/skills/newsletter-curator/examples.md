# Newsletter Curator - Usage Examples

This document provides complete examples of using the newsletter-curator skill, including expected inputs, outputs, and interactions.

---

## Example 1: Basic Usage

### User Input

```
User: "Curate newsletter from November 3 to November 10, 2025"
```

### Step 1: Extract Stories from Gmail

**Assistant Action:**
```
Searching Gmail for newsletters between 2025-11-03 and 2025-11-10...
Running: python extract_newsletters.py --start-date 2025-11-03 --end-date 2025-11-10
```

**Output:**
```
✓ Extracted 352 stories from 35 newsletters
✓ Saved to: outputs/raw_stories_2025-11-03_to_2025-11-10_COMPLETE.json

Newsletters processed:
- Superhuman AI: 7 newsletters
- Axios AI+: 5 newsletters
- TechCrunch: 8 newsletters
- The Rundown AI: 7 newsletters
- Startup Intros: 5 newsletters
- That Startup Guy: 3 newsletters
```

### Step 2: Deduplicate and Rank Stories

**Assistant Action:**
```
Running: python deduplicate_and_rank.py
```

**Output:**
```
✓ Deduplicated 352 stories to 186 unique stories
✓ Ranked stories using weighted editorial criteria
✓ Applied controversy boost to 12 stories
✓ Identified 64 launches (20 ranked as top launches)
✓ Saved to: outputs/ranked_stories_2025-11-03_to_2025-11-10.json

Categories:
- Top 5 stories
- Secondary 5 stories
- Next 10 stories
- Top 20 launches
- 44 other launches
- 122 other stories
```

### Step 3: Human Review

**Assistant Presentation:**
```markdown
## TOP 5 STORIES FOR REVIEW

**1. Amazon blocks Perplexity's shopping agents**
Summary: Amazon sent legal threats about Perplexity's Comet AI agent disguising itself as Chrome to bypass security measures.
Why it matters: First major legal battle over whether platforms can ban AI shopping agents to protect their ad business.
Sources: The Rundown AI, TechCrunch | Mentions: 2 | Headline: Yes

**2. Anthropic projects $70B in revenue by 2028 driven by B2B model**
Summary: Anthropic expects positive cash flow by 2027 and $3.8B in API revenue this year—double OpenAI's $1.8B from API sales.
Why it matters: Defining success in AI could be taking a turn towards methodical growth to profitability vs the mad-dash to AGI.
Sources: Axios AI+, Superhuman | Mentions: 2

**3. Apple pays Google $1 billion annually to power Siri with Gemini**
Summary: Apple finalized a $1B annual deal with Google to use a custom 1.2T parameter version of Gemini for next-generation Siri.
Why it matters: Apple has historically been self-reliant, but is losing the AI arms race, forcing them to turn to outside support.
Sources: TechCrunch, The Rundown AI, Superhuman | Mentions: 3 | Headline: Yes

**4. OpenAI denies bailout pitch after CFO's comments**
Summary: Following comments by CFO Sarah Friar suggesting the U.S. government should "backstop" infrastructure loans, CEO Sam Altman clarified the company "does not have or want government guarantees."
Why it matters: Wall Street is getting antsy about an AI bubble, so government bailout comments from OpenAI's CFO cause nerves.
Sources: Axios AI+, TechCrunch | Mentions: 2

**5. Project Suncatcher: Google's AI data centers in space**
Summary: Google publicly revealed Project Suncatcher, a "moonshot" initiative to deploy solar-powered satellite constellations with TPUs and optical links.
Why it matters: Space-based data centers would not have the same energy drains or emissions as planetary ones—a potential win for the environment.
Sources: The Rundown AI | Mentions: 1 | Headline: Yes

## SECONDARY 5 STORIES

6. OpenAI and Amazon ink $38B 7-year deal
7. Microsoft announces three major strategic deals
8. Perplexity to pay Snap $400M to power search
9. Seven families sue OpenAI over ChatGPT suicides
10. Google removes Gemma from AI studio

## NEXT 10 STORIES (for review)

11. Meta announces AI research breakthroughs
12. Anthropic releases safety framework
... (remaining stories)

## TOP 20 LAUNCHES

- Adobe unveils unified AI strategy with all major models in one plan
- Adobe launches Firefly Image Model 5 with 4MP resolution
- Google Maps integrates Gemini for conversational navigation
... (remaining 17 launches)

---

Please review the ranked stories above.
The Top 5 will be researched in depth.
Would you like to make any changes?
```

**User Response:**
```
User: "Looks good, proceed"
```

### Step 4: Research Top 5 Stories

**Assistant Action:**
```
Researching Story #1: Amazon blocks Perplexity's shopping agents
- Searching web for additional articles...
- Reading TechCrunch article...
- Reading Axios coverage...

Key findings:
- Amazon accused Perplexity of "committing computer fraud"
- Comet agent disguises itself as regular Chrome browser
- Perplexity argues agents should get "same access as humans"

Updated summary with research findings.

[Continues for all 5 stories...]

✓ Research complete for all Top 5 stories
✓ Updated summaries with accurate details and strategic insights
```

### Step 5-7: Format All Stories

**Assistant Action:**
```
Formatting Top 5 stories...
- Character counts: Headlines ~50, Summaries ~233, Why it matters ~124
- Applied markdown bolding
- Matching voice from examples

Formatting Secondary 5 stories...
- Added emojis: ⚙️ 🤝 💸 ⚖️ 😡
- Bold headlines, no bolding in summaries

Formatting launches list...
- Simple bullet list, no emojis or bolding
- One line per launch
```

### Step 8: Final Output

**Assistant Response:**
```
Newsletter complete! Saved to: outputs/newsletter_2025-11-03_to_2025-11-10.md

Preview:

# AI Newsletter - November 3-10, 2025

## TOP 5 STORIES

### Story #1
Amazon blocks Perplexity's **shopping agents**

Amazon is accusing Perplexity of **committing computer fraud** as its Comet browser agent disguises itself as a regular Chrome browser to circumvent Amazon's security measures. Perplexity argues agents should be given the **same access as humans**.

Are we about to see the first legal battle that determines whether platforms can ban AI shopping agents to protect their ad business?

---

[Full formatted newsletter continues...]
```

---

## Example 2: User Makes Changes During Review

### Step 3: Human Review

**User Response:**
```
User: "I want to swap story 3 and story 5, and move story 9 into the secondary 5"
```

**Assistant Action:**
```
Updating rankings:
- Swapping Story #3 (Apple-Google) with Story #5 (Project Suncatcher)
- Moving Story #9 (OpenAI suicides lawsuits) from next 10 to position 10 in secondary stories
- Adjusting other stories accordingly

Updated Top 5:
1. Amazon blocks Perplexity's shopping agents
2. Anthropic projects $70B in revenue
3. Project Suncatcher: Google's AI data centers in space
4. OpenAI denies bailout pitch
5. Apple pays Google $1 billion for Siri

Updated Secondary 5:
6. OpenAI and Amazon ink $38B deal
7. Microsoft announces three major deals
8. Perplexity to pay Snap $400M
9. Google removes Gemma from AI studio
10. Seven families sue OpenAI over ChatGPT suicides

Are you ready to proceed to research and formatting?
```

**User Response:**
```
User: "Yes, proceed"
```

---

## Example 3: Edge Case - No Newsletters Found

### Step 1: Extract Stories

**User Input:**
```
User: "Curate newsletter from December 25 to December 31, 2025"
```

**Assistant Action:**
```
Searching Gmail for newsletters between 2025-12-25 and 2025-12-31...
```

**Output:**
```
⚠️ Warning: No newsletters found for the specified date range.

Possible reasons:
- Date range is in the future or outside newsletter subscription period
- Gmail search query didn't match any emails
- Newsletters may be in different folders/labels

Would you like to:
1. Verify the date range
2. Check Gmail filters
3. Manually provide newsletter message IDs
```

---

## Example 4: Edge Case - Research Unavailable

### Step 4: Research

**Assistant Action:**
```
Researching Story #3: [Story headline]
- Attempting web search...
⚠️ Web search returned no results
- Checking original newsletter URLs...
⚠️ URLs not accessible

Continuing with original summary from newsletters.
Note: Research was unavailable for this story.

Proceeding to next story...
```

---

## Example 5: Character Count Adjustment

### Step 5: Format Top Stories

**First Draft (TOO LONG):**
```
Headline: Amazon takes legal action to block Perplexity's AI-powered shopping agents (72 chars - TOO LONG)
Summary: Amazon has sent cease-and-desist letters accusing Perplexity of committing computer fraud as its Comet browser agent disguises itself as a regular Chrome browser in order to circumvent Amazon's security measures and access the platform. Perplexity has responded by arguing that AI agents should be given the same level of access as human users. (350 chars - TOO LONG)
```

**Edited Version (CORRECT):**
```
Headline: Amazon blocks Perplexity's **shopping agents** (49 chars ✓)
Summary: Amazon is accusing Perplexity of **committing computer fraud** as its Comet browser agent disguises itself as a regular Chrome browser to circumvent Amazon's security measures. Perplexity argues agents should be given the **same access as humans**. (233 chars ✓)
```

---

## Expected File Outputs

### After Step 1:
```
outputs/raw_stories_2025-11-03_to_2025-11-10_COMPLETE.json
```

Contains all extracted stories with:
- headline
- summary
- source
- date
- urls (if available)

### After Step 2:
```
outputs/ranked_stories_2025-11-03_to_2025-11-10.json
```

Contains deduplicated and ranked stories with:
- top_stories (5)
- secondary_stories (5)
- next_10_stories (10)
- top_20_launches (20)
- other_launches (remaining)
- other_stories_count

### After Step 8:
```
outputs/newsletter_2025-11-03_to_2025-11-10.md
```

Contains fully formatted newsletter ready for presentation.

---

## Complete Newsletter Output Example

For a complete example of the final formatted newsletter output, see:
`outputs/newsletter_2025-11-03_to_2025-11-10.md`

This example includes:
- 5 fully formatted top stories with character-count-compliant headlines, summaries, and "why it matters"
- 5 secondary stories with emojis and bold headlines
- 20 launches in bullet format

---

## Troubleshooting Examples

### Problem: "The rankings don't match my preferences"

**Solution:**
During Step 3 (Human Review), tell Claude exactly what changes you want:
```
"Swap story 2 and story 7"
"Remove story 5 and promote story 11 to top 5"
"Move story 15 to secondary stories"
```

Claude will apply your changes and wait for approval before continuing.

### Problem: "Character counts are still too long"

**Solution:**
Ask Claude to re-edit specific stories:
```
"Story #3 headline is too long, please shorten to ~50 characters"
"The summary for story #1 needs to be under 240 characters"
```

Reference the character count targets:
- Headlines: ~50 chars (range: 42-62)
- Summaries: ~233 chars (range: 202-288)
- Why it matters: ~124 chars (range: 85-165)

### Problem: "Gmail authentication failed"

**Solution:**
Verify Gmail MCP server configuration:
```bash
# Check MCP server status
npx @gongrzhe/server-gmail-autoauth-mcp

# Re-authenticate if needed
```

Ensure Gmail MCP server is properly configured in Claude Code settings.

---

## Notes

- Always provide explicit date ranges in YYYY-MM-DD format
- The human review step is mandatory - Claude will wait for your approval
- You can make unlimited changes during the review step
- Research improves quality but continues even if some lookups fail
- Character count targets are critical for slide formatting
- All outputs are saved to the `outputs/` directory

---

For detailed step-by-step instructions, see `workflow-guide.md`.
For the complete skill definition, see `SKILL.md`.
