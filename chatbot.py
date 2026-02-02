from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# READ YOUR VARIABLE (custom name)
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# SAFETY CHECK
if not OPEN_AI_API_KEY:
    raise ValueError("open_ai_api_key is not set in environment variables")

# PASS IT EXPLICITLY (IMPORTANT)
client = OpenAI(api_key=OPEN_AI_API_KEY)


# ================================
# SYSTEM PROMPT (IMPORTANT)
# ================================
SYSTEM_PROMPT = """
You are a friendly, professional AI assistant embedded as a small chat widget
on the bottom-right corner of a website.

You chat naturally like ChatGPT and help users with general questions,
navigation support, and feature explanations.

Human-in-the-loop rules:
- You are NOT human.
- If the query involves complaints, payments, personal data,
  frustration, or business-critical decisions, escalate politely to a human.
- Keep responses concise, calm, and conversational.
- Never fabricate information.
"""

# ================================
# AI RESPONSE FUNCTION
# ================================
def generate_ai_response1(user_input, sentiment=None, category=None, sub_category=None):
    """
    LLM-powered ChatGPT-style response with human-in-the-loop safety.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Safe fallback (human escalation tone)
        return (
            "I’m having a bit of trouble responding right now. "
            "Let me connect you with a human team member for help 🙂"
        )
