

# Sentiment Analyzer

Food Review Analyzer is a web application that helps analyze food product reviews.
It uses Machine Learning to predict sentiment and AI to generate smart responses.

The app is built using **Streamlit**, so it runs directly in the browser.

---

## What this project consists of

This project has five main parts.

* **Sentiment Analysis**
  A Machine Learning model checks whether a review is Positive, Negative, or Neutral.

* **AI Response Generator**
  Based on the review and sentiment, AI generates a helpful response.

* **Sidebar Chatbot**
  Users can ask general questions and get AI powered answers.

* **Food Category Selection**
  Reviews are analyzed based on selected food category and sub category.

* **Email Notification**
  Users can receive the AI response on their email.

---

## Main Features

* Analyze food reviews instantly
* Predict sentiment using ML
* Generate AI based feedback
* Chat with AI assistant in sidebar
* Works for human food, pet food, animal feed, and processed food
* Optional email delivery of results
* Simple and interactive UI

---

## Project Files Explained

* `app.py`
  Main Streamlit application file. Handles UI and user interaction.

* `ml_model.py`
  Contains Machine Learning model for sentiment prediction.

* `ai_model.py`
  Generates AI responses based on review and sentiment.

* `chatbot.py`
  Handles sidebar chatbot functionality.

* `email_utils.py`
  Sends analysis results to user email.

* `food_reviews.xlsx`
  Dataset used for training the ML model.

* `requirements.txt`
  List of required Python libraries.

---

## How the App Works

1. User selects a food category
2. User enters a food review
3. ML model predicts sentiment
4. AI generates a response
5. Result is shown on screen
6. Email is sent if user provides email

---

## How to Run the App

Run locally.

```bash
streamlit run app.py
```

Or deploy on Streamlit Cloud by pushing the code to GitHub.

---

## Environment Setup

API keys and email credentials are stored securely using **Streamlit Secrets**.

Required secrets.

```toml
OPEN_AI_API_KEY = "your_openai_key"
SMTP_EMAIL = "your_email"
SMTP_PASSWORD = "your_email_app_password"
```

Do not upload secrets to GitHub.

---

## Use Case

* Product feedback analysis
* Customer support automation
* Food quality monitoring
* AI powered review summarization


