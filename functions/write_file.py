import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a new file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File_path of the file to write to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "content to write to the file.",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs, file_path))
        if os.path.commonpath([working_abs, target_file]) != working_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: recieved error from standard lib: {e}"
