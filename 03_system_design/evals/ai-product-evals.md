
## AI Product Evaluation: Practical Systems for LLM Products (Hamel Husain)
Reference: [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

This summary distills key lessons from Hamel Husain's [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) on building robust evaluation systems for LLM-powered products.


### 1. Motivation
- Most failed LLM products lack robust evaluation systems.
- Success = ability to iterate quickly: requires evaluation, debugging, and system change (prompting, fine-tuning, code).
- Evaluation is the flywheel for improvementlike tests in software engineering.


### 2. The Three Levels of Evaluation

#### 2.1 Level 1: Unit Tests
- Assertions (like pytest) for LLM features and scenarios.
- Should be fast, cheap, and run on every code change.
- Use LLMs to help brainstorm assertions and generate synthetic test cases.
- Example: For a real estate assistant, test that queries for listings return the correct number of results.```python
# Example assertion: No UUIDs in output
const noExposedUUID = message => {
  const sanitizedComment = message.comment.replace(/\{\{.*?\}\}/g, '')
  const regexp = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/ig
  const matches = Array.from(sanitizedComment.matchAll(regexp))
  expect(matches.length, 'Exposed UUIDs').to.equal(0, 'Exposed UUIDs found')
}