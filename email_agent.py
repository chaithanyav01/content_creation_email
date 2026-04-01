"""
Email Marketing Agent
======================
Generates marketing emails with LLM and sends them via Gmail SMTP.

Usage:
    python email_agent.py
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from openai import OpenAI
from dotenv import load_dotenv
import requests
from pathlib import Path
import base64

from streamlit import html

# Load environment variables
load_dotenv()


class EmailAgent:
    """Agent for generating and sending marketing emails."""

    def __init__(self):
        # OpenAI client for content generation
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_APP_PASSWORD")

    def generate_email_content(self, context: dict) -> dict:
        """
        Generate email HTML content using OpenAI.
        
        Args:
            context: Dictionary with brand, offer, audience, image_url keys
        
        Returns:
            Dictionary with 'subject' and 'html' keys
        """
        prompt = f"""
Create a professional marketing email in HTML format.

Brand: {context.get('brand', 'Our Brand')}
Offer: {context.get('offer', 'Special Offer')}
Audience: {context.get('audience', 'Valued Customers')}
Image URL: {context.get('image_url', 'https://via.placeholder.com/600x300')}

Requirements:
1. Create a compelling subject line (return it separately)
2. Design a responsive HTML email with:
   - Professional header with brand name
   - Hero image using the provided URL
   - Engaging body text highlighting the offer
   - Clear CTA (Call-to-Action) button
   - Footer with unsubscribe placeholder
3. Use inline CSS for email compatibility
4. Keep the design clean and mobile-friendly
5. Use appealing colors that match a food/restaurant brand

Return in this exact format:
SUBJECT: [Your subject line here]
---HTML---
[Your HTML code here]
"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content
        
        # Parse subject and HTML
        parts = content.split("---HTML---")
        subject = parts[0].replace("SUBJECT:", "").strip()
        html = parts[1].strip() if len(parts) > 1 else content

        return {"subject": subject, "html": html}

    def create_default_email(self, context: dict) -> dict:
        """
        Create a default template email without LLM.
        Useful when API is unavailable or for testing.
        """
#         brand = context.get('brand', 'Our Brand')
#         offer = context.get('offer', 'Special Offer')
#         audience = context.get('audience', 'Valued Customers')
#         image_url = context.get('image_url', 'https://via.placeholder.com/600x300')
#         cta_link = context.get('cta_link', '#')

#         html = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# </head>
# <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
#     <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
#         <tr>
#             <td align="center" style="padding: 40px 0;">
#                 <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    
#                     <!-- Header -->
#                     <tr>
#                         <td style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); padding: 30px; text-align: center;">
#                             <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">{brand}</h1>
#                         </td>
#                     </tr>
                    
#                     <!-- Hero Image -->
#                     <tr>
#                         <td style="padding: 0;">
#                             <img src="{image_url}" alt="{brand}" width="600" style="width: 100%; height: auto; display: block;">
#                         </td>
#                     </tr>
                    
#                     <!-- Body Content -->
#                     <tr>
#                         <td style="padding: 40px 30px;">
#                             <h2 style="color: #333333; margin: 0 0 20px; font-size: 24px; text-align: center;">
#                                 🎉 Exclusive Offer Just for You!
#                             </h2>
#                             <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px; text-align: center;">
#                                 Hey {audience}! We have something special for you.
#                             </p>
#                             <div style="background-color: #fff8f0; border-left: 4px solid #ff6b35; padding: 20px; margin: 20px 0; border-radius: 4px;">
#                                 <p style="color: #333333; font-size: 20px; font-weight: bold; margin: 0; text-align: center;">
#                                     {offer}
#                                 </p>
#                             </div>
#                             <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px; text-align: center;">
#                                 Don't miss out on this amazing deal! Limited time only.
#                             </p>
                            
#                             <!-- CTA Button -->
#                             <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
#                                 <tr>
#                                     <td align="center">
#                                         <a href="{cta_link}" style="display: inline-block; background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: #ffffff; text-decoration: none; padding: 15px 40px; border-radius: 30px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);">
#                                             Order Now →
#                                         </a>
#                                     </td>
#                                 </tr>
#                             </table>
#                         </td>
#                     </tr>
                    
#                     <!-- Footer -->
#                     <tr>
#                         <td style="background-color: #f8f8f8; padding: 30px; text-align: center; border-top: 1px solid #eeeeee;">
#                             <p style="color: #999999; font-size: 14px; margin: 0 0 10px;">
#                                 © 2024 {brand}. All rights reserved.
#                             </p>
#                             <p style="color: #999999; font-size: 12px; margin: 0;">
#                                 <a href="#" style="color: #999999;">Unsubscribe</a> | 
#                                 <a href="#" style="color: #999999;">View in Browser</a>
#                             </p>
#                         </td>
#                     </tr>
                    
