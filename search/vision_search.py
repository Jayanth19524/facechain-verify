from google.cloud import vision
import os

client = vision.ImageAnnotatorClient()

with open("samples/face.jpg", "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.web_detection(image=image)

web_detection = response.web_detection

print("\n=== WEB ENTITIES ===")
for entity in web_detection.web_entities[:10]:
    print(entity.description, entity.score)

print("\n=== PAGES WITH MATCHING IMAGES ===")
for page in web_detection.pages_with_matching_images[:10]:
    print(page.url)

print("\n=== FULL MATCHING IMAGES ===")
for image in web_detection.full_matching_images[:10]:
    print(image.url)

print("\n=== PARTIAL MATCHING IMAGES ===")
for image in web_detection.partial_matching_images[:10]:
    print(image.url)