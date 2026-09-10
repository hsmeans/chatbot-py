import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
  try:
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_abs, file_path))
    if os.path.commonpath([working_abs, target_file]) != working_abs:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if os.path.splitext(target_file)[1] != ".py":
      return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args is not None:
      command.extend(args)

    result = subprocess.run(command, cwd=working_abs, capture_output=True, text=True, timeout=30)

    output = ""
    if result.returncode != 0:
      output += "Process exited with code X"
    if not result.stdout and not result.stderr:
      output += "\nNo output produced"
    else:
      output += f"\nSTDOUT: {result.stdout}" if result.stdout else ""
      output += f"\nSTDERR: {result.stderr}" if result.stderr else ""
    return output

  except Exception as e:
    return f"Error: executing Python file: {e}"