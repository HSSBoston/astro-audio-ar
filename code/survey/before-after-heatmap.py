import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(5, 4.5))

# 2x2 paired table:
#                  After positive   After not positive
# Before positive        14                  4
# Before not positive    81                 15

matrix = np.array([[14, 4],
                   [81, 15]])

nPaired = matrix.sum()
pctMatrix = 100 * matrix / nPaired

fig, ax = plt.subplots(figsize=(5.2, 4.5))
im = ax.imshow(pctMatrix, cmap="Blues", vmin=0, vmax=100)
# im = ax.imshow(pctMatrix)

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["After positive", "After not positive"])
ax.set_yticklabels(["Before positive", "Before not positive"])

for i in range(2):
    for j in range(2):
        ax.text(j, i,
                f"{int(matrix[i, j])}\n({pctMatrix[i, j]:.1f}%)",
                ha="center", va="center",
                fontweight="bold", fontsize=11)

# ax.set_title("Before–After Perception Transitions")
ax.set_title("Before–After Perception Transitions (n=114)\nMcNemar test: p < 0.001")
plt.tight_layout()
plt.show()
