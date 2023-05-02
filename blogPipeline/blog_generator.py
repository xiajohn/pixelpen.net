
import os
from dotenv import load_dotenv
import base64
from content_generator import ContentGenerator
load_dotenv()

class BlogGenerator(ContentGenerator):
    def __init__(self, topic ):
        self.topic = topic
        self.blog_folder = self.create_blog_folder(self.topic)
    
    def sanitize_folder_name(self,name):
        invalid_chars = '\/:*?"<>|'
        sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in name)
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

    def create_blog_folder(self,blog_name):
        sanitized_blog_name = self.sanitize_folder_name(blog_name)
        folder_name = sanitized_blog_name.replace(" ", "-")
        folder_path = os.path.join("generated", folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path


    def replace_image_placeholders(self,content, replacements):
        for placeholder, image_filename in replacements.items():
            img_tag = f'![Description](/{image_filename})'
            content = content.replace(placeholder, img_tag)
        return content

    def create_blog_prompt(self,topic, num_images):
        image_placeholders = ", ".join([f"{{ImagePlaceholder{i}}}" for i in range(1, num_images+1)])
        return f'Generate introduction, main sections, and conclusion for writing a blog post about "{topic}". Include the introduction, title, and conclusion. Use 1700 words. Use markdown. Add {num_images} image placeholders randomly in the article in the format "{image_placeholders}". Do not use links.'


    def create_image_prompt(self,text):
        return self.generate_text(f"Generate short prompt for generating an image for \"{text}\".")

    def create_blog_content(self,topic):
        outline_prompt = self.create_blog_prompt(topic, 4)
        return self.generate_text(outline_prompt)

    def save_initial_blog(self,content, folder, filename="initialBlog.md"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def save_base64_image(self,base64_image_data, folder, filename="image_data.jpg"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(base64_image_data))

    def generate_and_save_images(self,content, folder):
        for i in range(1, 5):
            image_prompt = self.create_image_prompt(content)
            base64_image_data = self.generate_image(image_prompt)
            image_filename = f"image_data_{i}.jpg"
            self.save_base64_image(base64_image_data, folder, image_filename)

    def save_blog(self,content, folder, filename="blog_post.md"):
        file_path = os.path.join(folder, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def create(self):
        blog_file = os.path.join(self.blog_folder, "blog_post.md")

        # Check if the blog post file already exists
        if os.path.isfile(blog_file):
            print(f"Blog post '{blog_file}' already exists. Skipping blog creation.")
            return self.blog_folder

        # Generate and save initial blog content
        print(self.blog_folder)
        blog_content_with_placeholders = self.create_blog_content(self.topic)

        # Remove the unwanted character
        blog_content_with_placeholders = blog_content_with_placeholders.replace('�', '')

        # Generate and save images
        self.generate_and_save_images(blog_content_with_placeholders, self.blog_folder)

        # Save the final blog content with images
        self.save_blog(blog_content_with_placeholders, self.blog_folder)

        return self.blog_folder

