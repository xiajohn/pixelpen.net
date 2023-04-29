import openai
import os
from dotenv import load_dotenv
import base64
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2500,
        messages=[
            {"role": "system", "content": "You are a blog writer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="256x256", response_format="b64_json")
    base64_image_data_list = []
    for data_object in response['data']:
        base64_image_data = data_object['b64_json']
        base64_image_data_list.append(base64_image_data)

    # If you only need the first image data, you can return the first item in the list
    return base64_image_data_list[0]

def sanitize_folder_name(name):
    invalid_chars = '\/:*?"<>|'
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in name)
    return sanitized_name

def create_blog_folder(blog_name):
    sanitized_blog_name = sanitize_folder_name(blog_name)
    folder_name = sanitized_blog_name.replace(" ", "_")
    folder_path = os.path.join("generated", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def replace_image_placeholders(content, replacements):
    for placeholder, image_filename in replacements.items():
        img_tag = f'![Description](/{image_filename})'
        content = content.replace(placeholder, img_tag)
    return content

def create_blog_prompt(topic, num_images):
    image_placeholders = ", ".join([f"{{ImagePlaceholder{i}}}" for i in range(1, num_images+1)])
    return f'Generate introduction, main sections, and conclusion for writing a blog post about "{topic}". Include the introduction, title, and conclusion. Use 1700 words. Use markdown. Add {num_images} image placeholders in the format "{image_placeholders}".'


def create_image_prompt(text):
    return generate_text(f"Generate short prompt for generating an image for \"{text}\".")

def create_blog_content(topic):
    outline_prompt = create_blog_prompt(topic, 4)
    return generate_text(outline_prompt)

def save_initial_blog(content, folder, filename="initialBlog.md"):
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as f:
        f.write(content)

def save_base64_image(base64_image_data, folder, filename="image_data.jpg"):
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64_image_data))

def generate_and_save_images(content, folder):
    image_data = {}
    for i in range(1, 5):
        image_prompt = create_image_prompt(content)
        base64_image_data = generate_image(image_prompt)
        image_filename = f"image_data_{i}.jpg"
        save_base64_image(base64_image_data, folder, image_filename)
        image_data[f"{{ImagePlaceholder{i}}}"] = image_filename
    return image_data


def save_blog_with_images(content, folder, image_replacements, filename="blog_post.md"):
    blog_content_with_images = replace_image_placeholders(content, image_replacements)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as f:
        f.write(blog_content_with_images)

topic = "Top 5 places to visit in Cancun"

# Create a folder for the blog post
blog_folder = create_blog_folder(topic)

# Generate and save initial blog content
blog_content_with_placeholders = create_blog_content(topic)

# Generate and save images
image_replacements = generate_and_save_images(blog_content_with_placeholders, blog_folder)

# Save the final blog content with images
save_blog_with_images(blog_content_with_placeholders, blog_folder, image_replacements)
