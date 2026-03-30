import numpy as np
from scipy import stats

data = np.array([94.8, 95.7, 92.2, 92.2, 92.2, 90.5, 90.5, 93.0, 91.4, 90.5])

# One-sample t-test (comparing one group against a fixed baseline avlue)
tStat, pVal = stats.ttest_1samp(data, 50)

print(tStat, pVal)

