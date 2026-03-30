import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from scipy.stats import binomtest

csvPath = "data/responses.csv"

beforeCol = "Before this survey, had you ever felt or perceived any connection between celestial objects and musical expression?"
afterCol  = "Based on your experience listening to several musical pieces translated from constellations, do you feel or perceive a connection between constellations and musical expression? "

beforePositive = {"Yes", "Somewhat yes"}
afterPositive  = {"Strongly agree", "Agree"}

def toBinaryBefore(x):
    if pd.isna(x):
        return None
    x = str(x).strip()
    if x in beforePositive:
        return 1
    return 0

def toBinaryAfter(x):
    if pd.isna(x):
        return None
    x = str(x).strip()
    if x in afterPositive:
        return 1
    return 0

df = pd.read_csv(csvPath)

df["beforeBin"] = df[beforeCol].apply(toBinaryBefore)
df["afterBin"]  = df[afterCol].apply(toBinaryAfter)

paired = df.dropna(subset=["beforeBin", "afterBin"]).copy()
paired["beforeBin"] = paired["beforeBin"].astype(int)
paired["afterBin"] = paired["afterBin"].astype(int)

# 2x2 table:
#                after=1   after=0
# before=1         a         b
# before=0         c         d
a = ((paired["beforeBin"] == 1) & (paired["afterBin"] == 1)).sum()
b = ((paired["beforeBin"] == 1) & (paired["afterBin"] == 0)).sum()
c = ((paired["beforeBin"] == 0) & (paired["afterBin"] == 1)).sum()
d = ((paired["beforeBin"] == 0) & (paired["afterBin"] == 0)).sum()

table = [[a, b],
         [c, d]]

print("Number of paired responses:", len(paired))
print("\n2x2 paired table:")
print("                 After positive   After not positive")
print(f"Before positive      {a:>4}               {b:>4}")
print(f"Before not positive  {c:>4}               {d:>4}")

# Exact McNemar test
resultExact = mcnemar(table, exact=True)
print("\nExact McNemar test (binomial version):")
print(f"Statistic = {resultExact.statistic}")
print(f"p-value   = {resultExact.pvalue:.6g}")

# Approximate McNemar test with continuity correction
resultCc = mcnemar(table, exact=False, correction=True)
print("\nApproximate McNemar test (chi-square with continuity correction):")
print(f"Chi-square = {resultCc.statistic:.6f}")
print(f"p-value    = {resultCc.pvalue:.6g}")

# Equivalent binomial test
nDiscordant = b + c
smaller = min(b, c)
if nDiscordant > 0:
    binomRes = binomtest(smaller, n=nDiscordant, p=0.5, alternative="two-sided")
    print("\nEquivalent exact binomial test on discordant pairs:")
    print(f"Discordant pairs (b+c) = {nDiscordant}")
    print(f"min(b, c)              = {smaller}")
    print(f"p-value                = {binomRes.pvalue:.6g}")

print("\nInterpretation:")
if c > b:
    print(f"More participants changed from not positive to positive ({c}) than from positive to not positive ({b}).")
elif b > c:
    print(f"More participants changed from positive to not positive ({b}) than from not positive to positive ({c}).")
else:
    print(f"The number of changes in each direction is equal ({b} vs {c}).")
