# danbooru-scraper

yet another danbooru scraper, this time distributed for sagemaker use

## Installation:

```bash
pip install danbooru-scraper
```

## Usage

### cli:

```bash
# danbooru-scraper --help
usage: danbooru-scraper [-h] --from-id FROM_ID --to-id TO_ID
                        --local-dir LOCAL_DIR --upload-dir UPLOAD_DIR
```

example inputs:
```bash
danbooru-scraper --from-id 8627380 --to-id 8627391 --local-dir danbooru_downloads --upload-dir s3://dataset-ingested/danbooru --request-interval 0.85
```

### python:

```python
from danbooru_scraper import DanbooruScraper

scraper = DanbooruScraper(root_dir='../data/')
post_ids = [i for i in range(1000, 10000)]
scraper.scrape_posts(post_ids)
```

### SageMaker:

(Check notebooks/laucch_sagemaker.ipynb for a complete example of distributed scraping on sagemaker.)

## Build:

```bash
python -m pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```