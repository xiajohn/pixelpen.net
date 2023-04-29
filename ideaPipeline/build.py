import os
import shutil
import json

def sanitize_folder_name(name):
    return name.replace(':', '').replace(' ', '_')

def copy_files(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    items_to_copy = os.listdir(src_folder)

    for item in items_to_copy:
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            dest_subfolder = os.path.join(dest_folder, item)
            if not os.path.exists(dest_subfolder):
                os.makedirs(dest_subfolder)
            copy_files(src_path, dest_subfolder)

def main():
    # Folders
    generated_folder = "generated"
    local_testing_folder = "../frontend/public/local_testing"
    s3_upload_folder = "../content/blog"

    # Copy files to local testing folder
    copy_files(generated_folder, local_testing_folder)

    # Copy files to S3 upload folder
    copy_files(generated_folder, s3_upload_folder)

    # Generate blogs.json and blog_folders.json
    blog_folders = {}
    for folder in os.listdir(generated_folder):
        folder_path = os.path.join(generated_folder, folder)
        if os.path.isdir(folder_path):
            blog_folders[folder] = {
                "title": folder.replace('_', ' '),
                "filename": "blog_post.md",
                "folderName": folder
            }

    with open(os.path.join(local_testing_folder, "blogs.json"), "w") as f:
        json.dump(blog_folders, f, indent=2)

    with open(os.path.join(s3_upload_folder, "blog_folders.json"), "w") as f:
        json.dump(blog_folders, f, indent=2)

if __name__ == "__main__":
    main()
