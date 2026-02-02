import os
import requests
from dotenv import load_dotenv

# ==============================
# LOAD API KEY
# ==============================
load_dotenv("myapi.env")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# ==============================
# OPENAI RESPONSE FUNCTION
# ==============================
def openai_generate_response(prompt):
    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "input": prompt
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return None

    data = response.json()

    try:
        return data["output"][0]["content"][0]["text"]
    except:
        return None


# ==============================
# MAIN AI FUNCTION
# ==============================
def generate_ai_response(review_text, sentiment, food_category, sub_category):

    prompt = f"""
You are a customer support assistant for a FOOD PRODUCT brand.
strictly recommend three products based on the sentiment and category.

Food Category: {food_category}
Sub-Category: {sub_category}
Sentiment (from ML model): {sentiment}

Customer Review:
"{review_text}"

RULES:
- Do NOT analyze sentiment again
- Follow category and sub-category strictly
- Do NOT mention AI or ML
- Keep response professional and short

RESPONSE LOGIC:

If sentiment is Positive:
- Thank the customer
- Mention quality (taste, freshness, nutrition)
- Recommend exactly 3 related products

If sentiment is Negative:
- Apologize politely
- Acknowledge the issue
- Assure customer support help
- Do NOT recommend products

If sentiment is Neutral:
- Thank the customer
- Ask for more feedback
- Do NOT recommend products

FORMAT FOR RECOMMENDATIONS:
- Product 1
- Product 2
- Product 3
"""

    reply = openai_generate_response(prompt)

    if reply is None:
        return "AI response could not be generated."

    return reply
##### CHATBOT FUNCTION FOR GENERAL QUESTIONS #####

def chatbot_response(user_question):
    prompt = f"""
    You are a helpful food product assistant.

    Answer the user's question clearly and politely.
    Keep answers short and easy to understand.

    User Question:
    "{user_question}"
    """

    return openai_generate_response(prompt)

# ==============================
