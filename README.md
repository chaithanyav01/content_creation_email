# 📧 Email Marketing Agent

AI-powered email marketing agent that generates beautiful HTML emails and sends them via Gmail SMTP.

## ✨ Features

- 🤖 **AI Content Generation** - Uses OpenAI GPT-4 to create compelling marketing emails
- 🎨 **Beautiful Templates** - Responsive HTML email templates with professional design
- 🖼️ **Image Support** - Embed images via URL or local files
- 📬 **Gmail SMTP** - Send emails through your Gmail account
- 📊 **Campaign Support** - Send to multiple recipients with tracking

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env with your credentials
```

### 3. Gmail App Password Setup

1. Go to [Google Account Settings](https://myaccount.google.com)
2. Enable **2-Step Verification**
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate a new app password for "Mail"
5. Copy the 16-character password to your `.env` file

### 4. Run the Agent

```bash
python email_agent.py
```

## 📖 Usage Examples

### Basic Usage

```python
from email_agent import EmailAgent

agent = EmailAgent()

# Define your campaign
context = {
    "brand": "Shawarmer",
    "offer": "20% off on chicken wraps",
    "audience": "Weekend food lovers",
    "image_url": "https://example.com/food.jpg",
    "cta_link": "https://shawarmer.com/order"
}

# Send to recipients
recipients = ["customer1@email.com", "customer2@email.com"]
results = agent.send_campaign(context, recipients, use_llm=True)
```

### Using Default Template (No API Needed)

```python
# Send without LLM - uses built-in responsive template
results = agent.send_campaign(context, recipients, use_llm=False)
```

### Send Single Email

```python
# Generate and send one email
email_content = agent.create_default_email(context)
agent.send_email("user@example.com", email_content["subject"], email_content["html"])
```

### Embed Local Images

```python
agent.send_email(
    to_email="user@example.com",
    subject="Check this out!",
    html_content='<img src="cid:hero_image">',
    embedded_images=[
        {"path": "images/hero.jpg", "cid": "hero_image"}
    ]
)
```

## 📁 Project Structure

```
content_creation_email/
├── email_agent.py      # Main agent code
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .env                # Your credentials (create this)
└── README.md           # This file
```

## ⚙️ Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `SENDER_EMAIL` | Your Gmail address |
| `SENDER_APP_PASSWORD` | Gmail app password (16 chars) |

## 🔒 Security Notes

- Never commit `.env` to version control
- Use App Passwords, not your main Gmail password
- Keep your OpenAI API key private

## 📈 Production Tips

For production use, consider:
- **SendGrid** or **Amazon SES** instead of Gmail SMTP
- Email tracking (opens/clicks)
- A/B testing for subject lines
- Unsubscribe handling
- Rate limiting

## 📝 License

MIT License
