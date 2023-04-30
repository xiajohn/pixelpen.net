import os

class AffiliateLinkInjector:
    def __init__(self, blog_generator, affiliate_links):
        self.blog_generator = blog_generator
        self.blog_folder = blog_generator.blog_folder
        self.affiliate_links = affiliate_links

    def generate_heading(self):
        prompt = f"Generate a heading for the affiliate links section in a blog post about {self.blog_folder}."
        return self.blog_generator.generate_text(prompt).strip()

    def inject_links(self):
        file_path = os.path.join(self.blog_folder, "blog_post.md")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

            # Check if the links already exist in the content
            if all(link['url'] not in content for link in self.affiliate_links):
                # Generate the heading for the affiliate links section
                heading = self.generate_heading()

                # Create the affiliate links markdown text
                links_text = "\n".join([f"[{link['name']}]({link['url']})" for link in self.affiliate_links])

                # Append the heading and links to the end of the blog content
                updated_content = f"{content}\n\n{heading}\n\n{links_text}"

                with open(file_path, "w") as f:
                    f.write(updated_content)
            else:
                print("Affiliate links already exist in the content. Skipping link injection.")
        else:
            print(f"File '{file_path}' does not exist. Skipping link injection.")
