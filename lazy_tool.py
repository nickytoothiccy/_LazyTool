import os
import sys
import argparse
from pathlib import Path

# Possible usages:
# python lazy_tool.py device.lst  .\templates_MM\P_07401.xml --target_folder ..\mimic\
# python lazy_tool_2.py XL_07482 DO_IO.txt --output_file IO_074_3.txt
# python lazy_tool.py device.lst  .\templates_MM\PIT_07401.xml --target_folder ..\mimic\


def generate_files(names, template_file, target_folder, output_file):
    # Check if names is a list or a single name
    if isinstance(names, str):
        names = [names]

    # Open the template file
    with open(template_file, 'r') as template_file_obj:
        template_content = template_file_obj.read()

    # Get the extension of the template file
    template_extension = Path(template_file).suffix

    if target_folder:
        # Create the target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

    # Generate new files or append to the output file for each name
    for name in names:
        # Replace placeholder with the name in the template content
        new_content = template_content.replace('<NAME>', name)

        # Replace any occurrence of the template file name with the new name
        new_content = new_content.replace(Path(template_file).stem, name)

        if target_folder:
            # Create a new file with the name as the filename in the target folder
            new_filename = os.path.join(target_folder, f"{name}{template_extension}")
            with open(new_filename, 'w') as new_file:
                new_file.write(new_content)
            print(f"Generated file: {new_filename}")

        if output_file:
            # Append the output to the file if it already exists
            if os.path.isfile(output_file):
                with open(output_file, 'a') as existing_file:
                    existing_file.write(new_content + '\n\n')
            else:
                with open(output_file, 'w') as new_file:
                    new_file.write(new_content + '\n\n')
            print(f"Appended output to file: {output_file}")

def is_comma_divided(input_string):
    # Split the input string by comma
    parts = input_string.split(',')

    # Check if the string has two parts and they are not empty
    if len(parts) == 2 and parts[0] != '' and parts[1] != '':
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate files using a template.')
    parser.add_argument('names_file_or_name', help='names file or a single name')
    parser.add_argument('template_file', help='template file (path)')
    parser.add_argument('--target_folder', help='target folder to save the generated files')
    parser.add_argument('--output_file', help='output file to append the content')

    args = parser.parse_args()

    names_or_file = args.names_file_or_name
    template_file = args.template_file
    target_folder = args.target_folder
    output_file = args.output_file

    if os.path.isfile(names_or_file):
        # If names_or_file is a file, read names from the file
        with open(names_or_file, 'r') as names_file:
            names = names_file.read().splitlines()
    else:
        # If names_or_file is a name, use it directly
        names = names_or_file

    generate_files(names, template_file, target_folder, output_file)