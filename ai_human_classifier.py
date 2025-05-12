import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.inspection import permutation_importance

# plot more relations
# document the process 
# work on testing 

fallback_stopwords = set([
    'the', 'and', 'is', 'in', 'it', 'you', 'of', 'for', 'on', 'with', 'as', 'this',
    'that', 'to', 'a', 'an', 'are', 'be', 'was', 'were', 'by', 'at', 'or', 'from'
])

def basic_sentiment(text):
    positive = ['love', 'great', 'excellent', 'good', 'wonderful', 'best', 'amazing']
    negative = ['hate', 'bad', 'terrible', 'worst', 'awful', 'poor']
    score = 0
    words = text.lower().split()
    score += sum(w in positive for w in words)
    score -= sum(w in negative for w in words)
    return score / max(len(words), 1)

df = pd.read_csv("AI_Human.csv")
df.columns = ['text', 'label']

df = df.sample(n=8000, random_state=42).reset_index(drop=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    return text

df['cleaned_text'] = df['text'].astype(str).apply(clean_text)

def extract_features(df):
    features = pd.DataFrame()
    features['char_count'] = df['cleaned_text'].apply(len)
    features['word_count'] = df['cleaned_text'].apply(lambda x: len(x.split()))
    features['avg_word_len'] = df['cleaned_text'].apply(lambda x: np.mean([len(w) for w in x.split()]) if x else 0)
    features['sentence_std'] = df['text'].apply(lambda x: np.std([len(s.split()) for s in re.split(r'[.!?]', x) if s]))
    features['question_marks'] = df['text'].apply(lambda x: x.count('?'))
    features['parentheses'] = df['text'].apply(lambda x: x.count('(') + x.count(')'))
    features['semicolons'] = df['text'].apply(lambda x: x.count(';'))

    discourse_markers = ['however', 'therefore', 'moreover', 'thus', 'furthermore'] # figure out how to consider comma
    features['discourse_markers'] = df['cleaned_text'].apply(
        lambda x: sum(w in discourse_markers for w in x.split())
    )

    features['sentiment'] = df['cleaned_text'].apply(basic_sentiment)

    pronouns = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    features['authorial_voice'] = df['cleaned_text'].apply(
        lambda x: sum(x.split().count(p) for p in pronouns)
    )

    equivocal = ['maybe', 'perhaps', 'possibly', 'might', 'could', 'seems'] # consider comma
    features['equivocal'] = df['cleaned_text'].apply(
        lambda x: sum(x.split().count(w) for w in equivocal)
    )

    return features

linguistic_features = extract_features(df)

vectorizer = TfidfVectorizer(max_features=100)
tfidf_matrix = vectorizer.fit_transform(df['cleaned_text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=[f"tfidf_{i}" for i in range(100)])

X = pd.concat([linguistic_features.reset_index(drop=True), tfidf_df], axis=1)
y = df['label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

perm = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
importances = perm.importances_mean[:len(linguistic_features.columns)]
feature_names = linguistic_features.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title("Top Linguistic Features by Importance (Sampled Data)")
plt.xlabel("Permutation Importance")
plt.tight_layout()
plt.show()
