from textnode import *
import os
import shutil
from markdown_blocks import *

def copy_tree(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    source_files = os.listdir(source)
    for obj in source_files:
        if os.path.isfile(f"{source}/{obj}"):
            shutil.copy(f"{source}/{obj}", f"{destination}/{obj}")
        else:
            copy_tree(f"{source}/{obj}", f"{destination}/{obj}")

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise Exception("HTML Error: h1 header not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template_html = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template_html.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    os.makedirs(dest_path, exist_ok=True)
    with open(f"{dest_path}/index.html", 'w') as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    md_files = os.listdir(dir_path_content)
    for obj in md_files:
        obj_path = f"{dir_path_content}/{obj}"
        if os.path.isfile(obj_path):
            generate_page(obj_path, template_path, dest_dir_path)
        else:
            generate_pages_recursive(obj_path, template_path, f"{dest_dir_path}/{obj}")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    source_dir = f"{parent_dir}/static"
    destination_dir = f"{parent_dir}/public"
    content_dir = f"{parent_dir}/content"
    template_file = f"{parent_dir}/template.html"

    print("Copying files to public directory")
    copy_tree(source_dir, destination_dir)

    print("Generating content...")
    generate_pages_recursive(content_dir, template_file, destination_dir)

if __name__ == "__main__":
    main()