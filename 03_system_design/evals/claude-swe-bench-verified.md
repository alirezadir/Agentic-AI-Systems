# Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

Published Jan 06, 2025

[SWE-bench](https://www.swebench.com/) is an AI evaluation benchmark that assesses a model's ability to complete real-world software engineering tasks. It tests how an AI model can resolve GitHub issues from open-source Python repositories, requiring the model to understand, modify, and test code before submitting a solution. Each solution is graded against the real unit tests from the original pull request.

## What is SWE-bench Verified?
- A 500-problem subset of SWE-bench, reviewed by humans to ensure solvability.
- Evaluates the entire "agent" system (model + scaffolding), not just the model.
- Measures the ability to complete real engineering tasks, not just interview-style questions.

## Claude 3.5 Sonnet Results
- Achieved **49%** on SWE-bench Verified, surpassing the previous SOTA (45%).
- Uses a minimal agent scaffold: a prompt, a Bash Tool, and an Edit Tool.
- The agent loop continues until the model decides it is finished or exceeds the context limit (200k tokens).

| Model                      | Claude 3.5 Sonnet (new) | Previous SOTA | Claude 3.5 Sonnet (old) | Claude 3 Opus |
|----------------------------|-------------------------|---------------|-------------------------|---------------|
| SWE-bench Verified score   | 49%                     | 45%           | 33%                     | 22%           |

## Agent Design Philosophy
- Give as much control as possible to the language model.
- Keep scaffolding minimal; let the model decide the workflow.
- Use detailed tool descriptions to guide the model.

### Agent Prompt Example
```plaintext
<uploaded_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.
```

## Tool Specs

### Bash Tool
```json
{
   "name": "bash",
   "description": "Run commands in a bash shell\n* When invoking this tool, the contents of the 'command' parameter does NOT need to be XML-escaped.\n* You don't have access to the internet via this tool.\n* You do have access to a mirror of common linux and python packages via apt and pip.\n* State is persistent across command calls and discussions with the user.\n* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n* Please avoid commands that may produce a very large amount of output.\n* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "The bash command to run."
           }
       },
       "required": ["command"]
   }
}
```

### Edit Tool
```json
{
   "name": "str_replace_editor",
   "description": "Custom editing tool for viewing, creating and editing files\n* State is persistent across command calls and discussions with the user\n* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n* The `create` command cannot be used if the specified `path` already exists as a file\n* If a `command` generates a long output, it will be truncated and marked with <response clipped>\n* The `undo_edit` command will revert the last edit made to the file at `path`\nNotes for using the `str_replace` command:\n* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
               "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
           },
           "file_text": {
               "description": "Required parameter of `create` command, with the content of the file to be created.",
               "type": "string"
           },
           "insert_line": {
               "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
               "type": "integer"
           },
           "new_str": {
               "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
               "type": "string"
           },
           "old_str": {
               "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
               "type": "string"
           },
           "path": {
               "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
               "type": "string"
           },
           "view_range": {
               "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
               "items": {
                   "type": "integer"
               },
               "type": "array"
           }
       },
       "required": ["command", "path"]
   }
}
```

## Example Agent Workflow

1. **Explore repo structure** using the Edit Tool.
2. **Create a script** to reproduce the error.
3. **Run the script** with the Bash Tool to confirm the error.
4. **Edit source code** to fix the issue.
5. **Rerun the script** to verify the fix.
6. **Repeat** as needed, considering edge cases, until the model decides it's done.

### Example (abbreviated):
- **THOUGHT:** Explore repo structure
- **ACTION:** Edit Tool (view /repo)
- **OBSERVATION:** List of files and directories
- **THOUGHT:** Create script to reproduce error
- **ACTION:** Edit Tool (create /repo/reproduce_error.py)
- **OBSERVATION:** File created
- **THOUGHT:** Run script
- **ACTION:** Bash Tool (python3 /repo/reproduce_error.py)
- **OBSERVATION:** Error reproduced
- **THOUGHT:** Edit source code to fix
- **ACTION:** Edit Tool (str_replace in /repo/sklearn/linear_model/ridge.py)
- **OBSERVATION:** Edit made
- **THOUGHT:** Rerun script to verify fix
- **ACTION:** Bash Tool (python3 /repo/reproduce_error.py)
- **OBSERVATION:** Error fixed

## Challenges
1. **Duration and token costs:** Some runs take hundreds of steps and >100k tokens.
2. **Grading:** Environment setup issues can affect grading accuracy.
3. **Hidden tests:** The model can't see the tests, so it may think it succeeded when it hasn't.
4. **Multimodal:** No implementation for viewing files or URLs, making some debugging harder.

## Conclusion
Claude 3.5 Sonnet, with a simple prompt and two general-purpose tools, achieved state-of-the-art results on SWE-bench Verified. The agent's minimal scaffolding and robust tool design allow the model to self-direct and solve complex real-world coding tasks.


*For more details, see the original post: [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet)* 