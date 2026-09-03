import requests
import os


def download_image(url, output_path):
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"Failed to download image. Status code: {response.status_code}"
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Downloaded: {output_path}")

    return output_path


if __name__ == "__main__":
    url = "https://images.news18.com/ibnlive/uploads/2026/07/Bobby-Deol-Thalapathy-Vijay-Jana-Nayagan-2026-07-e8029ca53ca6b92ed603a9c3ca76322c.jpg"

    download_image(
        url,
        "samples/candidate.jpg"
    )