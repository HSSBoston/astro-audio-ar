import numpy as np
from scipy import stats

data = np.array([94.5, 95.5, 92.7, 93.6, 92.7, 90.9, 90.0, 92.7, 90.9, 90.9])

tStat, pVal = stats.ttest_1samp(data, 50)

print(tStat, pVal)

