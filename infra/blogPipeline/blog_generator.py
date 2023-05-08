import os
import random
from dotenv import load_dotenv
import base64
from common.content_generator import ContentGenerator

load_dotenv(os.path.join('..', '.env'))


class BlogGenerator(ContentGenerator):
    def __init__(self, topic):
        super().__init__()
        self.topic = topic
        self.blog_folder = self.create_blog_folder(self.topic)

    def sanitize_folder_name(self, name):
        invalid_chars = '\/:*?"<>|'
        sanitized_name = ''.join(
            c if c not in invalid_chars else '_' for c in name)
        return sanitized_name

    def generate_metadata(self, topic):
        title_prompt = f"Write a short, concise, and SEO-friendly title for a blog post about {topic}. Response will be used in HTML for SEO purposes."
        title = self.generate_text(title_prompt).strip()

        description_prompt = f"Generate a concise SEO-friendly summary for a blog post about {topic}. Response will be used in HTML for SEO purposes."
        description = self.generate_text(description_prompt).strip()

        keywords_prompt = f"Generate 3 concise SEO-friendly keywords for a blog post about {topic}. Response will be used in HTML for SEO purposes."
        keywords = self.generate_text(keywords_prompt).strip()
        url = self.sanitize_folder_name(title)

        return {
            "title": title,
            "description": description,
            "keywords": keywords
        }

    def create_blog_folder(self, blog_name):
        sanitized_blog_name = self.sanitize_folder_name(blog_name)
        folder_name = sanitized_blog_name.replace(" ", "-")
        folder_path = os.path.join("generated", folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def insert_image_placeholders(self, content, num_images):
        sections = content.split('\n\n')
        for i in range(1, num_images + 1):
            img_tag = f'ImagePlaceholder{i}'
            random_index = random.randint(0, len(sections) - 1)
            sections.insert(random_index, img_tag)
        return '\n\n'.join(sections)

    def create_blog_prompt(self, topic):
        return f'Generate introduction, main sections, and conclusion for writing a blog post about "{topic}". Write a detailed response discussing {topic}. Include the introduction, title, and conclusion. Use 1700 words. Use markdown. Do not use links. Use a conversational tone. while ensuring it is coherent, avoids lists or options, and engages the reader. Use senteces of varying lengths'

    def create_image_prompt(self, topic):
        return self.generate_text(f"Generate a short prompt for generating an image for \"{topic}\".")

    def create_blog_content(self, topic):
        outline_prompt = self.create_blog_prompt(topic)
        content = self.generate_text(outline_prompt)
        # reviewer = BlogReviewer(content)
        # content = reviewer.review_blog()
        content_with_images = self.insert_image_placeholders(content, 4)

        return content_with_images

    def save_initial_blog(self, content, folder, filename="initialBlog.md"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def save_base64_image(self, base64_image_data, folder, filename="image_data.jpg"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(base64_image_data))

    def generate_and_save_images(self, folder):
        for i in range(1, 5):
            image_prompt = self.create_image_prompt(self.topic)
            base64_image_data = self.generate_image(image_prompt)
            image_filename = f"image_data_{i}.jpg"
            self.save_base64_image(base64_image_data, folder, image_filename)

    def save_blog(self, content, folder, filename="blog_post.md"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def create(self):
        blog_file = os.path.join(self.blog_folder, "blog_post.md")

        # Check if the blog post file already exists
        if os.path.isfile(blog_file):
            print(
                f"Blog post '{blog_file}' already exists. Skipping blog creation.")
            return self.blog_folder

        # Generate and save initial blog content
        print(self.blog_folder)
        blog_content_with_images = self.create_blog_content(self.topic)

        # Remove the unwanted character
        blog_content_with_images = blog_content_with_images.replace('�', '')

        # Generate and save images
        self.generate_and_save_images(self.blog_folder)

        # Save the final blog content with images
        self.save_blog(blog_content_with_images, self.blog_folder)

        return self.blog_folder
