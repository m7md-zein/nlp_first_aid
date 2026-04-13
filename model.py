"""
Member 3 - NLP Model
Handles: TF-IDF feature extraction, Logistic Regression training, evaluation, model saving
"""

import os
import csv
import pickle
import math
from collections import defaultdict
from preprocessing import preprocess_text

# Base directory = folder where model.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ─── Tiny TF-IDF implementation (no sklearn needed) ──────────────────────────

class TfidfVectorizer:
    """Simple TF-IDF vectorizer built from scratch."""

    def __init__(self, max_features=500):
        self.max_features = max_features
        self.vocab = {}          # word -> index
        self.idf = {}            # word -> idf score
        self.feature_names = []  # ordered list of words

    def fit(self, docs):
        N = len(docs)
        df = defaultdict(int)
        for doc in docs:
            for word in set(doc.split()):
                df[word] += 1
        # Compute IDF
        all_idf = {w: math.log((N + 1) / (cnt + 1)) + 1 for w, cnt in df.items()}
        # Keep top max_features by IDF (most discriminating words)
        sorted_words = sorted(all_idf, key=lambda w: -all_idf[w])[:self.max_features]
        self.feature_names = sorted_words
        self.vocab = {w: i for i, w in enumerate(sorted_words)}
        self.idf = {w: all_idf[w] for w in sorted_words}
        return self

    def transform(self, docs):
        result = []
        for doc in docs:
            tokens = doc.split()
            tf = defaultdict(float)
            for t in tokens:
                tf[t] += 1
            n = max(len(tokens), 1)
            vec = [0.0] * len(self.vocab)
            for word, idx in self.vocab.items():
                if word in tf:
                    vec[idx] = (tf[word] / n) * self.idf[word]
            result.append(vec)
        return result

    def fit_transform(self, docs):
        self.fit(docs)
        return self.transform(docs)


# ─── Logistic Regression (one-vs-rest, from scratch) ─────────────────────────

class LogisticRegression:
    """Binary logistic regression via gradient descent."""

    def __init__(self, lr=0.1, epochs=500, regularization=0.01):
        self.lr = lr
        self.epochs = epochs
        self.reg = regularization
        self.weights = None
        self.bias = 0.0

    def _sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-max(-500, min(500, z))))

    def fit(self, X, y):
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0
        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                z = sum(w * x for w, x in zip(self.weights, xi)) + self.bias
                pred = self._sigmoid(z)
                err = pred - yi
                self.weights = [
                    w - self.lr * (err * x + self.reg * w)
                    for w, x in zip(self.weights, xi)
                ]
                self.bias -= self.lr * err

    def predict_proba(self, x):
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
        return self._sigmoid(z)


class OneVsRestClassifier:
    """Multi-class classifier using one binary LR per class."""

    def __init__(self):
        self.classifiers = {}
        self.classes = []

    def fit(self, X, y):
        self.classes = sorted(set(y))
        for cls in self.classes:
            binary_y = [1 if label == cls else 0 for label in y]
            clf = LogisticRegression(lr=0.1, epochs=300)
            clf.fit(X, binary_y)
            self.classifiers[cls] = clf

    def predict(self, X):
        results = []
        for x in X:
            scores = {cls: self.classifiers[cls].predict_proba(x) for cls in self.classes}
            results.append(max(scores, key=scores.get))
        return results

    def predict_proba_single(self, x):
        """Return {class: probability} for a single sample."""
        return {cls: self.classifiers[cls].predict_proba(x) for cls in self.classes}


# ─── Training ─────────────────────────────────────────────────────────────────

def load_data(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(BASE_DIR, 'data', 'first_aid_data.csv')
    elif not os.path.isabs(csv_path):
        csv_path = os.path.join(BASE_DIR, 'data', 'first_aid_data.csv')
    questions, answers, intents = [], [], []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row['question'])
            answers.append(row['answer'])
            intents.append(row['intent'])
    return questions, answers, intents


def train_model(data_path=None):
    print("[1/4] Loading dataset...")
    questions, answers, intents = load_data(data_path)
    print(f"      {len(questions)} samples, {len(set(intents))} intents")

    print("[2/4] Preprocessing text...")
    processed = [preprocess_text(q) for q in questions]

    print("[3/4] Fitting TF-IDF and training model...")
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(processed)
    model = OneVsRestClassifier()
    model.fit(X, intents)

    print("[4/4] Evaluating on training data...")
    preds = model.predict(X)
    correct = sum(p == t for p, t in zip(preds, intents))
    accuracy = correct / len(intents) * 100
    print(f"      Training accuracy: {accuracy:.1f}%")

    # Save model + vectorizer
    model_dir = os.path.join(BASE_DIR, 'model')
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    with open(os.path.join(model_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)

    # Build intent -> best answer mapping
    intent_answers = {}
    for intent, answer in zip(intents, answers):
        if intent not in intent_answers:
            intent_answers[intent] = answer
    with open(os.path.join(model_dir, 'intent_answers.pkl'), 'wb') as f:
        pickle.dump(intent_answers, f)

    print("      Model saved to model/")
    return model, vectorizer, intent_answers, accuracy


def load_model():
    """Load saved model artefacts."""
    model_dir = os.path.join(BASE_DIR, 'model')
    with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(model_dir, 'intent_answers.pkl'), 'rb') as f:
        intent_answers = pickle.load(f)
    return model, vectorizer, intent_answers


if __name__ == "__main__":
    train_model()
