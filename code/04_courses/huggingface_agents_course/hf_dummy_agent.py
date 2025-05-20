#
# This is a dummy agent library and a simple serverless API to access our LLM engine.
#

import os
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer

# Set your Hugging Face API token from https://hf.co/settings/tokens
os.getenv("HF_TOKEN")

# client = InferenceClient("meta-llama/Llama-3.3-70B-Instruct")
client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.3-70B-Instruct")

# This system prompt is a bit more complex and actually contains the function description already appended.
# Here we suppose that the textual description of the tools has already been appended.

SYSTEM_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

get_weather: Get the current weather in a given location

The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and an `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are:
get_weather: Get the current weather in a given location, args: {"location": {"type": "string"}}
example use :

{{
  "action": "get_weather",
  "action_input": {"location": "New York"}
}}


ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:

$JSON_BLOB (inside markdown cell)

Observation: the result of the action. This Observation is unique, complete, and the source of truth.
... (this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer. """


# appying the chat template to the prompt
prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{SYSTEM_PROMPT}
<|eot_id|><|start_header_id|>user<|end_header_id|>
What's the weather in London ?
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

# or we can use tokenizer to create the prompt in a chat template.
# messages=[
#     {"role": "system", "content": SYSTEM_PROMPT},
#     {"role": "user", "content": "What's the weather in London ?"},
#     ]
#
# tokenizer.apply_chat_template(messages, tokenize=False,add_generation_prompt=True)

# This answer will be hallucinated by the model
output = client.text_generation(
    prompt,
    max_new_tokens=200,
)
print(output)

# stop before observation to actually execute the function!
output = client.text_generation(
    prompt,
    max_new_tokens=200,
    stop=["Observation:"] # Let's stop before any actual function is called
)

print(output)


# Dummy function
def get_weather(location):
    return f"the weather in {location} is sunny with low temperatures. \n"

new_prompt = prompt + output + get_weather('London')
final_output = client.text_generation(
    new_prompt,
    max_new_tokens=200,
)

print(final_output)