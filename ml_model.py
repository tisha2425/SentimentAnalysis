import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_excel("food reviews.xlsx")
df.columns = df.columns.str.strip()
df = df.dropna()

# Remove Neutral for training
df = df[df['sentiment'] != 'Neutral']

# ================================
# DATA BALANCING (UNDERSAMPLING)
# ================================

# Separate classes
df_positive = df[df['sentiment'] == 'Positive']
df_negative = df[df['sentiment'] == 'Negative']

# Find minority class size
min_size = min(len(df_positive), len(df_negative))

# Undersample majority class
df_positive_balanced = df_positive.sample(n=min_size, random_state=42)
df_negative_balanced = df_negative.sample(n=min_size, random_state=42)

# Combine balanced data
df = pd.concat([df_positive_balanced, df_negative_balanced])

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# Combine text
df['Review'] = df['Review_Title'] + " " + df['Text']
df['Review_Length'] = df['Review'].apply(len)
df = df[df['Review_Length'] > 30]

X_text = df['Review']
y = df['sentiment']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Vectorizer
tfidf = TfidfVectorizer(stop_words='english', max_features=3000)
X = tfidf.fit_transform(X_text)

# Model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X, y_encoded)

# Prediction function
def predict_sentiment(review_text):
    vec = tfidf.transform([review_text])
    probs = model.predict_proba(vec)[0]
    pos_index = list(le.classes_).index("Positive")
    pos_prob = probs[pos_index]

    # if pos_prob >= 0.65:
    #     return "Positive"
    # elif pos_prob <= 0.35:
    #     return "Negative"
    # else:
    #     return "Neutral"

    # if pos_prob >= 0.55:
    #     return "Positive"
    # elif pos_prob <= 0.35:
    #     return "Negative"
    # else:
    #     return "Neutral"    

    if pos_prob >= 0.45:
        return "Positive"
    elif pos_prob <= 0.30:
        return "Negative"
    else:
        return "Neutral"
 