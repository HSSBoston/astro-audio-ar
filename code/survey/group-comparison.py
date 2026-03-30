import math
import pandas as pd
from scipy import stats

# Load CSV
data = pd.read_csv("data/responses.csv")

# Question columns (Q1-Q10)
questionCols = [
    data.columns[9],
    data.columns[10],
    data.columns[11],
    data.columns[12],
    data.columns[13],
    data.columns[14],
    data.columns[15],
    data.columns[16],
    data.columns[17],
    data.columns[18],
]

# Correct answers
correctAnswers = [
    "Constellation 1",
    "Constellation 2",
    "Constellation 2",
    "Constellation 1",
    "Constellation 2",
    "Constellation 2",
    "Constellation 1",
    "Audio 2",
    "Audio 2",
    "Audio 1",
]

# Create correctness columns
for i, questionCol in enumerate(questionCols):
    correctCol = f"q{i + 1}Correct"
    data[correctCol] = (data[questionCol] == correctAnswers[i]).astype(int)

# Compute per-participant accuracy
correctCols = [f"q{i + 1}Correct" for i in range(10)]
data["accuracy"] = data[correctCols].mean(axis=1)

# Grouping columns
musicCol = "Do you have prior experience with playing, making, or learning music beyond the regular high school curriculum (beyond required music classes) or outside of school?"
astronomyCol = "How would you rate your knowledge on astronomy?"

# Music groups
musicGroup = data[data[musicCol] == "Yes"]["accuracy"]
noMusicGroup = data[data[musicCol] == "No"]["accuracy"]

# Astronomy groups
lowAstronomyGroup = data[
    data[astronomyCol].isin(["Not knowledgeable", "Slightly knowledgeable"])
]["accuracy"]

highAstronomyGroup = data[
    data[astronomyCol].isin(["Moderately knowledgeable", "Very knowledgeable"])
]["accuracy"]

# Welch two-sample t-tests
musicTest = stats.ttest_ind(musicGroup, noMusicGroup, equal_var=False)
astronomyTest = stats.ttest_ind(lowAstronomyGroup, highAstronomyGroup, equal_var=False)

def computeCohensD(group1, group2):
    n1 = len(group1)
    n2 = len(group2)

    mean1 = group1.mean()
    mean2 = group2.mean()

    sd1 = group1.std(ddof=1)
    sd2 = group2.std(ddof=1)

    pooledVariance = ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)
    pooledSd = math.sqrt(pooledVariance)

    cohensD = (mean1 - mean2) / pooledSd
    return cohensD

musicCohensD = computeCohensD(musicGroup, noMusicGroup)
astronomyCohensD = computeCohensD(lowAstronomyGroup, highAstronomyGroup)

# Print results
print("Music vs No Music")
print("nMusic =", len(musicGroup))
print("nNoMusic =", len(noMusicGroup))
print("meanMusic =", musicGroup.mean())
print("meanNoMusic =", noMusicGroup.mean())
print("tStat =", musicTest.statistic)
print("pValue =", musicTest.pvalue)
print("cohensD =", musicCohensD)
print()

print("Low vs Higher Astronomy Knowledge")
print("nLowAstronomy =", len(lowAstronomyGroup))
print("nHighAstronomy =", len(highAstronomyGroup))
print("meanLowAstronomy =", lowAstronomyGroup.mean())
print("meanHighAstronomy =", highAstronomyGroup.mean())
print("tStat =", astronomyTest.statistic)
print("pValue =", astronomyTest.pvalue)
print("cohensD =", astronomyCohensD)