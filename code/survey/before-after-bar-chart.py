import matplotlib.pyplot as plt
import numpy as np

# 2x2 paired table:
#                  After positive   After not positive
# Before positive        14                  4
# Before not positive    81                 15

nPaired = 114
beforePositiveCount = 18
afterPositiveCount = 95

beforePositivePct = 100 * beforePositiveCount / nPaired
afterPositivePct = 100 * afterPositiveCount / nPaired

fig, ax = plt.subplots(figsize=(4.5, 4.5))

labels = ["Before", "After"]
values = [beforePositivePct, afterPositivePct]

bars = ax.bar(labels, values)

for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.1f}%",
            ha="center", va="bottom", fontweight="bold")

ax.set_ylabel("Participants perceiving a connection (%)")
ax.set_ylim(0, 100)
ax.set_title("Before–After Perception Transitions (n=114)\nMcNemar test: p < 0.001")
# ax.set_title("Perceived Connection Before vs After")
plt.tight_layout()
plt.show()