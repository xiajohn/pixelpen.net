import openai
import os
from dotenv import load_dotenv
import base64
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
class BlogGenerator:
    def __init__(self, topic ):
        self.topic = topic
        self.blog_folder = self.create_blog_folder(self.topic)
        
        
    def generate_text(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=2500,
            messages=[
                {"role": "system", "content": "You are a blog writer."},
                {"role": "user", "content": f"{prompt}. Pick the first option."}
            ]
        )
        return response.choices[0].message.content

    def generate_image(self, prompt):
        max_attempts = 2  # total attempts: initial attempt + 1 retry
        attempt = 0
        base64_image_data_list = []

        while attempt < max_attempts:
            response = openai.Image.create(prompt=prompt, n=1, size="256x256", response_format="b64_json")
            
            for data_object in response['data']:
                base64_image_data = data_object['b64_json']
                base64_image_data_list.append(base64_image_data)

            if base64_image_data_list:
                # If the list is not empty, the image was generated successfully
                break
            else:
                attempt += 1

        # If you only need the first image data, you can return the first item in the list
        return base64_image_data_list[0]
    
    def sanitize_folder_name(self,name):
        invalid_chars = '\/:*?"<>|'
        sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in name)
        return sanitized_name
    
    def generate_metadata(self, topic):
            title_prompt = f"Generate a catchy SEO-friendly title for a blog post about {topic}."
            title = self.generate_text(title_prompt).strip()

            description_prompt = f"Generate a concise and descriptive SEO-friendly summary for a blog post about {topic}."
            description = self.generate_text(description_prompt).strip()

            keywords_prompt = f"Generate 3 relevant SEO-friendly keywords for a blog post about {topic}."
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
        return f'Generate introduction, main sections, and conclusion for writing a blog post about "{topic}". Include the introduction, title, and conclusion. Use 1700 words. Use markdown. Add {num_images} image placeholders in the format "{image_placeholders}".'


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

