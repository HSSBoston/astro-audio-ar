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

fig, ax = plt.subplots(figsize=(3.5, 3.5))

labels = ["Before", "After"]
values = [beforePositivePct, afterPositivePct]

bars = ax.bar(labels, values)

for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.1f}%",
            ha="center", va="bottom", fontweight="bold")

ax.set_ylabel("Participants perceiving a connection (%)", labelpad=0)
ax.set_ylim(0, 100)
# ax.set_title("Before–After Perception Transitions",
#              fontsize=12)
ax.set_title("Before–After Perception Transitions\nMcNemar test: p < 0.001",
             fontsize=12)
# ax.set_title("Perceived Connection Before vs After")

plt.tick_params(axis='both', direction='in')

plt.tight_layout()
plt.tight_layout(pad=0)
plt.subplots_adjust(left=0.14, right=0.99, top=0.87, bottom=0.05)

plt.show()