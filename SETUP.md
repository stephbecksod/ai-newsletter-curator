# Complete Setup Guide for Newsletter Curator Skill

## Prerequisites

Before you start, you'll need:

- **Claude Code** installed and configured
- **Python 3.11+** installed
- **Gmail account** with newsletters you want to curate
- **Anthropic API key** (for Claude API calls during extraction/ranking)
- **Node.js and npm** (for Gmail MCP server)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/stephbecksod/ai-newsletter-curator.git
cd ai-newsletter-curator
```

---

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

The project requires:
- `anthropic` - Claude API client
- `python-dotenv` - Environment variable management
- `pyyaml` - Configuration file parsing
- `google-auth` and Gmail API libraries

---

## Step 3: Set Up Gmail MCP Server

### Option A: Auto-Authentication MCP (Recommended)

This uses a community MCP server that handles Gmail authentication automatically:

1. **Install the Gmail MCP server:**
   ```bash
   npm install -g @gongrzhe/server-gmail-autoauth-mcp
   ```

2. **Run the authentication:**
   ```bash
   npx @gongrzhe/server-gmail-autoauth-mcp
   ```

   This will:
   - Open a browser window for Google OAuth
   - Ask you to grant Gmail read permissions
   - Save credentials to `~/.gmail-mcp/` directory

3. **Configure Claude Code to use the MCP server:**

   Edit your Claude Code MCP settings file:
   - **macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

   Add this configuration:
   ```json
   {
     "mcpServers": {
       "gmail": {
         "command": "npx",
         "args": ["@gongrzhe/server-gmail-autoauth-mcp"]
       }
     }
   }
   ```

4. **Restart Claude Code** to load the MCP server

### Option B: Manual Gmail API Setup

If you prefer to set up your own Gmail API credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`
6. Place in project root directory
7. Run `python gmail_text_extractor.py` once to authenticate

---

## Step 4: Configure Your Newsletter Sources

Edit `config.yaml` to specify which newsletters to monitor:

```yaml
# Newsletter Sources (Gmail sender addresses)
newsletter_sources:
  - superhuman@mail.joinsuperhuman.ai
  - ai.plus@axios.com
  - newsletters@techcrunch.com
  - thatstartupguy@mail.beehiiv.com
  - news@daily.therundown.ai
  - startupintros@mail.beehiiv.com
  # Add your own newsletter senders here
```

**How to find newsletter sender addresses:**
1. Open Gmail
2. Find a newsletter you want to include
3. Click "Show original" or view the email headers
4. Look for the "From:" address
5. Add it to the list above

**Tips:**
- Use the exact sender email address (not display name)
- Include newsletters that consistently cover your topic (AI, tech, etc.)
- Start with 5-10 quality sources; you can add more later
- Make sure you're subscribed and receiving these newsletters

---

## Step 5: Set Up Your Anthropic API Key

1. **Get your API key** from [Anthropic Console](https://console.anthropic.com/)

2. **Create a `.env` file** in the project root:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-api-key-here
   ```

3. **Keep this file secure** - it's already in `.gitignore`

---

## Step 6: Verify the Skill Is Available

The skill is located in `.claude/skills/newsletter-curator/` and should be automatically discovered by Claude Code.

**Verify the skill structure:**
```
.claude/skills/newsletter-curator/
├── SKILL.md              # Main skill definition
├── workflow-guide.md     # Detailed step-by-step guide
└── examples.md           # Usage examples
```

**Check SKILL.md frontmatter:**
```yaml
---
name: newsletter-curator
description: Automates the complete AI newsletter curation workflow...
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch, TodoWrite, mcp__gmail__search_emails, mcp__gmail__read_email]
---
```

---

## Step 7: Test the Setup

Before running the full skill, test each component:

### Test 1: Gmail MCP Connection

Open Claude Code and ask:
```
Search my Gmail for newsletters from the past week
```

If successful, you should see newsletter results.

### Test 2: Python Scripts

Test extraction manually:
```bash
python extract_all_newsletters.py --start-date 2025-11-17 --end-date 2025-11-20
```

You should see:
- Gmail authentication
- Newsletter fetching progress
- Story extraction with Claude API
- Output file created in `outputs/`

### Test 3: Deduplication

```bash
python deduplicate_and_rank.py
```

Should automatically detect the latest raw stories file and generate ranked output.

---

## Step 8: Using the Skill

Once everything is set up, you can use the skill by simply asking Claude Code:

```
Curate newsletter from November 24 to December 1, 2025
```

Or:

```
Create my AI newsletter for this week (Nov 24-Dec 1)
```

The skill will automatically:
1. ✅ Search Gmail for newsletters in your date range
2. ✅ Extract stories using Claude API
3. ✅ Deduplicate and rank using weighted editorial criteria
4. ✅ Present top 20 stories + top 20 launches for your review
5. ⏸️ **Wait for your approval**
6. ✅ Research the top 5 stories after approval
7. ✅ Format everything with strict character counts
8. ✅ Generate final newsletter markdown file

---

## Step 9: Customize the Workflow (Optional)

### Adjust Ranking Criteria

Edit `docs/Newsletter Copy Creation Workflow.md` to modify:
- Story type priorities (high/medium/low)
- Controversy boost rules
- Launch vs news distinction
- Major AI companies list

Then update `config.yaml`:
```yaml
# Major AI companies (for ranking)
major_ai_companies:
  - OpenAI
  - Anthropic
  - Google
  - Add your own focus companies
