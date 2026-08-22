import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("data/ocean_hazard_dataset.csv")

df = df.dropna(subset=["text", "hazard_type"])
df["text"] = df["text"].astype(str).str.lower()

X = df["text"]
y = df["hazard_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

word_tfidf = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=20000,
    min_df=2,
    sublinear_tf=True
)

char_tfidf = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    max_features=20000,
    min_df=2,
    sublinear_tf=True
)

features = FeatureUnion([
    ("word_tfidf", word_tfidf),
    ("char_tfidf", char_tfidf)
])

model = Pipeline([
    ("features", features),
    ("classifier", LinearSVC(class_weight="balanced"))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, "ocean_hazard_model.pkl")

test_texts = [
    "A severe tropical cyclone is approaching the coast.",
    "Heavy rainfall has caused rivers to overflow.",
    "A tanker is leaking diesel into coastal waters.",
    "Large ocean swells are making navigation dangerous."
]

predictions = model.predict(test_texts)

for text, prediction in zip(test_texts, predictions):
    print(text)
    print(prediction)
