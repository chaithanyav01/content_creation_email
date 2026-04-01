import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("STABILITY_API_KEY")

# Endpoint (cheaper: core | better: ultra)
URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
# URL = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

def generate_image(prompt, filename="output.jpg"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, prompt),
        "negative_prompt": (None, "blurry, low quality, distorted, bad anatomy"),
        "aspect_ratio": (None, "1:1")
    }

    response = requests.post(URL, headers=headers, files=files)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved: {filename}")
    else:
        print("❌ Error:", response.status_code, response.text)


if __name__ == "__main__":
    prompt = "Employee working under google lamp in google office, 4k"
    generate_image(prompt)