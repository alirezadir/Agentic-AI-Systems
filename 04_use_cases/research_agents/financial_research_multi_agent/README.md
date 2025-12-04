# Financial Research Agent Example

This example shows how you might compose a richer financial research agent using the Agents SDK. The pattern is similar to the `research_bot` example, but with more specialized subagents and a verification step.

The flow is:

1. **Planning**: A planner agent turns the end users request into a list of search terms relevant to financial analysis  recent news, earnings calls, corporate filings, industry commentary, etc.
2. **Search**: A search agent uses the builtin `WebSearchTool` to retrieve terse summaries for each search term. (You could also add `FileSearchTool` if you have indexed PDFs or 10Ks.)
3. **Subanalysts**: Additional agents (e.g. a fundamentals analyst and a risk analyst) are exposed as tools so the writer can call them inline and incorporate their outputs.
4. **Writing**: A senior writer agent brings together the search snippets and any subanalyst summaries into a longform markdown report plus a short executive summary.
5. **Verification**: A final verifier agent audits the report for obvious inconsistencies or missing sourcing.

You can run the example with:

```bash
python -m examples.financial_research_agent.main
```

and enter a query like:

```
Write up an analysis of Apple Inc.'s most recent quarter.
```

### Starter prompt

The writer agent is seeded with instructions similar to:

```
You are a senior financial analyst. You will be provided with the original query
and a set of raw search summaries. Your job is to synthesize these into a
longform markdown report (at least several paragraphs) with a short executive
summary. You also have access to tools like `fundamentals_analysis` and
`risk_analysis` to get short specialist writeups if you want to incorporate them.
Add a few followup questions for further research.
```

You can tweak these prompts and subagents to suit your own data sources and preferred report structure.
