import pandas as pd
from scipy.stats import spearmanr

# === 1. Load data ===
df = pd.read_csv("data/responses.csv")

# === 2. Define column names ===

ENJOYMENT_COL = "Did you enjoy exploring celestial objects based on their musical representations?"
MOTIVATION_COL = "After listening to the music of celestial objects, do you feel as if you want to explore and discover more about them?"

BEFORE_COL = "Before this survey, had you ever felt or perceived any connection between celestial objects and musical expression?"
AFTER_COL = "Based on your experience listening to several musical pieces translated from constellations, do you feel or perceive a connection between constellations and musical expression? "

# === 3. Mapping ===

likert_map = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neither agree nor disagree": 3,
    "Agree": 4,
    "Strongly agree": 5
}

df["enjoyment_num"] = df[ENJOYMENT_COL].map(likert_map)
df["motivation_num"] = df[MOTIVATION_COL].map(likert_map)

# === 4. Convert perception ===

def before_map(x):
    if pd.isna(x):
        return None
    x = str(x).lower()
    if x in ["strongly agree", "agree"]:
        return 1
    else:
        return 0
#     if "yes" in x:
#         return 1
#     else:
#         return 0

def after_map(x):
    if pd.isna(x):
        return None
    x = str(x).lower()
    if x in ["strongly agree", "agree"]:
        return 1
    else:
        return 0

df["before_num"] = df[BEFORE_COL].apply(before_map)
df["after_num"] = df[AFTER_COL].apply(after_map)

df["shift"] = df["after_num"] - df["before_num"]

# === 5. Accuracy ===
df["accuracy"] = df["Score"]

# === 6. Drop missing values ===

df_corr1 = df.dropna(subset=["enjoyment_num", "motivation_num"])
df_corr2 = df.dropna(subset=["accuracy", "shift"])

# NEW: accuracy ↔ motivation
df_corr3 = df.dropna(subset=["accuracy", "motivation_num"])

# === 7. Compute correlations ===

# (1) Enjoyment ↔ Motivation
corr1, p1 = spearmanr(df_corr1["enjoyment_num"], df_corr1["motivation_num"])

# (2) Accuracy ↔ Perception shift
corr2, p2 = spearmanr(df_corr2["accuracy"], df_corr2["shift"])

# (3) Accuracy ↔ Motivation  ⭐ NEW
corr3, p3 = spearmanr(df_corr3["accuracy"], df_corr3["motivation_num"])

# === 8. Output ===

print("=== Correlation Results ===")
print(f"Enjoyment ↔ Motivation: rho = {corr1:.3f}, p = {p1:.5f}")
print(f"Accuracy ↔ Perception shift: rho = {corr2:.3f}, p = {p2:.5f}")
print(f"Accuracy ↔ Motivation: rho = {corr3:.3f}, p = {p3:.5f}")
