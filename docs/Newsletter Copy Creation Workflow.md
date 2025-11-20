# <a id="_y8lp0843amhi"></a>__Newsletter Copy Creation Workflow__

### <a id="_bdaxqa74mf33"></a>__Overall Goal__

You receive daily AI newsletters from specific email senders\. When I run a command that we create, I want Claude to do the following:

1. Read all your newsletters for the dates specified
2. Extract only the *news* content
3. Deduplicate and consolidate overlapping stories
4. Rank the stories by importance
5. Present the ranked list to you for review
6. After you approve the order, fully format:
	- The Top 5 stories
	- The next 4–5 secondary stories
	- All additional launches from the week
7. Output the full finalized copy exactly as it will appear in your Monday AI news deck\.

## <a id="_miv45sejykib"></a>__STEP 1: Ingest Newsletters and Extract News__

Claude reads newsletters only from these sender email addresses:

- superhuman@mail\.joinsuperhuman\.ai
- ai\.plus@axios\.com
- newsletters@techcrunch\.com
- thatstartupguy@mail\.beehiiv\.com
- news@daily\.therundown\.ai
- startupintros@mail\.beehiiv\.com

Claude pulls in *every* newsletter from these senders throughout the dates specified\.

For each newsletter, Claude should:
1. Extract the entire newsletter content
2. Read through all the content carefully
3. Identify and extract __only the news stories__—not tips, tools, tutorials, prompts, or opinion content

Some newsletters are pure news; some are mixed\. Claude must detect which items in each newsletter are actually news\. News can include but not be limited to new partnerships, new product or features, new fundraising or valuations\. I can also provide a list of the news stories I've included recently for reference\.

For each news story Claude finds, it should add a raw entry to a weekly list with:

- Headline \(from newsletter or rewritten for clarity\)
- Newsletter source \(consistent naming each week\)
- Date of the newsletter \(email received date\)
- Summary \(1–3 sentences\)
- URL to the news story, if available \(but do not spend extra energy or resources looking for this as it will not exist for many\)

No deduplication here—this is just raw extraction\.

This should be one list that is produced \- the full list of all news stories, the sources, the summaries, the dates, and the URL if applicable\. This list does not get overridden by the next steps, but is a stand alone list output\.

## <a id="_zggnnytg87g8"></a>__STEP 2: Weekly Deduplication & Ranking__

Once the first list has been created, we need to run a deduplication and ranking step\. This should produce a second document\.

Claude should:

### <a id="_xwlvs7ooxafq"></a>__Deduplicate__

Group overlapping stories across newsletters into a single canonical story\. A cluster is a duplicate if it reports on the same underlying event\.

When merging duplicates, Claude keeps:

- Combined list of sources
- Count of how many newsletters mentioned it
- Whether it was a headline in any newsletter
- A clean final headline
- A unified summary
- URLs
- The earliest date among the duplicates

Claude must also tag whether each story is a __launch__ \(e\.g\., new model, company, product, feature, integration, partnership tied to new capability\)\.

### <a id="_nf1t21jm5z03"></a>__Ranking__

Claude must rank stories using a __weighted, editorial approach__ that prioritizes strategic significance over mechanical metrics\.

#### __Primary Ranking Criteria \(in priority order\):__

1. __"Why it matters" strength__ — Does this story signal something bigger about the future of AI, platform power, market structure, or societal impact?
2. __Story type weighting__ — Apply category\-specific priorities \(see below\)
3. __Multiple newsletter mentions__ — 2\+ mentions for high\-priority story types, 3\+ for others
4. __Headline appearance__ — Was it featured as a headline in any newsletter?
5. __Major AI company involvement__ — But not sufficient alone for top ranking

#### __Story Type Priorities:__

__HIGH\-PRIORITY STORY TYPES__ \(boost ranking even with fewer mentions\):

- __Platform/ecosystem battles__ — Stories about platforms blocking or enabling AI \(e\.g\., Amazon blocking Perplexity, app store policies, API access restrictions\)
- __Controversy & safety__ — Model removals, lawsuits, ethical concerns, regulatory action, AI failures with consequences
- __Strategic moonshots__ — Long\-term vision announcements \(e\.g\., space data centers, AGI timelines, fundamental research breakthroughs\)
- __Market structure changes__ — New business models, pricing disruptions, competitive dynamics shifts, strategic partnerships that reshape industries

