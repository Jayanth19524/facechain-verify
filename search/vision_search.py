from google.cloud import vision
from serpapi import GoogleSearch
from dotenv import load_dotenv
from .download_image import download_image;

import requests
import os
import re
import json

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_instagram_post(person_name):
    print(f"\nSearching Instagram for: {person_name}")

    search = GoogleSearch({
        "engine": "google",
        "q": f'"{person_name}" site:instagram.com/p/',
        "api_key": SERPAPI_KEY
    })

    results = search.get_dict()

    post_urls = []
    for result in results.get("organic_results", []):
        link = result.get("link")
        if not link:
            continue
        if "instagram.com/p/" in link:
            post_urls.append(link)

    return post_urls if post_urls else None


def extract_instagram_image(post_url):
    print("\nFetching Instagram page...")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        html = requests.get(post_url, headers=headers, timeout=15).text
        match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if match:
            return match.group(1)
    except Exception as e:
        print(e)
    return None


def search_image(image_path, max_results=8):
    for f in os.listdir("samples"):
        if f.startswith("candidate"):
            os.remove(os.path.join("samples", f))

    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.web_detection(image=image)
    web_detection = response.web_detection

    if not web_detection.web_entities:
        raise Exception("No web entities found")

    person_name = web_detection.web_entities[0].description
    print(f"\nDetected person: {person_name}")

    post_urls = search_instagram_post(person_name)
    if not post_urls:
        raise Exception(f"No Instagram posts found for {person_name}")

    print(f"\nFound {len(post_urls)} Instagram posts")

    candidates = []
    for post_url in post_urls[:max_results]:
        print(f"\nProcessing post: {post_url}")
        image_url = extract_instagram_image(post_url)
        if not image_url:
            print(f"  No image found, skipping...")
            continue
        print(f"  Image URL: {image_url}")

        candidate_path = download_image(image_url)
        candidates.append({
            "person_detected": person_name,
            "matched_page": post_url,
            "candidate_image": image_url,
            "candidate_path": candidate_path
        })
        print(f"  Saved to: {candidate_path}")

    if not candidates:
        raise Exception("No candidate images downloaded")

    print(f"\nTotal candidates collected: {len(candidates)}")
    return {
        "person_detected": person_name,
        "candidates": candidates
    }


if __name__ == "__main__":
    result = search_image("samples/face1.jpg")
    print("\nFinal Result:")
    print(json.dumps(result, indent=2))