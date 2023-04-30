import os
import shutil
import json


def sanitize_folder_name(name):
    return name.replace(':', '').replace(' ', '_')


def generate_sitemap(blog_folders, domain="https://pixelpen.net"):
    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>'''

    url_template = '''  <url>
    <loc>{loc}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>'''

    static_urls = [
        {
            "loc": f"{domain}/",
            "changefreq": "weekly",
            "priority": "1.0"
        },
        {
            "loc": f"{domain}/blog",
            "changefreq": "daily",
            "priority": "0.9"
        },
        {
            "loc": f"{domain}/contact",
            "changefreq": "monthly",
            "priority": "0.8"
        },
        {
            "loc": f"{domain}/about",
            "lastmod": "2022-05-02",
            "changefreq": "monthly",
            "priority": "0.5"
        }
    ]

    blog_urls = [
        {
            "loc": f"{domain}/blog/{sanitize_folder_name(blog_folders[folder]['title'])}",
            "changefreq": "daily",
            "priority": "0.7"
        }
        for folder in blog_folders
    ]

    all_urls = static_urls + blog_urls
    url_entries = [url_template.format(**url) for url in all_urls]
    sitemap_content = sitemap_template.format(urls="\n".join(url_entries))

    return sitemap_content


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


def generate_blogs_json(generated_folder, output_folders, metadata):
    blogs = {}
    for folder in os.listdir(generated_folder):
        folder_path = os.path.join(generated_folder, folder)
        if os.path.isdir(folder_path):
            topic = folder.replace('_', ' ')
            blogs[folder] = {
                "title": metadata[topic]["title"],
                "filename": "blog_post.md",
                "folderName": folder,
                "meta": metadata[topic]
            }

    for output_folder in output_folders:
        with open(os.path.join(output_folder, "blogs.json"), "w") as f:
            json.dump(blogs, f, indent=2)

    return blogs




def save_sitemap_to_folders(sitemap_content, output_folders):
    for output_folder in output_folders:
        with open(os.path.join(output_folder, "sitemap.xml"), "w") as f:
            f.write(sitemap_content)


def build(metadata):
    # Folders
    generated_folder = "generated"
    local_testing_folder = "../frontend/public/local_testing"
    s3_upload_folder = "../content/blog"
    frontend_public_folder = "../frontend/public"

    output_folders = [local_testing_folder, s3_upload_folder]

    # Copy files to local testing folder and S3 upload folder
    for output_folder in output_folders:
        copy_files(generated_folder, output_folder)

    # Generate blogs.json
    blogs = generate_blogs_json(generated_folder, output_folders, metadata)

    # Generate sitemap.xml
    sitemap_content = generate_sitemap(blogs)

    # Save sitemap.xml to output folders
    save_sitemap_to_folders(
        sitemap_content, [generated_folder, frontend_public_folder])


