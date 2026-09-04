import os
import subprocess
from html import unescape

CANDIDATE_IMAGE = "samples/candidate.jpg"


def download_image(url, output_path=None):
    os.makedirs("samples", exist_ok=True)

    if output_path is None:
        output_path = CANDIDATE_IMAGE

    url = unescape(url)

    if os.path.exists(output_path):
        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base}_{counter}{ext}"
            counter += 1

    cmd = [
        "curl",
        "-L",
        "-A",
        "Mozilla/5.0",
        url,
        "-o",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(result.stderr)

    if not os.path.isfile(output_path):
        raise Exception("candidate.jpg was not created")

    if os.path.getsize(output_path) == 0:
        raise Exception("candidate.jpg is empty")

    return output_path


if __name__ == "__main__":
    url = input("Paste URL: ").strip()

    try:
        download_image(url)
    except Exception as e:
        print("\nERROR:")
        print(e)