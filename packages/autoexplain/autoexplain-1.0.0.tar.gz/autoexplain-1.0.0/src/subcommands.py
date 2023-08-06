# This file contains the functions that are called when the user runs the 'adoc file' command.
# The 'adoc file' command is used to add documentation to a file, or to set the openai key.
# The 'adoc file' command has two subcommands: 'add' and 'set-key'.
# The 'add' subcommand is used to add documentation to a file.
# The 'set-key' subcommand is used to set the openai key.
# The 'add' subcommand takes a list of files as an argument.
# The 'set-key' subcommand takes a key as an argument.
# The 'add' subcommand calls the 'edit' function from the 'openai_functions' file.
# The 'set-key' subcommand stores the key in the '.adoconfig' file.

from src.openai_functions import edit, complete
import subprocess
import configparser
import os

# This function is called when the user runs the 'adoc file add' command.
# This function takes a list of files as an argument.
# This function iterates over the list of files and passes each file to the 'edit' function.
# This function then adds the files to the git repository.
def add(args):
    # Iterate over the list of modified files and pass each file to the add_docs function
    files = args.files
    max = len(files)
    pointer = 0
    while pointer < max:
        if os.path.isdir(files[pointer]):
            files = files + [files[pointer]+file for file in os.listdir(files[pointer])]
            max+=len(os.listdir(files[pointer]))
        else:
            with open(files[pointer], 'r') as f:
                content = f.read()
            edit(content, output_path=files[pointer])
        pointer+=1
    subprocess.run(["git", "add"]+files)

def generate_readme():
    FILES_NOT_TO_INCLUDE = ['LICENSE', 'README.md']
    if os.path.exists('.aexignore'):
        with open('.aexignore', 'r') as f:
            contents = f.read()
        FILES_NOT_TO_INCLUDE = contents.split('\\n')
    cur_dir_not_full_path = os.getcwd().split('/')[-1]
    README_START =  f'# {cur_dir_not_full_path}\n## What is it?\n'

    def generate_prompt(length=3000):
        #This function has been borrowed from tom-doerr (https://github.com/tom-doerr/codex-readme)
        input_prompt = ''
        files_sorted_by_mod_date = sorted(os.listdir('.'), key=os.path.getmtime)
        # Reverse sorted files.
        files_sorted_by_mod_date = files_sorted_by_mod_date[::-1]
        for filename in files_sorted_by_mod_date:
            # Check if file is a image file.
            is_image_file = False
            for extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']:
                if filename.endswith(extension):
                    is_image_file = True
                    break
            if filename not in FILES_NOT_TO_INCLUDE and not filename.startswith('.') \
                    and not os.path.isdir(filename) and not is_image_file:
                with open(filename) as f:
                    input_prompt += '\n===================\n# ' + filename + ':\n'
                    input_prompt += f.read() + '\n'

        input_prompt = input_prompt[:length]
        input_prompt += '\n\n===================\n# ' + 'README.md:' + '\n'
        input_prompt += README_START
        return input_prompt

    prompt = generate_prompt()
    complete(prompt, output_path="README.md")
    

def set_key(args):
    config = configparser.ConfigParser()
    config.read('.aexconfig')
    if not config.has_section('openai'):
        config.add_section('openai')
        with open('.gitignore', 'a') as gitignorefile:
            gitignorefile.write('.adoconfig')
    config.set('openai', 'openai_key', args.key[0])
    with open('.aexconfig', 'w') as configfile:
        config.write(configfile)