__MEDIUM\-PRIORITY STORY TYPES__ \(standard newsworthiness criteria\):

- __Major product launches__ — Significant new capabilities, models, or features from leading companies
- __Funding & valuations__ — Large rounds \($100M\+\) or notable valuations that signal market direction
- __Enterprise adoption__ — Major companies adopting AI in transformative ways

__LOWER\-PRIORITY STORY TYPES__ \(require more mentions to rank highly\):

- __Infrastructure capex__ — Pure spending announcements on GPUs, data centers, cloud deals \(unless they signal strategic shifts like diversification away from a single provider\)
- __Corporate governance__ — Executive compensation, board changes \(unless directly AI\-related\)
- __Incremental updates__ — Features that are evolutionary, not revolutionary

#### __Special Rules:__

__CONTROVERSY BOOST:__ Stories involving controversy, lawsuits, safety concerns, model removals, or regulatory action automatically get \+1\-2 ranking tiers, even with lower mention counts\. These stories signal important "what could go wrong" narratives that readers need to understand\.

__LAUNCH vs\. NEWS DISTINCTION:__

- __NOT a launch:__ Research projects, long\-term visions \(Project Suncatcher\), strategic partnerships that change market structure, moonshot announcements without near\-term availability
- __IS a launch:__ Products/features available now or within 3 months, API releases, model updates, tactical integrations

__INFRASTRUCTURE CONTEXT:__ Large GPU/cloud deals \(even $25B\+\) should be ranked as secondary stories unless they represent strategic shifts\. The dollar amount alone is not newsworthy—the strategic implication is\.

For examples of story selection for each section, refer to the Newsletter Story Example document\. In this document, there are 4 weeks worth of stories\. The earliest two weeks do not have launches, as I added them later\. Review this to understand the type of stories I want to emphasize\.

#### __Output Categories:__

Claude should produce:

__News Stories \(Top 20\):__
- __Top 5 stories__
- __Secondary 5 stories__ \(the next 5 highest\-ranked after top 5\)
- __Next 10 stories__ \(ranked 11\-20, for human review\)

__Launches \(Top 20\):__
- __Top 20 launches__ ranked using the same weighted approach as news stories
- Apply the same ranking criteria \(strategic significance, mention count, major companies, etc\.\)
- Focus on launches with the most significant impact on the AI ecosystem

__Other:__
- __Remaining launches__ \(all launches not in top 20\)
- __Everything else__ that was in the news but not listed in the sections above

Each story/launch in the top 20 should have:

- Final headline
- Brief summary describing the news event or launch
- One sentence on "why it matters"

The output of this step should be a second list of deduped, ranked stories with summaries\. The stories should be categorized into Top 5, Secondary 5, Next 10, Top 20 Launches, Other Launches, and Other Stories\.  


## <a id="_jrk8d75xkyax"></a>__STEP 3: Human Review of Ranked List__

Claude generates a ranked list of the __top 20 stories__ including:

- Final headline
- Summary
- One\-sentence "why it matters"

Claude presents the top 20 stories \(Top 5 \+ Secondary 5 \+ Next 10\) from step 2, clearly categorized, to you to review and adjust\. This allows you to see beyond the immediate top 10 and make better editorial decisions about which stories belong in the final output\.

You may reorder, promote/demote stories between categories, or edit as needed\.

Claude must __wait for your approval__ before producing final formatted output\.

## <a id="_kpnkttf8f4bn"></a>__STEP 4: Research__

Once the story list is approved, Claude should research each of the top 5 stories by reviewing the information in the newsletters about the stories, following any URLs that link to deeper stories, and doing a web search and reviewing 1\-2 other articles about these stories, if available\. Once Claude has completed research for these stories, it should review the summaries and why it matters and rewrite, capturing the most critical components of the stories for the newsletter\. The original copy may not change based on this research, but if new or interesting viewpoints or facts are uncovered, consider updating\.