```

### Adjust Character Count Targets

Edit character count targets in the workflow document if your presentation format differs:

Current targets:
- Headlines: ~50 characters (42-62 range)
- Summaries: ~233 characters (202-288 range)
- Why it matters: ~124 characters (85-165 range)

### Modify Style and Voice

Edit `docs/Newsletter Style Guide.md` to define your preferred:
- Tone (currently: smart, concise, news-forward)
- Bolding patterns
- Emoji usage for secondary stories
- Launch formatting

---

## Step 10: File Outputs

After running the skill, you'll find:

```
outputs/
├── raw_stories_YYYY-MM-DD_to_YYYY-MM-DD_COMPLETE.json    # All extracted stories
├── ranked_stories_YYYY-MM-DD_to_YYYY-MM-DD.json          # Ranked and deduplicated
├── newsletter_YYYY-MM-DD_to_YYYY-MM-DD.md                # Final formatted output
└── debug_dedup_response.txt                               # Claude API debug output
```

---

## Troubleshooting

### "No newsletters found"

**Check:**
- Date range is correct (use YYYY-MM-DD format)
- Newsletter sender addresses in `config.yaml` match exactly
- You have emails from those senders in the date range
- Gmail MCP server is running (`mcp__gmail__search_emails` tool available)

**Fix:**
Test Gmail search manually:
```
Search Gmail for emails from ai.plus@axios.com after 2025-11-17
```

### "Anthropic API timeout"

**Check:**
- API key is set in `.env` file
- You have sufficient API credits
- Network connection is stable

**Fix:**
The scripts already have 600s timeout. If still failing, check Anthropic status page.

### "Permission denied on Gmail"

**Check:**
- You completed OAuth flow
- Credentials are in `~/.gmail-mcp/` directory
- MCP server is configured in Claude Code settings

**Fix:**
Re-run authentication:
```bash
npx @gongrzhe/server-gmail-autoauth-mcp
```

### "Stories don't match my preferences"

**Adjust:**
1. Edit ranking criteria in `docs/Newsletter Copy Creation Workflow.md`
2. During Step 3 (Human Review), you can reorder any stories
3. The skill always waits for your approval before research

### "Character counts are off"

**Check:**
- You're counting characters correctly (including spaces, excluding markdown)
- Examples in `docs/Newsletter Stories Example.md` for reference

**Fix:**
Edit stories during the review step or adjust targets in workflow documentation.

---

## Tips for Best Results

1. **Consistent Newsletter Sources:** Subscribe to 5-10 quality newsletters that cover your topic comprehensively

2. **Weekly Cadence:** Run the skill weekly to maintain consistent coverage and avoid overwhelming data

3. **Editorial Review:** Always review the rankings in Step 3 - the AI is good but your judgment matters

4. **Customize Rankings:** After a few weeks, adjust the ranking criteria to match your editorial preferences

5. **Monitor Costs:** Claude API calls cost money. The skill is optimized but processing 30+ newsletters can use significant tokens

6. **Version Control:** Keep your customizations in git so you can track what works

7. **Date Ranges:** Use Sunday-Saturday or Monday-Sunday for clean weekly boundaries

---

## Cost Estimates

Typical costs per newsletter curation (assuming 20 newsletters, 200 stories):

- **Extraction:** ~$2-5 (Claude API for parsing newsletters)
- **Ranking:** ~$1-2 (Claude API for deduplication/ranking)
- **Research:** ~$0.50-1 (Web searches for top 5 stories)

**Total per week:** ~$3.50-8 depending on newsletter volume

**Ways to reduce costs:**
- Reduce number of newsletter sources
- Shorten date ranges
- Skip research step if needed (edit skill)

---

## Support

- **Skill Issues:** Check `.claude/skills/newsletter-curator/workflow-guide.md`
- **Gmail MCP:** [GitHub repo](https://github.com/gongrzhe/server-gmail-autoauth-mcp)
- **Claude Code:** [Documentation](https://docs.anthropic.com/claude-code)
- **Project Issues:** [GitHub Issues](https://github.com/stephbecksod/ai-newsletter-curator/issues)

---

## Example Workflow

**Monday morning:**
```
You: "Curate newsletter from November 24 to December 1"

Claude: [Extracts 250 stories from 18 newsletters]
        [Deduplicates to 130 unique stories]
        [Presents top 20 for review]

You: "Move story 8 to position 4, proceed"

Claude: [Researches top 5 stories]
        [Formats everything]
        [Generates final newsletter]

Output: newsletter_2025-11-24_to_2025-12-01.md ready for your deck!
```

That's it! You now have a complete automated newsletter curation system.
