from google.cloud import vision


def search_image(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.web_detection(image=image)

    web_detection = response.web_detection

    if not web_detection.web_entities:
        raise Exception("No web entities found")

    if not web_detection.pages_with_matching_images:
        raise Exception("No matching pages found")

    if not web_detection.partial_matching_images:
        raise Exception("No candidate images found")

    return {
        "person_detected":
            web_detection.web_entities[0].description,

        "matched_page":
            web_detection.pages_with_matching_images[0].url,

        "candidate_image":
            web_detection.partial_matching_images[0].url
    }


if __name__ == "__main__":
    result = search_image("samples/face.jpg")

    print(result)