#                 </table>
#             </td>
#         </tr>
#     </table>
# </body>
# </html>
# """
#         subject = f"🔥 {offer} at {brand}!"
        context = {
    "groom_name": "Kolavennu Manikanta Krishna Kumar",   # replace with actual name
    "bride_name": "Shreya Garg",   # replace with actual name
    "date": "25th April 2026",
    "time": "7:00 PM onwards",
    "venue": "The Grand Palace, Bangalore",
    "address": "MG Road, Bangalore",
    "image_url": "https://instasize.com/api/image/2be19417439be57181d023fe5f1bcd32f7b6cb18b07754d4b423f430df66c44f.webp",
    "cta_link": "https://maps.google.com/?q=MG+Road+Bangalore"
}
        html = f"""
<html>
<body style="font-family:Georgia;text-align:center;background:#fff8f0;padding:20px;">

<h1 style="color:#b76e79;">💍 Wedding Invitation 💍</h1>

<h2>{context['groom_name']} ❤️ {context['bride_name']}</h2>

<img src="{context['image_url']}" width="100%" style="max-width:500px;border-radius:12px;" />

<p style="font-size:18px;">
Together with their families,<br>
<b>{context['groom_name']}</b> and <b>{context['bride_name']}</b><br>
request the pleasure of your company<br>
at their wedding celebration.
</p>

<p><b>Date:</b> {context['date']}</p>
<p><b>Time:</b> {context['time']}</p>
<p><b>Venue:</b> {context['venue']}</p>

<a href="{context['cta_link']}" 
style="padding:12px 24px;background:#b76e79;color:white;text-decoration:none;border-radius:6px;">
View Location
</a>

<p style="margin-top:20px;">We look forward to celebrating with you ❤️</p>

</body>
</html>
"""
        subject = f"💍 {context['groom_name']} weds {context['bride_name']}"
        return {"subject": subject, "html": html}

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        embedded_images: list = None
    ) -> bool:
        """
        Send an HTML email via Gmail SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML content of the email
            embedded_images: List of dicts with 'path' and 'cid' for embedded images
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message container
            msg = MIMEMultipart("related")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = to_email

            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Embed images if provided
            if embedded_images:
                for img_info in embedded_images:
                    img_path = img_info.get("path")
                    cid = img_info.get("cid")
                    
                    if img_path and cid:
                        if img_path.startswith("http"):
                            # Download image from URL
                            response = requests.get(img_path)
                            img_data = response.content
                        else:
                            # Read from local file
                            with open(img_path, "rb") as f:
                                img_data = f.read()
                        
                        img = MIMEImage(img_data)
                        img.add_header("Content-ID", f"<{cid}>")
                        img.add_header("Content-Disposition", "inline", filename=cid)
                        msg.attach(img)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False

    def send_campaign(
        self,
        context: dict,
        recipients: list,
        use_llm: bool = True
    ) -> dict:
        """
        Send a marketing campaign to multiple recipients.
        
        Args:
            context: Campaign context (brand, offer, audience, image_url)
            recipients: List of email addresses
            use_llm: Whether to use LLM for content generation
        
        Returns:
            Dictionary with success and failure counts
        """
        # Generate email content
        if use_llm:
            print("🤖 Generating email content with AI...")
            email_data = self.generate_email_content(context)
        else:
            print("📝 Using default template...")
            email_data = self.create_default_email(context)

        subject = email_data["subject"]
        html = email_data["html"]

        print(f"\n📧 Subject: {subject}")
        print(f"📬 Sending to {len(recipients)} recipient(s)...\n")

        results = {"success": 0, "failed": 0, "errors": []}

        for email in recipients:
            if self.send_email(email, subject, html):
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(email)

        print(f"\n📊 Campaign Results:")
        print(f"   ✅ Sent: {results['success']}")
        print(f"   ❌ Failed: {results['failed']}")

        return results


def main():
    """Example usage of the Email Agent."""
    
    # Initialize agent
    agent = EmailAgent()

    # Define campaign context
    context = {
        "brand": "Shawarmer",
        "offer": "20% off on chicken wraps",
        "audience": "Weekend food lovers",
        "image_url": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=600",
        "cta_link": "https://shawarmer.com/order"
    }

    # List of recipients
    recipients = [
        "velpulachaitu987@gmail.com"
        # "saisharathsadu@gmail.com",
        # "kmkkrishnakumar75@gmail.com",
        # "saivenkat0022@gmail.com"    # Replace with actual email
    ]

    # Option 1: Send using LLM-generated content
    # results = agent.send_campaign(context, recipients, use_llm=True)

    # Option 2: Send using default template (no API needed)
    results = agent.send_campaign(context, recipients, use_llm=False)

    # Or send a single email manually
    # email_content = agent.create_default_email(context)
    # agent.send_email("user@example.com", email_content["subject"], email_content["html"])


if __name__ == "__main__":
    main()
