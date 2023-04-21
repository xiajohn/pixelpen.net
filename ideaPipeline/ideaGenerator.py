import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
def save_to_file(file_prefix, blog_post):
    blog_post_filename = f"{file_prefix}_blog_post.txt"
    with open(blog_post_filename, 'w') as post_file:
        post_file.write(blog_post)

def generate_content_ideas(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_blog_post(prompt, max_tokens=4000, temperature=0.5):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature
    )
    return response.choices[0].text.strip()


def get_trending_news(api_key, query=None, category=None, country=None):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "q": query,
        "category": category,
        "country": country
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["articles"]
    else:
        print(f"Error: {response.status_code}")
        return None


trending_news = get_trending_news(news_api_key, query="love", category="entertainment", country="us")
titles = [article["title"] for article in trending_news]
print(titles)
for index, title in enumerate(titles[:4]):
    prompt = f"Generate a content idea based on the news headline: {title}"
    content_idea = generate_content_ideas(prompt)
    print(f"Content idea: {content_idea}\n")
    prompt = f"Write a blog post using the idea {content_idea}. Make it engaging and interesting. Use 4 paragraphs. Make the whole thing 1000 words"
    blog_post = generate_blog_post(prompt)

    file_prefix = f"post_{index+1}"
    save_to_file(file_prefix, blog_post)

    

    

