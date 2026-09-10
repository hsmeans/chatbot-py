import os

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
  f = None
  try:
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_abs, file_path))
    if os.path.commonpath([working_abs, target_file]) != working_abs:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
      return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file) as f:
      content = f.read(MAX_CHARS)

      # After reading the first MAX_CHARS...
      if f.read(1):
          content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

      return content
  except Exception as e:
    return f"Error: recieved error from standard lib: {e}"