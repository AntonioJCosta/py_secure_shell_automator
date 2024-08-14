import os
import re


def extract_docstrings(content):
    # Extract class docstrings, accounting for optional multiline decorators
    class_pattern = r'(?:@[\w\.]+\s*\(.*?\)\s*)*class (\w+)\(.*?\):\n\s+"""(.*?)"""'
    class_matches = re.findall(class_pattern, content, re.DOTALL)

    # Extract property docstrings
    property_pattern = r'@property\n\s+def\s+([a-zA-Z]\w*)\s*\(.*?\)\s*->\s*.*?:\n\s+"""(.*?)"""'
    property_matches = re.findall(property_pattern, content, re.DOTALL)

    # Extract method docstrings, excluding private methods (those starting with an underscore)
    # and methods that are properties
    property_names = [p[0] for p in property_matches]
    method_pattern = r'def\s+([a-zA-Z]\w*)\s*\(.*?\)\s*->\s*.*?:\n\s+"""(.*?)"""'
    method_matches = [
        match for match in re.findall(method_pattern, content, re.DOTALL)
        if match[0] not in property_names
    ]

    return class_matches, method_matches, property_matches


def format_docstrings(class_matches, method_matches, property_matches):
    formatted = ""
    
    for class_name, class_doc in class_matches:
        formatted += f"### {class_name}\n\n"
        formatted += f"{class_doc.strip()}\n\n"

        # Find properties belonging to this class
        class_properties = [p for p in property_matches if p]
        if class_properties:
            for property_name, property_doc in class_properties:
                # Extract the first line of the docstring as the description
                property_desc = property_doc.strip().split('\n')[0]
                # Remove the first line from the docstring
                cleaned_doc = '\n'.join(property_doc.strip().split('\n')[1:])
                # Remove '>>> ' from examples
                cleaned_doc = cleaned_doc.replace('>>> ', '')
                formatted += f"#### **{property_name}** (Property)\n\n"
                formatted += f"{property_desc.strip()}\n\n"
                formatted += f"```python\n{cleaned_doc}\n```\n\n"

        # Find methods belonging to this class
        class_methods = [m for m in method_matches if m]
        if class_methods:
            for method_name, method_doc in class_methods:
                # Extract the first line of the docstring as the description
                method_desc = method_doc.strip().split('\n')[0]
                # Remove the first line from the docstring
                cleaned_doc = '\n'.join(method_doc.strip().split('\n')[1:])
                # Remove '>>> ' from examples
                cleaned_doc = cleaned_doc.replace('>>> ', '')
                formatted += f"#### **{method_name}** (Method)\n\n"
                formatted += f"{method_desc.strip()}\n\n"
                formatted += f"```python\n{cleaned_doc}\n```\n\n"

    return formatted


def append_to_readme(readme_path, content):
    with open(readme_path, "a") as readme:
        readme.write("\n\n" + content)


def traverse_and_update_readme(root_dir, readme_path):
    for dirpath, _, filenames in os.walk(root_dir):
        # if dirpath in ["py_secure_shell_automator/base_ssh"]:
            print(f"Checking {dirpath}")
            for filename in filenames:
                if filename.endswith(".py") and filename not in [
                    "__init__.py",
                    "exceptions.py",
                ]:
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r") as file:
                        content = file.read()
                    class_matches, method_matches, property_matches = extract_docstrings(content)
                    if class_matches or method_matches or property_matches:
                        formatted_docstrings = format_docstrings(class_matches, method_matches, property_matches)
                        append_to_readme(readme_path, formatted_docstrings)
                        print(f"Docstrings from {file_path} added to {readme_path}")


def main():
    root_dir = "py_secure_shell_automator"
    readme_path = "README.md"

    traverse_and_update_readme(root_dir, readme_path)


if __name__ == "__main__":
    main()