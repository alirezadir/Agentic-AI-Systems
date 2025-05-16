# Projects
## Example Projects (OpenAI Agents SDK)

### Tutorials and Repositories

- [Building a Specialized Weather Assistant](https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial)
- [Email Automation Agent (Tutorial)](https://aiablog.medium.com/complete-openai-agents-sdk-course-2025-a4dd68af0855)
- [Email Automation Agent (GitHub Repo)](https://github.com/nnamu-cl/agents-sdk-course-2)
- [Building a Research Assistant](https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial)
- [Automating Dispute Management with Agents SDK and Stripe API](https://cookbook.openai.com/examples/agents_sdk/dispute_agent)
- ["Agento": A Modular AI Planning System](https://github.com/dazzaji/agento6)  
    _Turn broad goals into structured, actionable plans with iterative polish._

## Example Projects to Build

### 1. Personal Study Assistant

**Description:**  
Build an AI agent system to help students manage study schedules, find resources, and summarize academic content. The system includes a scheduler, web researcher, and summarizer agent.

**Objectives:**
- Orchestrate multiple agents with distinct roles.
- Use the Responses API for web search and file processing.
- Implement agent handoffs for seamless task delegation.

**Directions:**
- **Define Agents:**  
    - Scheduler Agent: Generates study plans from user input.
    - Research Agent: Searches the web for relevant resources.
    - Summarizer Agent: Condenses findings into concise notes.
- **Set Up Inputs:**  
    Simple interface for study goals and time constraints.
- **Configure Tools:**  
    Use web search and file processing via Responses API.
- **Implement Handoffs:**  
    Scheduler → Research → Summarizer.
- **Add Guardrails:**  
    Filter for relevant sources and concise summaries.
- **Test & Debug:**  
    Use sample inputs and SDK tracing tools.
- **Enhance:**  
    Save study plans and summaries to a file.

### 2. AI-Powered Travel Planner

**Description:**  
Develop a multi-agent system that plans trips based on user preferences (budget, destination, interests).

**Objectives:**
- Explore agent collaboration and task delegation.
- Integrate real-time web search and computation tools.

**Directions:**
- **Define Agents:**  
    - Destination Agent: Researches locations.
    - Itinerary Agent: Builds day-by-day plans.
    - Budget Agent: Estimates costs.
- **Set Up Inputs:**  
    User preferences (e.g., "5-day trip to Europe under $2000").
- **Configure Tools:**  
    Web search for destinations and costs; budget calculator.
- **Implement Handoffs:**  
    Destination → Itinerary ↔ Budget.
- **Add Guardrails:**  
    Ensure safe locations and budget compliance.
- **Test & Debug:**  
    Vary inputs and use tracing.
- **Enhance:**  
    Suggest alternatives if over budget.

### 3. Customer Support Automation System

**Description:**  
Automate customer support for an online store with agents for inquiries, returns, and escalation.

**Objectives:**
- Design agents for real-world applications.
- Integrate file search and external tools.
- Implement safety mechanisms.

**Directions:**
- **Define Agents:**  
    - Inquiry Agent: Answers basic questions.
    - Returns Agent: Guides return process.
    - Escalation Agent: Handles complex queries.
- **Set Up Inputs:**  
    Text-based input for customer queries.
- **Configure Tools:**  
    File search for FAQ/product catalog; returns policy access.
- **Implement Handoffs:**  
    Inquiry ↔ Returns → Escalation.
- **Add Guardrails:**  
    Validate info and avoid unnecessary escalation.
- **Test & Debug:**  
    Use common and edge-case queries.
- **Enhance:**  
    Log interactions for analysis.

### 4. News Digest Generator

**Description:**  
Create an AI agent system that compiles a daily news digest based on user-specified topics.

**Objectives:**
- Leverage web search for real-time data.
- Practice multi-step reasoning and content filtering.

**Directions:**
- **Define Agents:**  
    - Search Agent: Finds recent articles.
    - Filter Agent: Removes irrelevant/low-quality sources.
    - Digest Agent: Summarizes articles.
- **Set Up Inputs:**  
    User topics of interest.
- **Configure Tools:**  
    Web search with citations; source credibility checks.
- **Implement Handoffs:**  
    Search → Filter → Digest.
- **Add Guardrails:**  
    Exclude outdated/unreliable sources; keep summaries brief.
- **Test & Debug:**  
    Review digests for accuracy and relevance.
- **Enhance:**  
    Email or export digest as PDF.

### 5. Code Review Assistant

**Description:**  
Develop an AI agent system to assist with code reviews by analyzing code, suggesting improvements, and generating documentation.

**Objectives:**
- Integrate file processing and external tools.
- Handle multi-step agent workflows.

**Directions:**
- **Define Agents:**  
    - Analyzer Agent: Reads code and identifies issues.
    - Suggestion Agent: Proposes fixes/optimizations.
    - Documentation Agent: Generates comments/README.
- **Set Up Inputs:**  
    Upload code files or GitHub repo links.
- **Configure Tools:**  
    File search for code; optional web search for best practices.
- **Implement Handoffs:**  
    Analyzer → Suggestion ↔ Documentation.
- **Add Guardrails:**  
    Flag only relevant issues; avoid impractical fixes.
- **Test & Debug:**  
    Use sample code and tracing.
- **Enhance:**  
    Support multiple languages or GitHub API integration.
