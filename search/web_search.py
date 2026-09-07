import os
import re
import json
import requests
from dotenv import load_dotenv
from google.cloud import vision
from serpapi import GoogleSearch
from .download_image import download_image
from models import FaceCandidate, SearchResult

load_dotenv()

SERPI_API_KEY = os.getenv("SERPAPI_KEY")

class WebSearchService:
    def search_instagram_post(self, person_name: str) -> list:
        search = GoogleSearch({
            "engine": "google",
            "q": f'"{person_name}" site:instagram.com/p/',
            "api_key": SERPI_API_KEY
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

    def extract_instagram_image(self, post_url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            html = requests.get(post_url, headers=headers, timeout=15).text
            match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            if match:
                return match.group(1)
        except Exception as e:
            print(e)
        return None

    def search_image(self, image_path: str, max_results: int = 8) -> SearchResult:
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

        post_urls = self.search_instagram_post(person_name)
        if not post_urls:
            raise Exception(f"No Instagram posts found for {person_name}")
        print(f"\nFound {len(post_urls)} Instagram posts")

        candidates = []
        for post_url in post_urls[:max_results]:
            print(f"\nProcessing post: {post_url}")
            image_url = self.extract_instagram_image(post_url)
            if not image_url:
                continue
            print(f"Image URL: {image_url}")

            candidate_path = download_image(image_url)
            candidates.append(FaceCandidate(
                person_detected=person_name,
                matched_page=post_url,
                candidate_image=image_url,
                candidate_path=candidate_path
            ))
        if not candidates:
            raise Exception("No candidate images downloaded")
        print(f"\nTotal candidates collected: {len(candidates)}")
        return SearchResult(person_detected=person_name, candidates=candidates)