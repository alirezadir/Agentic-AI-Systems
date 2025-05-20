#
# This is a dummy agent library and a simple serverless API to access our LLM engine.
#
import os
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer

# Set your Hugging Face API token from https://hf.co/settings/tokens
os.getenv("HF_TOKEN") 
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.3-70B-Instruct")
client = InferenceClient("meta-llama/Llama-3.3-70B-Instruct")


# Example of using text_generation()
# This will keep generating until it reaches the max_new_tokens limit or the Eos token.

# output = client.text_generation(
#     "The capital of France is",
#     max_new_tokens=100,
# )

# So we need to use a chat template to get the model to respons based the context.
# appying the chat template to the prompt
prompt="""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
The capital of France is<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

output = client.text_generation(
    prompt,
    max_new_tokens=100,
)

print(output)

# or we can use tokenizer to create the prompt in a chat template.
messages=[
    {"role": "user", "content": "The capital of France is"},
    ]
tokenizer.apply_chat_template(messages, tokenize=False,add_generation_prompt=True)

output = client.text_generation(
    prompt,
    max_new_tokens=100,
)

print(output)


# Example of using chat.completions.create()
output = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "The capital of France is"},
    ],
    stream=False,
    max_tokens=1024,
)
print(output.choices[0].message.content)