## <a id="_8y5h6x9nwld8"></a>__STEP 5: Top 5 Story Formatting__

After the ranking is approved and the top story research is complete, generate the content for the top stories\. Follow the Newsletter Style Guide document, section 1 on "Top Stories Style Guide \(Headline \+ Summary \+ Why It Matters\)\. You can also reference the News Stories Example document to see the full set of top stories in the past and understand what the content looked like\.

Each story must have a headline, a summary, and a why it matters section\.

### <a id="_yrc3k73loqfn"></a>__Bolding rules__

- Headlines: ideally 1 bold phrase, max 2
- Summary: ideally 2 bold phrases, max 2
- Bold phrases should be key words, actions, or companies

### <a id="_character_count_targets"></a>__Character Count Targets__

__CRITICAL:__ Stories must be concise\. Target these character counts based on historical examples:

- __Headlines:__ ~50 characters \(range: 42\-62 characters\)
- __Summaries:__ ~233 characters \(range: 202\-288 characters\)
- __Why it matters:__ ~124 characters \(range: 85\-165 characters\)

These targets ensure content fits properly in the slide layout without being too verbose\. When drafting, count characters and edit ruthlessly to stay within these ranges\.

### <a id="_fh9nqgcfir51"></a>__Slide layout constraints Claude must write to__

- Headline fits exactly 3 lines \(Playfair Display Medium 60 → 9\.31in x 5\.21in box\)
- Summary is 4–6 lines \(Source Sans Pro 25 → 8\.52in width\)
- Why it matters is 2 lines, max 3 \(Arial 20 → 8\.52in width\)

The output should be the 5 stories with a headline, summary, and "why it matters" section, following the bolding and formatting rules above and following the guidelines in the Newsletter Style Guide\.

## <a id="_hi6kyae9sdvl"></a>__STEP 6: Secondary Stories Formatting__

Claude formats the next 4–5 stories\. Follow the Newsletter Style Guide document, section 2 “Secondary Stories Style Guide \(Emoji \+ Headline \+ 1\-2 Sentences\)\. The stories should have:

__Headline__

- Starts with an emoji
- Entire headline is bold
- One line only

__Summary__

- 1–2 sentences
- No bolding  


Example:

\*\*💸 Mercor hits $10B valuation\*\*

The company, which connects AI labs like ChatGPT to domain experts to train foundation models, raised a $350M Series C\.

## <a id="_es90ldn1ss8j"></a>__STEP 7: Launches List__

Claude creates a bullet list of all weekly launches\. Follow the Newsletter Style Guide document, section 3 “Launches Section Style Guide \(Bullet List\),  that:

- Are tagged as is\_launch = true
- Did NOT appear in the Top 9–10 stories

Format:

\- OpenAI launches Company Knowledge

\- Adobe launches AI assistance for Express and Photoshop

\- Anthropic released Claude for Excel

Rules:

- One line per bullet
- No emojis
- No bolding
- No commentary

## <a id="_ry9i3g6vhg5"></a>__STEP 8: Final Output — FULL COPY__

Claude must output:

### <a id="_4qtrxn9mj051"></a>__1\. Top Stories__

Each story contains:

- Headline \(Markdown bold inside\)
- Summary \(with bolding\)
- Why it matters \(no bold\)

### <a id="_bbn6wrfw0acu"></a>__2\. Other noteworthy news__

4–5 secondary stories with emoji bolded headlines \+ short summaries

### <a id="_86qig0kp5f3t"></a>__3\. Launches this week__

Bullet list exactly as described

The final output is __fully formatted copy__, ready to paste into your deck\. It should be formatted like the November 10, 2025 examples in the Newsletter Story Example document\.

## <a id="_sencbpaysghz"></a>__Final Notes__

Keep in mind the following as you go through this process:

- You should output the following:
	- A full list, not deduplicated, of all news stories, unranked, with headline, summary, date, source, and URL if applicable
	- A ranked, deduplicated list of news stories for review
	- Once the final list is approved, a final copy output of all the news stories, fully formatted
- You should refer to the Newsletter Style Guide for how to write and format each story
- You should refer to the Newsletter Stories Example document for:
	- Real examples of formatting
	- Story selection examples

