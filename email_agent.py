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
                CTA Link: {context.get('cta_link', '#')}

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
            model="gpt-4o-mini",
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
        Styled similar to Swiggy/Zomato food delivery apps.
        """
        brand = context.get('brand', 'Our Brand')
        offer = context.get('offer', 'Special Offer')
        audience = context.get('audience', 'Valued Customers')
        image_url = context.get('image_url', 'https://via.placeholder.com/600x300')
        cta_link = context.get('cta_link', '#')

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand} - Order Now</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; background-color: #f8f8f8;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f8f8f8;">
        <tr>
            <td align="center" style="padding: 20px 15px;">
                
                <!-- Preheader -->
                <div style="display: none; max-height: 0; overflow: hidden;">
                    {offer} - Order now and save big! 🍔
                </div>
                
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    
                    <!-- Header Bar - Swiggy Orange Style -->
                    <tr>
                        <td style="background-color: #FC8019; padding: 16px 24px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td>
                                        <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700;">{brand}</h1>
                                    </td>
                                    <td align="right">
                                        <span style="color: #ffffff; font-size: 13px; opacity: 0.9;">🕐 30 min delivery</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Hero Image -->
                    <tr>
                        <td style="padding: 0;">
                            <img src="{image_url}" alt="Delicious Food" width="600" style="width: 100%; height: 220px; object-fit: cover; display: block;">
                        </td>
                    </tr>
                    
                    <!-- Offer Banner - Zomato Red Style -->
                    <tr>
                        <td style="padding: 0 20px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top: -30px; position: relative;">
                                <tr>
                                    <td style="background: linear-gradient(135deg, #E23744 0%, #cb202d 100%); border-radius: 12px; padding: 20px 24px; box-shadow: 0 4px 15px rgba(226, 55, 68, 0.3);">
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td>
                                                    <p style="color: rgba(255,255,255,0.85); font-size: 12px; margin: 0 0 4px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">TODAY'S DEAL</p>
                                                    <p style="color: #ffffff; font-size: 22px; margin: 0; font-weight: 700;">{offer}</p>
                                                </td>
                                                <td align="right" style="vertical-align: middle;">
                                                    <div style="background: #ffffff; color: #E23744; padding: 8px 16px; border-radius: 6px; font-weight: 700; font-size: 14px;">
                                                        FLAT OFF
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Greeting -->
                    <tr>
                        <td style="padding: 28px 24px 0;">
                            <h2 style="color: #1C1C1C; margin: 0 0 8px; font-size: 20px; font-weight: 700;">
                                Hey {audience}! 👋
                            </h2>
                            <p style="color: #686B78; font-size: 15px; line-height: 1.5; margin: 0;">
                                We know you're craving something delicious. Here's a special treat just for you!
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Quick Info Cards -->
                    <tr>
                        <td style="padding: 24px 20px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td width="33%" style="padding: 0 4px;">
                                        <div style="background: #FAFAFA; border-radius: 10px; padding: 16px 12px; text-align: center;">
                                            <div style="font-size: 24px; margin-bottom: 6px;">⚡</div>
                                            <p style="color: #1C1C1C; font-size: 12px; margin: 0; font-weight: 600;">FAST</p>
                                            <p style="color: #93959F; font-size: 11px; margin: 4px 0 0;">30 min avg</p>
                                        </div>
                                    </td>
                                    <td width="33%" style="padding: 0 4px;">
                                        <div style="background: #FAFAFA; border-radius: 10px; padding: 16px 12px; text-align: center;">
                                            <div style="font-size: 24px; margin-bottom: 6px;">⭐</div>
                                            <p style="color: #1C1C1C; font-size: 12px; margin: 0; font-weight: 600;">TOP RATED</p>
                                            <p style="color: #93959F; font-size: 11px; margin: 4px 0 0;">4.5+ rating</p>
                                        </div>
                                    </td>
                                    <td width="33%" style="padding: 0 4px;">
                                        <div style="background: #FAFAFA; border-radius: 10px; padding: 16px 12px; text-align: center;">
                                            <div style="font-size: 24px; margin-bottom: 6px;">🛡️</div>
                                            <p style="color: #1C1C1C; font-size: 12px; margin: 0; font-weight: 600;">SAFE</p>
                                            <p style="color: #93959F; font-size: 11px; margin: 4px 0 0;">Best practices</p>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Coupon Code Box -->
                    <tr>
                        <td style="padding: 0 24px 24px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td style="background: #FFF6E8; border: 1px dashed #FC8019; border-radius: 8px; padding: 16px;">
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td width="40" style="vertical-align: middle;">
                                                    <div style="width: 36px; height: 36px; background: #FC8019; border-radius: 50%; text-align: center; line-height: 36px;">
                                                        <span style="font-size: 18px;">🏷️</span>
                                                    </div>
                                                </td>
                                                <td style="padding-left: 12px; vertical-align: middle;">
                                                    <p style="color: #93959F; font-size: 11px; margin: 0; text-transform: uppercase;">Use Code</p>
                                                    <p style="color: #1C1C1C; font-size: 16px; margin: 2px 0 0; font-weight: 700; letter-spacing: 1px;">YUMMY20</p>
                                                </td>
                                                <td align="right" style="vertical-align: middle;">
                                                    <span style="color: #FC8019; font-size: 12px; font-weight: 600;">COPY →</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- CTA Button -->
                    <tr>
                        <td style="padding: 0 24px 32px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td align="center">
                                        <a href="{cta_link}" style="display: block; background: #60B246; color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 700; text-align: center; text-transform: uppercase; letter-spacing: 0.5px;">
                                            Order Now
                                        </a>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding-top: 12px;">
                                        <p style="color: #93959F; font-size: 12px; margin: 0;">
                                            🔥 Limited time offer • Valid till midnight
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Divider -->
                    <tr>
                        <td style="padding: 0 24px;">
                            <div style="height: 1px; background: #E8E8E8;"></div>
                        </td>
                    </tr>
                    
                    <!-- App Download Section -->
                    <tr>
                        <td style="padding: 24px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td>
                                        <p style="color: #1C1C1C; font-size: 14px; margin: 0 0 4px; font-weight: 600;">Get the app for best experience</p>
                                        <p style="color: #93959F; font-size: 12px; margin: 0;">Exclusive app-only offers waiting for you!</p>
                                    </td>
                                    <td align="right" width="120">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td style="padding-right: 8px;">
                                                    <div style="background: #1C1C1C; color: white; padding: 8px 12px; border-radius: 6px; font-size: 10px; text-align: center;">
                                                        <span style="font-size: 14px;">🍎</span><br>iOS
                                                    </div>
                                                </td>
                                                <td>
                                                    <div style="background: #1C1C1C; color: white; padding: 8px 12px; border-radius: 6px; font-size: 10px; text-align: center;">
                                                        <span style="font-size: 14px;">🤖</span><br>Android
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #1C1C1C; padding: 24px;">
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td align="center">
                                        <p style="color: #ffffff; font-size: 16px; margin: 0 0 4px; font-weight: 600;">{brand}</p>
                                        <p style="color: #93959F; font-size: 12px; margin: 0 0 16px;">Delivering happiness to your doorstep 🚴</p>
                                        
                                        <!-- Social Icons -->
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 16px;">
                                            <tr>
                                                <td style="padding: 0 6px;"><a href="#" style="color: #93959F; text-decoration: none; font-size: 18px;">📸</a></td>
                                                <td style="padding: 0 6px;"><a href="#" style="color: #93959F; text-decoration: none; font-size: 18px;">🐦</a></td>
                                                <td style="padding: 0 6px;"><a href="#" style="color: #93959F; text-decoration: none; font-size: 18px;">📘</a></td>
                                            </tr>
                                        </table>
                                        
                                        <p style="color: #686B78; font-size: 11px; margin: 0;">
                                            <a href="#" style="color: #686B78; text-decoration: none;">Unsubscribe</a> &nbsp;•&nbsp;
                                            <a href="#" style="color: #686B78; text-decoration: none;">Help</a> &nbsp;•&nbsp;
                                            <a href="#" style="color: #686B78; text-decoration: none;">Terms</a>
                                        </p>
                                        <p style="color: #4A4A4A; font-size: 10px; margin: 12px 0 0;">
                                            © 2024 {brand}. All rights reserved.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
</body>
</html>
"""
        subject = f"🍔 {offer} | Order now from {brand}!"
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

        # Clean up code block formatting if present
        if html.startswith("```html"):
            html = html.replace("```html", "").replace("```", "").strip()
            
        if html.endswith("```"):
            html = html.replace("```", "").strip()

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
        "cta_link": "https://shawarmer.com/"
    }

    # List of recipients
    recipients = [
        "velpulachaitu987@gmail.com"
    ]

    results = agent.send_campaign(context, recipients, use_llm=False)

if __name__ == "__main__":
    main()
