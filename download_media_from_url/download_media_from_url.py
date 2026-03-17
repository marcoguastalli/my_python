import instaloader
import os

# Initialize Instaloader
L = instaloader.Instaloader()

# Function to download media from a given Instagram post URL
def download_media_from_url(url):
    try:
        # Extract the shortcode from the URL
        shortcode = url.rstrip('/').split('/')[-1]
        # Download the post using the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=os.getcwd())
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Main function to read URLs from a file and download media
def main():
    input_file = '~/Downloads/todo_insta_filtered.txt'
    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' not found.")
        return

    with open(input_file, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            download_media_from_url(url)

if __name__ == "__main__":
    main()
