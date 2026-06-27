"""Train disease prediction model from medicine combinations."""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../datasets/disease_training.csv'))

    # Normalize medicine names in training data
    df['medicines_normalized'] = df['medicines'].apply(
        lambda x: ' '.join(sorted([m.strip().lower() for m in x.split('|')]))
    )

    X = df['medicines_normalized']
    y = df['disease']

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_vec = vectorizer.fit_transform(X)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_vec, y_enc)

    model_dir = os.path.dirname(__file__)
    with open(os.path.join(model_dir, 'disease_model.pkl'), 'wb') as f:
        pickle.dump({'model': clf, 'vectorizer': vectorizer, 'label_encoder': le}, f)

    print(f"Model trained on {len(df)} samples, {len(le.classes_)} diseases.")
    print("Diseases:", list(le.classes_))

if __name__ == '__main__':
    train()
