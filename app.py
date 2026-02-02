import streamlit as st
from ml_model import predict_sentiment
from ai_model import generate_ai_response
from email_utils import send_email
from chatbot import generate_ai_response1
# import speech_recognition as sr
# import pyttsx3
import random
import time
import os
import pandas as pd
# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Food Review Analyzer",
    layout="wide"
)
# ================================
# STORE REVIEW HISTORY
# ================================
if "review_history" not in st.session_state:
    st.session_state.review_history = []



# ================================
# GLOBAL CSS
# ================================
st.markdown("""
<style>
html, body, .stApp {
    height: 100vh;
    margin: 0;
    overflow-x: hidden;
}

@keyframes pinterestBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg,#f3d6da,#e6dacb,#dfe5e7,#ead7c3);
    background-size: 400% 400%;
    animation: pinterestBG 25s ease infinite;
}

.category-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.category-selected {
    border: 3px solid #ff6f61;
    box-shadow: 0 0 14px rgba(255,111,97,0.6);
}

.result-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    height: 350px;
}

.sentiment-positive { color: #2e7d32; font-size: 22px; font-weight: 700; }
.sentiment-negative { color: #c62828; font-size: 22px; font-weight: 700; }
.sentiment-neutral  { color: #ef6c00; font-size: 22px; font-weight: 700; }

.desc-box {
    background: #dcedc8;
    border-radius: 12px;
    padding: 12px;
    font-weight: 600;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================
quotes = [
    "🍽️ Good food builds healthy lives.",
    "🥗 Quality food creates trust.",
    "🌱 Better food, better well-being."
]
st.sidebar.markdown(f"### {random.choice(quotes)}")

st.sidebar.markdown("### ✨ Why Choose Us?")
st.sidebar.markdown("📊 Data-Driven Analysis")
st.sidebar.markdown("🤖 AI-Powered Insights")
st.sidebar.markdown("⚡ Fast & Accurate")
st.sidebar.markdown("🔍 Transparent Results")
st.sidebar.markdown("🌍 Works for all food types")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Customer Support")
st.sidebar.markdown("""
📧 support@foodreviewcare.com  
📱 +91 98765 43210  
⏰ Mon–Sat | 9 AM – 6 PM
""")

# ================================
# SIDEBAR CHATBOT (FINAL FIX)
# ================================

st.sidebar.markdown("---")

# Session state init
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# ================================
# LOAD REVIEW HISTORY FROM FILE
# ================================
if "review_history" not in st.session_state:
    if os.path.exists("review_history.csv"):
        st.session_state.review_history = pd.read_csv("review_history.csv").to_dict("records")
    else:
        st.session_state.review_history = []


# Chat toggle button
if st.sidebar.button("💬 Chat with Assistant"):
    st.session_state.chat_open = not st.session_state.chat_open

# Clear input BEFORE widget is created
if st.session_state.clear_input:
    st.session_state.sidebar_chat_input = ""
    st.session_state.clear_input = False

# Chat UI
if st.session_state.chat_open:
    st.sidebar.markdown("### 💬 Assistant")

    # Display chat history
    for msg in st.session_state.chat_messages:
        role = "You" if msg["role"] == "user" else "AI"
        st.sidebar.markdown(f"**{role}:** {msg['content']}")

    # Text input
    user_input = st.sidebar.text_input(
        "Ask a question",
        key="sidebar_chat_input"
    )

    # Send button
    if st.sidebar.button("Send"):
        if user_input.strip():

            # Save user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })

            # AI response
            ai_response = generate_ai_response1(
                user_input,
                "N/A",
                "General Query",
                "Sidebar Chatbot"
            )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": ai_response
            })

            # Request input clear on next run
            st.session_state.clear_input = True

            st.rerun()
# ================================
# TITLE
# ================================
st.markdown("<h1 style='text-align:center;'>Food Review Analyzer</h1>", unsafe_allow_html=True)

# ================================
# FOOD CATEGORY DATA
# ================================
categories = {
    "Human Food": {"img": "https://img.icons8.com/fluency/144/meal.png",
                   "desc": "Meals, snacks, restaurant food & diet-based human food"},
    "Pet Food": {"img": "https://img.icons8.com/fluency/144/dog-bowl.png",
                 "desc": "Food for dogs, cats, birds & pets"},
    "Animal Feed": {"img": "https://img.icons8.com/fluency/144/farm.png",
                    "desc": "Livestock & poultry feed"},
    "Processed Food": {"img": "https://img.icons8.com/fluency/144/ingredients.png",
                       "desc": "Packaged, frozen & ready-to-eat food"},
    "Other": {"img": "https://img.icons8.com/fluency/144/help.png",
              "desc": "Any other food category"}
}

if "food_category" not in st.session_state:
    st.session_state.food_category = "Human Food"

# ================================
# CATEGORY SELECTION
# ================================
st.markdown("## 🍴 Select Food Category")
cols = st.columns(5)

for col, (name, data) in zip(cols, categories.items()):
    with col:
        selected = st.session_state.food_category == name
        card_class = "category-card category-selected" if selected else "category-card"

        if st.button("", key=name):
            st.session_state.food_category = name
            st.rerun()

        st.markdown(f"""
        <div class="{card_class}">
            <img src="{data['img']}" width="80">
            <div style="font-weight:700;margin-top:8px;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

food_category = st.session_state.food_category

st.markdown(
    f"<div class='desc-box'>{food_category} — {categories[food_category]['desc']}</div>",
    unsafe_allow_html=True
)

# ================================
# SUB-CATEGORY
# ================================
if food_category == "Human Food":
    sub_category = st.radio("Sub-category:",
        ("Home-cooked", "Restaurant Food", "Snacks & Beverages", "Health / Diet Food"),
        horizontal=True)
elif food_category == "Pet Food":
    sub_category = st.radio("Sub-category:",
        ("Dog Food", "Cat Food", "Bird Food", "Fish Food"),
        horizontal=True)
elif food_category == "Animal Feed":
    sub_category = st.radio("Sub-category:",
        ("Cattle Feed", "Poultry Feed", "Goat / Sheep Feed", "Mixed Feed"),
        horizontal=True)
elif food_category == "Processed Food":
    sub_category = st.radio("Sub-category:",
        ("Ready-to-eat", "Frozen", "Canned", "Instant"),
        horizontal=True)
else:
    sub_category = st.text_input("Enter sub-category:")

# ================================
# CONTACT DETAILS
# ================================
st.markdown("### 👤 Your Contact Details")
c1, c2 = st.columns(2)
user_email = c1.text_input("Email (optional)")
user_phone = c2.text_input("Phone number (optional)")

# ================================
# REVIEW INPUT
# ================================
review = st.text_area("Enter your food product review:", height=120)
b1, b2 = st.columns(2)
analyze = b1.button("Analyze Review")
clear = b2.button("Clear")

if clear:
    st.experimental_rerun()

# ================================
# OUTPUT + EMAIL
# ================================
if analyze and review.strip():
    with st.spinner("Analyzing..."):
        time.sleep(1)
        sentiment = predict_sentiment(review)
        ai_reply = generate_ai_response(review, sentiment, food_category, sub_category)

    # ================================
    # SAVE REVIEW TO HISTORY (SESSION)
    # ================================
    st.session_state.review_history.append({
        "review": review,
        "sentiment": sentiment
    })

    # ================================
    # SAVE HISTORY TO CSV (PERSISTENT)
    # ================================
    pd.DataFrame(st.session_state.review_history).to_csv(
        "review_history.csv", index=False
    )

    # (rest of your existing UI code continues below)

# ai_reply = generate_ai_response(review, sentiment, food_category, sub_category)

    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="result-card">
            <h4>📊 Predicted Sentiment</h4>
            <div class="sentiment-positive">{sentiment}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="result-card">
            <h4>🤖 AI Response</h4>
            <p>{ai_reply}</p>
        </div>
        """, unsafe_allow_html=True)

    # ================================
    # CLEAN EMAIL FORMAT (FIXED)
    # ================================
    email_body = f"""Hello,

Thank you for sharing your food review with us.

--------------------------------------
Sentiment
--------------------------------------
{sentiment}

--------------------------------------
Category
--------------------------------------
{food_category}
Sub-category: {sub_category}

--------------------------------------
AI Response
--------------------------------------
{ai_reply}

--------------------------------------
Thank You
--------------------------------------
We truly appreciate your feedback.

Best regards,
Food Review Analyzer Team
"""

    if user_email:
        sent = send_email(
            to_email=user_email,
            subject="Your Food Review Analysis",
            body=email_body
        )

        if sent:
            st.success("📧 AI response sent to your email!")
        else:
            st.error("❌ Email could not be sent.")


# ================================
# PREVIOUS REVIEWS SECTION
# ================================
st.markdown("---")
st.markdown("## 🕘 Previous Reviews")

if st.session_state.review_history:
    for i, item in enumerate(reversed(st.session_state.review_history), start=1):
        st.markdown(f"""
        <div style="
            background:#ffffff;
            padding:12px;
            border-radius:12px;
            margin-bottom:10px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
        ">
            <strong>Review {i}</strong><br>
            <em>{item['review']}</em><br><br>
            <strong>Predicted Sentiment:</strong> {item['sentiment']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No reviews analyzed yet.")


