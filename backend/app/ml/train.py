import re
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ============================================================
# 2. CONFIGURATION
# ============================================================

DATASET_PATH = "ocean_hazard_dataset.csv"

MODEL_PATH = "ocean_hazard_lr_model.pkl"

TEXT_COLUMN = "text"
TARGET_COLUMN = "hazard_type"

RANDOM_STATE = 42


# ============================================================
# 3. TEXT PREPROCESSING
# ============================================================

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)

    # Remove HTML
    text = re.sub(r"<.*?>", " ", text)

    # Remove mentions
    text = re.sub(r"@\w+", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text


# ============================================================
# 4. LOAD DATASET
# ============================================================

print("=" * 70)
print("        OCEAN HAZARD AI-GIS MODEL TRAINING")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print("\nDataset shape:")
print(df.shape)

print("\nDataset columns:")
print(df.columns.tolist())


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

if TEXT_COLUMN not in df.columns:
    raise ValueError(
        f"Text column '{TEXT_COLUMN}' not found.\n"
        f"Available columns: {df.columns.tolist()}"
    )

if TARGET_COLUMN not in df.columns:
    raise ValueError(
        f"Target column '{TARGET_COLUMN}' not found.\n"
        f"Available columns: {df.columns.tolist()}"
    )


# ============================================================
# 6. REMOVE MISSING VALUES
# ============================================================

print("\nMissing values before cleaning:")

print(
    df[[TEXT_COLUMN, TARGET_COLUMN]]
    .isnull()
    .sum()
)


df = df.dropna(
    subset=[
        TEXT_COLUMN,
        TARGET_COLUMN
    ]
).copy()


# ============================================================
# 7. TEXT CLEANING
# ============================================================

print("\nCleaning text...")

df[TEXT_COLUMN] = df[TEXT_COLUMN].apply(clean_text)


# Remove empty text
df = df[df[TEXT_COLUMN].str.len() > 0].copy()


# ============================================================
# 8. PREPARE X AND Y
# ============================================================

X = df[TEXT_COLUMN]

y = df[TARGET_COLUMN]


print("\nNumber of samples:", len(df))

print("\nHazard distribution:")
print(y.value_counts())


# ============================================================
# 9. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# 10. WORD TF-IDF
# ============================================================

word_tfidf = TfidfVectorizer(

    # Unigrams + bigrams
    ngram_range=(1, 2),

    # Ignore common English words
    stop_words="english",

    # Minimum document frequency
    min_df=2,

    # Maximum number of features
    max_features=20000,

    # Reduce effect of repeated words
    sublinear_tf=True
)


# ============================================================
# 11. CHARACTER TF-IDF
# ============================================================

char_tfidf = TfidfVectorizer(

    analyzer="char_wb",

    # Character n-grams
    ngram_range=(3, 5),

    min_df=2,

    max_features=20000,

    sublinear_tf=True
)


# ============================================================
# 12. FEATURE UNION
# ============================================================

features = FeatureUnion([

    (
        "word_tfidf",
        word_tfidf
    ),

    (
        "char_tfidf",
        char_tfidf
    )

])


# ============================================================
# 13. LINEAR SVC CLASSIFIER
# ============================================================

classifier = LinearSVC(
    class_weight="balanced"
)


# ============================================================
# 14. COMPLETE PIPELINE
# ============================================================

final_model = Pipeline([

    (
        "features",
        features
    ),

    (
        "classifier",
        classifier
    )

])


print("\nPipeline:")
print(final_model)


# ============================================================
# 15. MODEL TRAINING
# ============================================================

print("\n" + "=" * 70)
print("TRAINING MODEL")
print("=" * 70)

final_model.fit(
    X_train,
    y_train
)

print("\nTraining completed.")


# ============================================================
# 16. TEST PREDICTIONS
# ============================================================

y_pred = final_model.predict(
    X_test
)


# ============================================================
# 17. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)

print(
    f"\nAccuracy: {accuracy:.4f}"
)


# ============================================================
# 18. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# 19. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=final_model.classes_
)

print("\nConfusion Matrix:")

print(cm)


# ============================================================
# 20. DISPLAY CONFUSION MATRIX
# ============================================================

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=final_model.classes_
)

fig, ax = plt.subplots(
    figsize=(9, 7)
)

disp.plot(
    ax=ax,
    xticks_rotation=45
)

plt.title(
    "Ocean Hazard Classification - Confusion Matrix"
)

plt.tight_layout()

plt.show()


# ============================================================
# 21. MODEL PERFORMANCE SUMMARY
# ============================================================

report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)

print("\n" + "=" * 70)
print("FINAL PERFORMANCE")
print("=" * 70)

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Macro F1 : {report['macro avg']['f1-score']:.4f}"
)

print(
    f"Weighted F1 : {report['weighted avg']['f1-score']:.4f}"
)


# ============================================================
# 22. SAVE COMPLETE MODEL
# ============================================================

print("\n" + "=" * 70)
print("SAVING MODEL")
print("=" * 70)

joblib.dump(
    final_model,
    MODEL_PATH
)

print(
    f"\nModel saved successfully:"
)

print(
    MODEL_PATH
)


# ============================================================
# 23. TEST PREDICTIONS
# ============================================================

test_texts = [

    "A severe tropical cyclone has formed over the Arabian Sea.",

    "Heavy rainfall caused the river to overflow and flood nearby homes.",

    "A damaged tanker is releasing diesel into coastal waters.",

    "Large ocean swells are making navigation dangerous.",

    "Authorities issued a hurricane warning for coastal districts.",

    "An oil sheen was observed around a damaged vessel.",

    "Several streets are completely submerged after continuous rainfall.",

    "Ferry operations were suspended because of extremely dangerous swells."

]


print("\n" + "=" * 70)
print("TEST PREDICTIONS")
print("=" * 70)


predictions = final_model.predict(
    test_texts
)


for text, prediction in zip(
    test_texts,
    predictions
):

    print("\nText:")
    print(text)

    print(
        "Prediction:",
        prediction
    )

    print("-" * 60)


# ============================================================
# 24. DECISION SCORES
# ============================================================

print("\n" + "=" * 70)
print("DECISION SCORES")
print("=" * 70)


decision_scores = final_model.decision_function(
    test_texts
)


for i, text in enumerate(test_texts):

    print("\nText:")
    print(text)

    print(
        "\nPrediction:",
        predictions[i]
    )

    print("\nScores:")

    for class_name, score in zip(
        final_model.classes_,
        decision_scores[i]
    ):

        print(
            f"{class_name:30s} : {score:.4f}"
        )


# ============================================================
# 25. LOAD SAVED MODEL TEST
# ============================================================

print("\n" + "=" * 70)
print("TESTING SAVED MODEL")
print("=" * 70)


loaded_model = joblib.load(
    MODEL_PATH
)


sample_text = (
    "A tanker is leaking diesel into coastal waters."
)


prediction = loaded_model.predict(
    [sample_text]
)[0]


print("\nText:")
print(sample_text)

print(
    "\nPrediction:",
    prediction
)


# ============================================================
# 26. FINAL INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("MODEL TRAINING COMPLETED")
print("=" * 70)

print(
    "\nClasses:"
)

for class_name in final_model.classes_:
    print(
        "-",
        class_name
    )

print(
    "\nSaved model:",
    MODEL_PATH
)

print(
    "\nModel type:",
    type(final_model)
)

print(
    "\nPipeline steps:",
    list(final_model.named_steps.keys())
)

print("\nDone.")
