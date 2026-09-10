import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
prompt = args.user_prompt
messages = [
    {"role": "user", "content": prompt},
]

response = client.chat.completions.create(
  model="openrouter/free",
  messages=messages # pyright: ignore[reportArgumentType]
)

if args.verbose:
    print(f"User prompt: {prompt}")
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
print("Response:")
print(response.choices[0].message.content)