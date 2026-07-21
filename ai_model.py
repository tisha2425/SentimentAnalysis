import os
from dotenv import load_dotenv
from openai import OpenAI


import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPEN_AI_API_KEY"]
)

def openai_generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
    
# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================
load_dotenv("myapi.env")

api_key = os.getenv("OPEN_AI_API_KEY")

if not api_key:
    raise ValueError("OPEN_AI_API_KEY not found in myapi.env")

client = OpenAI(api_key=api_key)

# ==============================
# OPENAI RESPONSE FUNCTION
# ==============================
def openai_generate_response(prompt):
    """
    Sends a prompt to OpenAI and returns the generated response.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional customer support assistant "
                        "for a food products company."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Unable to generate AI response at the moment."


# ==============================
# AI REVIEW RESPONSE
# ==============================
def generate_ai_response(
    review_text,
    sentiment,
    food_category,
    sub_category
):

    prompt = f"""
You are a customer support executive for a food products company.

Food Category:
{food_category}

Sub Category:
{sub_category}

Customer Sentiment:
{sentiment}

Customer Review:
"{review_text}"

Instructions:

1. Never analyze the sentiment again.
2. Use the sentiment provided.
3. Keep the reply under 120 words.
4. Do not mention AI, machine learning, or sentiment analysis.

If sentiment is Positive:
- Thank the customer.
- Appreciate their feedback.
- Mention the product quality.
- Recommend exactly three products from the same category.

If sentiment is Negative:
- Apologize politely.
- Acknowledge the issue.
- Assure them their concern is important.
- Do not recommend any products.

If sentiment is Neutral:
- Thank the customer.
- Ask them for additional feedback.
- Do not recommend products.

Recommendation format:

Recommended Products:
• Product 1
• Product 2
• Product 3
"""

    return openai_generate_response(prompt)


# ==============================
# FOOD CHATBOT
# ==============================
def chatbot_response(user_question):

    prompt = f"""
You are a helpful food product assistant.

Answer the user's question politely.

Rules:
- Keep the answer short.
- Be accurate.
- If asked about food, nutrition, products, ingredients, or storage, answer clearly.
- If you don't know something, politely say so.

User Question:
{user_question}
"""

    return openai_generate_response(prompt)
