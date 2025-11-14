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

Claude must rank stories based on:

1. Whether multiple newsletters mentioned it
2. Whether it appeared as a headline anywhere
3. Whether it involves a major AI company \(OpenAI, Anthropic, Google/Gemini, Meta, xAI, Amazon, Microsoft, etc\.\)
4. Whether it is truly significant \(use judgment—big companies release lots of minor things, small companies do really amazing things, and sometimes news is not company specific\)
5. Whether a casual AI reader would need to know this to feel “caught up” for the week

For examples of story selection for each section, refer to the Newsletter Story Example document\. In this document, there are 4 weeks worth of stories\. The earliest two weeks do not have launches, as I added them later\. Review this to understand the type of stories I want to emphasize\.

Claude should produce:

- __Top 5 stories__
- __Next ~4–5 secondary stories__
- __Launch list: a list of all launches not listed in the stories above__
- Everything else that was in the news but not listed in the three sections above

Each story in each section should have a brief summary to describe the news event, and one sentence on why it matters\.

The output of this step should be a second list of deduped, ranked stories with summaries\. The stories should be categorized into Top Stories, Other Headlines, Launches, and Other\.  


## <a id="_jrk8d75xkyax"></a>__STEP 3: Human Review of Ranked List__

Claude generates a ranked list including:

- Final headline
- Summary
- One\-sentence “why it matters”

Claude presents the full list from step 2, categorized as indicated, to you to review and adjust\. You may reorder or edit as needed\.

Claude must __wait for your approval__ before producing final formatted output\.

## <a id="_kpnkttf8f4bn"></a>__STEP 4: Research__

Once the story list is approved, Claude should research each of the top 5 stories by reviewing the information in the newsletters about the stories, following any URLs that link to deeper stories, and doing a web search and reviewing 1\-2 other articles about these stories, if available\. Once Claude has completed research for these stories, it should review the summaries and why it matters and rewrite, capturing the most critical components of the stories for the newsletter\. The original copy may not change based on this research, but if new or interesting viewpoints or facts are uncovered, consider updating\.

## <a id="_8y5h6x9nwld8"></a>__STEP 5: Top 5 Story Formatting__

After the ranking is approved and the top story research is complete, generate the content for the top stories\. Follow the Newsletter Style Guide document, section 1 on “Top Stories Style Guide \(Headline \+ Summary \+ Why It Matters\)\. You can also reference the News Stories Example document to see the full set of top stories in the past and understand what the content looked like\.

Each story must have a headline, a summary, and a why it matters section\.

### <a id="_yrc3k73loqfn"></a>__Bolding rules__

- Headlines: ideally 1 bold phrase, max 2
- Summary: ideally 2 bold phrases, max 2
- Bold phrases should be key words, actions, or companies

### <a id="_fh9nqgcfir51"></a>__Slide layout constraints Claude must write to__

- Headline fits exactly 3 lines \(Playfair Display Medium 60 → 9\.31in x 5\.21in box\)
- Summary is 4–6 lines \(Source Sans Pro 25 → 8\.52in width\)
- Why it matters is 2 lines, max 3 \(Arial 20 → 8\.52in width\)

The output should be the 5 stories with a headline, summary, and “why it matters” section, following the bolding and formatting rules above and following the guidelines in the Newsletter Style Guide\.

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

