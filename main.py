import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions import get_file_content, get_files_info, run_python_file, write_file
from functions.call_function import call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

available_functions = [
    get_files_info.schema_get_files_info,
    get_file_content.schema_get_file_content,
    run_python_file.schema_run_python_file,
    write_file.schema_write_file,
]

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
prompt = args.user_prompt
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
]

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,  # pyright: ignore[reportArgumentType]
        tools=available_functions,  # pyright: ignore[reportArgumentType]
    )

    message = response.choices[0].message
    messages.append(message)

    if args.verbose:
        print(f"User prompt: {prompt}")
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
        print(response.choices[0].message.content)

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            # function_args = json.loads(tool_call.function.arguments or "{}") # pyright: ignore[reportAttributeAccessIssue]
            # print(f"Calling function: {tool_call.function.name}({function_args})") # pyright: ignore[reportAttributeAccessIssue]
            result = call_function(tool_call, args.verbose)
            if result["content"] is None:
                raise Exception()

            if args.verbose:
                print(f"-> {result['content']}")

            messages.append(result)
    else:
        break
if not messages[-1].content or "Final message:" not in messages[-1].content:
    exit(1)
