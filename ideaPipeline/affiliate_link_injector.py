import os

class AffiliateLinkInjector:
    def __init__(self, affiliate_links):
        self.affiliate_links = affiliate_links

    def generate_heading(self):
        return "Recommended Products"

    def inject_links(self, blog_folder):
        file_path = os.path.join(blog_folder, "blog_post.md")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

            # Check if the links already exist in the content
            if all(link['url'] not in content for link in self.affiliate_links):
                # Generate the heading for the affiliate links section
                heading = self.generate_heading()

                # Create the affiliate links markdown text
                links_text = "\n".join([f"- [{link['name']}]({link['url']})" for link in self.affiliate_links])

                # Append the heading and links to the end of the blog content
                updated_content = f"{content}\n\n---\n\n## {heading}\n\nAs a reader of our blog, we want to share some products and services that we think might be helpful to you. We may earn a small commission for any purchases made through the following affiliate links, at no additional cost to you.\n\n{links_text}\n\nThank you for your support and happy shopping!"

                with open(file_path, "w") as f:
                    f.write(updated_content)
            else:
                print("Affiliate links already exist in the content. Skipping link injection.")
        else:
            print(f"File '{file_path}' does not exist. Skipping link injection.")
