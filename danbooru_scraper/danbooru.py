import os
import json
import httpx
import time
from tqdm.auto import tqdm
from tenacity import retry, stop_after_delay, wait_exponential, retry_if_exception_type

import unibox as ub

logger = ub.UniLogger()

class DanbooruScraper:
    BASE_URL = "https://danbooru.donmai.us/posts/{}.json"

    def __init__(self, root_dir: str, rpm: float = 0.85):
        """
        Initialize the scraper with a root directory and rate limit.
        
        Args:
            root_dir (str): Directory to save metadata files.
            rpm (float): Requests per second (default: 0.85).
        """
        self.root_dir = root_dir
        self.rpm = rpm
        self.request_interval = 1 / self.rpm  # Calculate time interval between requests
        os.makedirs(root_dir, exist_ok=True)

    @retry(
        retry=retry_if_exception_type(httpx.RequestError),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        stop=stop_after_delay(20),
        reraise=True,
    )
    def fetch_post_metadata(self, post_id: str):
        """Fetch post metadata as JSON from Danbooru."""
        url = self.BASE_URL.format(post_id)
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def save_metadata(self, metadata: dict, post_id: str):
        """Save metadata to a JSON file."""
        metadata_path = os.path.join(self.root_dir, f"danbooru_{post_id}.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    def scrape_post(self, post_id: str):
        """Scrape metadata for a single post and save it."""
        try:
            metadata = self.fetch_post_metadata(post_id)
            self.save_metadata(metadata, post_id)
        except Exception as e:
            logger.error(f"Failed to fetch post {post_id}: {e}")

    def scrape_posts(self, post_ids: list[str]):
        """Scrape metadata for multiple posts."""
        pbar = tqdm(post_ids)
        for post_id in pbar:
            pbar.set_description(f"Scraping post ID: {post_id}")
            self.scrape_post(post_id)
            print("Sleeping for", self.request_interval)
            time.sleep(self.request_interval)  # Enforce rate limit


# Example Usage
if __name__ == "__main__":
    scraper = DanbooruScraper(root_dir="danbooru_downloads", rpm=0.85)
    scraper.scrape_posts(["8627389", "8627390", "8627391"])
