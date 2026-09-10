import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
  res = f"Results for {"current directory" if "." else directory}"
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
      res += f'\n\tError: Cannot list "{directory}" as it is outside the permitted working directory'
      return res
    if not os.path.isdir(target_dir):
      res += f'\n\tError: "{directory}" is not a directory'
      return res

    for f in os.listdir(target_dir):
      full_path = os.path.join(target_dir, f)
      res += f"\n\t- {f}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
    # res += f'\n\tSuccess: "{directory}" is within the working directory'
  except Exception as e:
    res += f"\n\tError: recieved error from standard lib: {e}"
  return res