#!/usr/bin/env python3
import os
import re
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO

# Global set to keep track of visited URLs to avoid cycles
visited = set()

def sanitize_filename(name):
    """
    Sanitize a string to be safe as a folder/file name.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name) or "root"

def download_image(img_url, folder, index):
    """
    Download an image from img_url, save it in folder and create a text file with its metadata.
    """
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}")
        return

    # Determine a file extension based on content type
    content_type = response.headers.get('Content-Type', '')
    if 'png' in content_type:
        ext = 'png'
    elif 'gif' in content_type:
        ext = 'gif'
    elif 'jpeg' in content_type or 'jpg' in content_type:
        ext = 'jpg'
    else:
        ext = 'bin'

    image_filename = os.path.join(folder, f'image_{index}.{ext}')
    with open(image_filename, 'wb') as f:
        f.write(response.content)
    print(f"Saved image: {image_filename}")

    # Extract meta data using Pillow
    meta = {}
    try:
        image = Image.open(BytesIO(response.content))
        meta['format'] = image.format
        meta['size'] = image.size
        meta['mode'] = image.mode
        # Attempt to get EXIF data if available
        exif_data = image._getexif() if hasattr(image, '_getexif') else None
        if exif_data:
            meta['exif'] = exif_data
    except Exception as e:
        meta['error'] = f"Failed to extract metadata: {e}"

    # Write metadata to a text file
    meta_filename = os.path.join(folder, f'image_{index}_metadata.txt')
    try:
        with open(meta_filename, 'w', encoding='utf-8') as f:
            for key, value in meta.items():
                f.write(f"{key}: {value}\n")
        print(f"Saved metadata: {meta_filename}")
    except Exception as e:
        print(f"Failed to write metadata for image {img_url}: {e}")

def process_url(url, parent_folder, depth, max_depth):
    """
    Process a URL: create a folder for it, download any images,
    and recursively follow links (up to max_depth).
    """
    if depth > max_depth:
        return
    if url in visited:
        return
    visited.add(url)

    # Create a folder for the current URL using a sanitized version of its netloc and path
    parsed = urlparse(url)
    folder_name = sanitize_filename(parsed.netloc + parsed.path)
    current_folder = os.path.join(parent_folder, folder_name)
    os.makedirs(current_folder, exist_ok=True)
    print(f"{'  ' * (depth-1)}Processing ({depth}): {url}")

    # Try to get the content of the URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"{'  ' * (depth-1)}Failed to retrieve {url}: {e}")
        return

    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Download images found on this page
        images = soup.find_all('img')
        for idx, img in enumerate(images, start=1):
            img_src = img.get('src')
            if not img_src:
                continue
            # Resolve relative URLs
            img_url = urljoin(url, img_src)
            download_image(img_url, current_folder, idx)
        # Find and follow links
        links = soup.find_all('a')
        for a in links:
            href = a.get('href')
            if not href:
                continue
            next_url = urljoin(url, href)
            if next_url.startswith('http'):
                process_url(next_url, current_folder, depth + 1, max_depth)
    else:
        # If the content is not HTML and seems to be an image, download it directly
        if 'image' in content_type:
            download_image(url, current_folder, 1)

def main():
    parser = argparse.ArgumentParser(
        description="Tracer: A tool to follow links, download images, and save metadata organized as a folder tree."
    )
    parser.add_argument("url", help="The starting URL")
    parser.add_argument("--depth", type=int, default=5, help="Maximum depth to traverse (default: 5)")
    parser.add_argument("--output", default="output", help="Output folder (default: output)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    process_url(args.url, args.output, depth=1, max_depth=args.depth)

if __name__ == "__main__":
    main()
