import os
import sys

def copy_to_dirs(directory):
    # Get the list of all files in the provided directory
    all_files = os.listdir(directory)

    # Filter only .py files
    py_files = [file for file in all_files if file.endswith(".py")]

    # Move the files dynamically into the created directories
    for py_file in py_files:
        directory_name = py_file.replace(".py", "")
        new_directory_path = os.path.join(directory, directory_name)

        # Check if the directory exists, if not create it
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)

        # Move the file into the created directory
        file_path = os.path.join(directory, py_file)
        if os.path.exists(file_path):
            os.rename(file_path, os.path.join(new_directory_path, py_file))

def rename_py_files_to_app(directory):
    # Get the list of all directories in the provided directory
    all_items = os.listdir(directory)

    # Filter only directories
    directories = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]

    for dir_name in directories:
        dir_path = os.path.join(directory, dir_name)
        py_file = os.path.join(dir_path, f"{dir_name}.py")
        new_file_name = os.path.join(dir_path, "app.py")

        # Rename the file to app.py if it exists and app.py doesn't already exist
        if os.path.exists(py_file) and not os.path.exists(new_file_name):
            os.rename(py_file, new_file_name)

if __name__ == "__main__":
    # Check if the directory is provided as a command-line argument
    if len(sys.argv) > 1:
        input_directory = sys.argv[1]
        copy_to_dirs(input_directory)
        rename_py_files_to_app(input_directory)
    else:
        print("Please provide a directory path as an argument.")

