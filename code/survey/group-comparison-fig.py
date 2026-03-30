import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

data = pd.read_csv("data/responses.csv")

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

for i, questionCol in enumerate(questionCols):
    correctCol = f"q{i + 1}Correct"
    data[correctCol] = (data[questionCol] == correctAnswers[i]).astype(int)

correctCols = [f"q{i + 1}Correct" for i in range(10)]
data["accuracy"] = data[correctCols].mean(axis=1)

musicCol = "Do you have prior experience with playing, making, or learning music beyond the regular high school curriculum (beyond required music classes) or outside of school?"
astronomyCol = "How would you rate your knowledge on astronomy?"

lowAstronomyLabels = [
    "Not knowledgeable at all (novice)",
    "Slightly knowledgeable",
]

highAstronomyLabels = [
    "Moderately knowledgeable",
    "Very knowledgeable (expert)",
]

musicGroup = data[data[musicCol] == "Yes"]["accuracy"]
noMusicGroup = data[data[musicCol] == "No"]["accuracy"]

highAstronomyGroup = data[data[astronomyCol].isin(highAstronomyLabels)]["accuracy"]
lowAstronomyGroup = data[data[astronomyCol].isin(lowAstronomyLabels)]["accuracy"]

highAstronomyWithMusicGroup = data[
    (data[musicCol] == "Yes")
    & (data[astronomyCol].isin(highAstronomyLabels))
]["accuracy"]

lowAstronomyNoMusicGroup = data[
    (data[musicCol] == "No")
    & (data[astronomyCol].isin(lowAstronomyLabels))
]["accuracy"]

musicTest = stats.ttest_ind(musicGroup, noMusicGroup, equal_var=False)
astronomyTest = stats.ttest_ind(highAstronomyGroup, lowAstronomyGroup, equal_var=False)
combinedGroupTest = stats.ttest_ind(
    highAstronomyWithMusicGroup,
    lowAstronomyNoMusicGroup,
    equal_var=False
)

def getMeanPercent(group):
    return group.mean() * 100.0

def getSdPercent(group):
    return group.std(ddof=1) * 100.0

def getSignificanceLabel(pValue):
    if pValue < 0.001:
        return "***"
    if pValue < 0.01:
        return "**"
    if pValue < 0.05:
        return "*"
    return "ns"

def addSignificanceBracket(ax, x1, x2, y, h, label):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], linewidth=1.1, color="black")
    ax.text(
        (x1 + x2) / 2,
        y + h + 0.4,
        label,
        ha="center",
        va="bottom",
        fontsize=10
    )

groupNames = ["Music", "Astronomy", "Combined"]
leftBarLabels = ["Music", "Higher\nknowledge", "Higher astro\n+\nmusic"]
rightBarLabels = ["No music", "Lower\nknowledge", "Lower astro\n+\nno music"]

leftMeans = [
    getMeanPercent(musicGroup),
    getMeanPercent(highAstronomyGroup),
    getMeanPercent(highAstronomyWithMusicGroup),
]

rightMeans = [
    getMeanPercent(noMusicGroup),
    getMeanPercent(lowAstronomyGroup),
    getMeanPercent(lowAstronomyNoMusicGroup),
]

leftSds = [
    getSdPercent(musicGroup),
    getSdPercent(highAstronomyGroup),
    getSdPercent(highAstronomyWithMusicGroup),
]

rightSds = [
    getSdPercent(noMusicGroup),
    getSdPercent(lowAstronomyGroup),
    getSdPercent(lowAstronomyNoMusicGroup),
]

leftNs = [
    len(musicGroup),
    len(highAstronomyGroup),
    len(highAstronomyWithMusicGroup),
]

rightNs = [
    len(noMusicGroup),
    len(lowAstronomyGroup),
    len(lowAstronomyNoMusicGroup),
]

pValues = [
    musicTest.pvalue,
    astronomyTest.pvalue,
    combinedGroupTest.pvalue,
]

significanceLabels = [getSignificanceLabel(pValue) for pValue in pValues]

x = np.arange(len(groupNames))
barWidth = 0.28

fig, ax = plt.subplots(figsize=(7.5, 4.2))

leftBars = ax.bar(
    x - barWidth / 2,
    leftMeans,
    barWidth,
    yerr=leftSds,
    capsize=3,
    label="Group 1"
)

rightBars = ax.bar(
    x + barWidth / 2,
    rightMeans,
    barWidth,
    yerr=rightSds,
    capsize=3,
    label="Group 2"
)

offset = 1.2
height = 1.0

for i in range(len(x)):
    leftX = x[i] - barWidth / 2
    rightX = x[i] + barWidth / 2
    topY = max(leftMeans[i] + leftSds[i], rightMeans[i] + rightSds[i])
    addSignificanceBracket(
        ax,
        leftX,
        rightX,
        topY + offset,
        height,
        significanceLabels[i]
    )

for bar, meanValue, n in zip(leftBars, leftMeans, leftNs):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f"{meanValue:.1f}%\n(n={n})",
        ha="center",
        va="bottom",
        fontsize=10
    )

for bar, meanValue, n in zip(rightBars, rightMeans, rightNs):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f"{meanValue:.1f}%\n(n={n})",
        ha="center",
        va="bottom",
        fontsize=10
    )

ax.set_ylabel("Recognition accuracy (%)", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(groupNames, fontsize=10)

maxBarHeight = max(
    [m + s for m, s in zip(leftMeans, leftSds)] +
    [m + s for m, s in zip(rightMeans, rightSds)]
)

yMax = maxBarHeight + 6
ax.set_ylim(50, yMax)
ax.set_yticks(np.arange(50, 101, 10))
ax.tick_params(axis="y", labelsize=9)

ax.set_title("Recognition accuracy by participant background", fontsize=12, pad=6)

labelY = 60

ax.text(x[0] - barWidth / 2, labelY, leftBarLabels[0], ha="center", va="top", fontsize=7.5)
ax.text(x[0] + barWidth / 2, labelY, rightBarLabels[0], ha="center", va="top", fontsize=7.5)

ax.text(x[1] - barWidth / 2, labelY, leftBarLabels[1], ha="center", va="top", fontsize=7.5)
ax.text(x[1] + barWidth / 2, labelY, rightBarLabels[1], ha="center", va="top", fontsize=7.5)

ax.text(x[2] - barWidth / 2, labelY, leftBarLabels[2], ha="center", va="top", fontsize=7.2)
ax.text(x[2] + barWidth / 2, labelY, rightBarLabels[2], ha="center", va="top", fontsize=7.2)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(direction="in")

plt.subplots_adjust(
    left=0.09,
    right=0.985,
    top=0.90,
    bottom=0.16
)

plt.show()

print("Music comparison:")
print("  nMusic =", len(musicGroup))
print("  nNoMusic =", len(noMusicGroup))
print("  pValue =", musicTest.pvalue)
print("  significance =", significanceLabels[0])
print()

print("Astronomy comparison:")
print("  nHighAstronomy =", len(highAstronomyGroup))
print("  nLowAstronomy =", len(lowAstronomyGroup))
print("  pValue =", astronomyTest.pvalue)
print("  significance =", significanceLabels[1])
print()

print("Combined comparison:")
print("  nHighAstronomyWithMusic =", len(highAstronomyWithMusicGroup))
print("  nLowAstronomyNoMusic =", len(lowAstronomyNoMusicGroup))
print("  pValue =", combinedGroupTest.pvalue)
print("  significance =", significanceLabels[2])