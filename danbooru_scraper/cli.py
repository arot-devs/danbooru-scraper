import argparse
import s5cmdpy

from danbooru_scraper.danbooru import DanbooruScraper

import unibox as ub
logger = ub.UniLogger()

def scrape_and_process_posts(from_id:int, to_id:int, local_dir:str, upload_dir:str):
    """Scrape metadata for posts and process them."""
    scraper = DanbooruScraper(root_dir=local_dir)
    post_ids = [str(post_id) for post_id in range(from_id, to_id + 1)]
    scraper.scrape_posts(post_ids)

    local_files = ub.ls(local_dir)
    logger.info(f"Scraping complete | total files: {len(local_files)}")

    logger.info("Uploading files to S3...")
    s5cmdpy.sync(local_dir, upload_dir)
    logger.info(f"id: {from_id} - {to_id} uploading complete, exiting")


def main():

    # danbooru_scraper/cli.py --from-id 8627380 --to-id 8627391 --local-dir danbooru_downloads --upload-dir s3://dataset-ingested/danbooru
    parser = argparse.ArgumentParser(description="Scrape and upload Danbooru metadata to S3")
    parser.add_argument("--from-id", type=int, help="Starting post ID", required=True)
    parser.add_argument("--to-id", type=int, help="Ending post ID", required=True)
    parser.add_argument("--local-dir", type=str, help="Local directory to store metadata", required=True)
    parser.add_argument("--upload-dir", type=str, help="S3 directory to upload metadata", required=True)
    parser.add_argument("--request-interval", type=float, help="Time interval between requests", default=0.85)
    args = parser.parse_args()

    scrape_and_process_posts(args.from_id, args.to_id, args.local_dir, args.upload_dir)

if __name__ == "__main__":
    main()
    
