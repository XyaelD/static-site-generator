import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No title in the markdown! At least one h1 element is required!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = None
    template_file = None
    with open(from_path, "r") as f:
        markdown_file = f.read()
    
    with open(template_path, "r") as f:
        template_file = f.read()
    
    content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", content)
    
    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)
    with open(f"{dest_path}".replace(".md", ".html"), "a") as f:
        f.write(template_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(dir_path_content):
        files_and_directories = os.listdir(dir_path_content)
        for f_d in files_and_directories:
            current_path = os.path.join(dir_path_content, f_d)
            if os.path.isfile(current_path):
                _, file_extension = os.path.splitext(current_path)
                if file_extension == '.md':
                    print(f"Creating html file from {current_path} to {current_path.replace(dir_path_content, dest_dir_path)}")
                    generate_page(current_path, template_path, current_path.replace(dir_path_content, dest_dir_path))    
            else:
                new_directory = current_path.replace(dir_path_content, dest_dir_path)
                if not os.path.exists(new_directory):
                    print(f"Creating new directory: {new_directory}")
                    os.mkdir(new_directory)
                generate_pages_recursive(current_path, template_path, current_path.replace(dir_path_content, dest_dir_path))
        
    