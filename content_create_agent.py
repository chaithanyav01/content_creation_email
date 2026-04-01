"""
AI Email + Image Generator Agent
===============================
- Takes TEXT input
- Generates email (LLM)
- Generates image (Stability AI)
- Embeds image in email
- Sends via Gmail SMTP
"""

import os
import smtplib
import requests
from dotenv import load_dotenv
from openai import OpenAI
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Load env
load_dotenv()

# API KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

# Stability endpoint
STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"


class EmailAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    # 🔥 TEXT → EMAIL HTML
    def generate_email_content(self, user_text: str) -> dict:
        prompt = f"""
        Create a visually rich, high-converting restaurant marketing email in HTML.

        INPUT:
        {user_text}

        Design Style:
        - Warm, appetizing, premium food theme
        - Use rich colors (orange, red, brown, gold tones)
        - Soft shadows + rounded corners (modern card UI)
        - Clean, minimal but mouth-watering layout

        Visual Requirements:
        - Hero food image (use {{IMAGE}})
        - Highlight food textures (crispy, juicy, fresh feel)
        - Use section cards with light shadows
        - CTA button should stand out (bold gradient)

        Content Requirements:
        - Catchy subject line (food craving trigger)
        - Headline that creates hunger (e.g. "Craving something delicious?")
        - Emphasize offer clearly (discount, combo, limited deal)
        - Add urgency ("Today only", "Limited time")
        - Friendly, conversational tone

        Structure:
        1. Header (restaurant name/logo style text)
        2. Hero Image ({{IMAGE}})
        3. Bold Headline (craving trigger)
        4. Offer Highlight Box (discount/combo)
        5. Short description (taste-focused)
        6. CTA button (Order Now / Grab Deal)
        7. Footer (minimal)

        Styling:
        - Max width: 600px
        - Inline CSS only
        - Box shadow: 0 4px 15px rgba(0,0,0,0.1)
        - Border radius: 12px+
        - Gradient CTA (orange/red)
        - Generous padding & spacing

        CTA Examples:
        - "Order Now 🍔"
        - "Grab Your Deal 🔥"
        - "Satisfy Your Cravings 😋"

        Return STRICT format:
        SUBJECT: [Your subject]
        ---HTML---
        [Full HTML code]
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content

        parts = content.split("---HTML---")
        subject = parts[0].replace("SUBJECT:", "").strip()
        html = parts[1].strip()

        # Clean up code block formatting if present
        if html.startswith("```html"):
            html = html.replace("```html", "").replace("```", "").strip()
            
        if html.endswith("```"):
            html = html.replace("```", "").strip()

        return {"subject": subject, "html": html}

    # 🎨 IMAGE GENERATION
    def generate_image(self, prompt, filename="generated.jpg"):
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }

        files = {
            "prompt": (None, prompt),
            "negative_prompt": (None, "blurry, low quality"),
            "aspect_ratio": (None, "1:1")
        }

        response = requests.post(STABILITY_URL, headers=headers, files=files)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Image saved: {filename}")
            return filename
        else:
            print("❌ Image error:", response.text)
            return None

    # 📧 SEND EMAIL (WITH EMBEDDED IMAGE)
    def send_email(self, to_email, subject, html_content, image_path=None):
        try:
            msg = MIMEMultipart("related")
            msg["Subject"] = subject
            msg["From"] = SENDER_EMAIL
            msg["To"] = to_email

            # Handle IMAGE placeholder properly
            if image_path:
                # Replace with CID if image exists
                html_content = html_content.replace(
                    "{{IMAGE}}", "cid:generated_image"
                )
            else:
                # Remove image block completely if no image
                html_content = html_content.replace(
                    "{{IMAGE}}", ""
                )

            # Attach HTML
            msg.attach(MIMEText(html_content, "html"))

            # Attach image only if present
            if image_path:
                with open(image_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<generated_image>")
                    msg.attach(img)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
                server.send_message(msg)

            print(f"✅ Sent to {to_email}")
            return True

        except Exception as e:
            print("❌ Email error:", e)
            return False

    # 🚀 FULL PIPELINE
    def run_campaign(self, user_text, recipients):
        print("🤖 Generating email...")
        email_data = self.generate_email_content(user_text)

        print("🎨 Generating image...")
        image_prompt = f"High quality marketing image for: {user_text}"
        image_path = self.generate_image(image_prompt)

        # Ensure HTML has image placeholder
        html = email_data["html"]
        if "{{IMAGE}}" not in html:
            html = html.replace(
                "<body>",
                '<body><div style="text-align:center;"><img src="{{IMAGE}}" width="400"/></div>'
            )

        subject = email_data["subject"]

        for email in recipients:
            self.send_email(email, subject, html, image_path)


# ▶️ MAIN
if __name__ == "__main__":
    agent = EmailAgent()

    user_text = """
    Brand: CARIBOU
    Offer: 20% off on SM ICED AMERICANO
    Audience: coffee lovers
    Tone: exciting
    CTA: Order now
    Website : https://order.cariboucoffee.com/
    """

    recipients = [
        "velpulachaitu987@gmail.com"
    ]

    agent.run_campaign(user_text, recipients)