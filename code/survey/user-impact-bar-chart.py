import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

labels = [
    "Enjoyment",
    "Motivation\nto learn more",
    "Audio+visual\nlearning",
    "Parent-child\nlearning"
]
values = [91.3, 76.5, 84.9, 82.3]

x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(6.4, 3.2))

bars = ax.bar(
    x, values, width=0.62,
    edgecolor='black', linewidth=1.0
)

# Tight y-range to emphasize differences while keeping honesty
ax.set_ylim(50, 100)

# Axes labels / title
ax.set_ylabel("Positive response rate (%)", fontsize=11, labelpad=0)

# X ticks
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)

# Y ticks
ax.set_yticks(np.arange(50, 101, 10))
ax.yaxis.set_minor_locator(MultipleLocator(1))

# Tick style to match your existing figures
ax.tick_params(axis='both', which='major', direction='in', length=5, width=1.0)
ax.tick_params(axis='both', which='minor', direction='in', length=3, width=0.8)

# Light horizontal grid
ax.grid(axis='y', which='major', linestyle='--', linewidth=0.6, alpha=0.5)
ax.set_axisbelow(True)

# Group labels (optional but useful)
ax.text(0.5, 99.2, "Engagement", ha='center', va='top', fontsize=12)
ax.text(2.5, 99.2, "Educational value", ha='center', va='top', fontsize=12)

# Small divider between the two conceptual groups
ax.axvline(1.5, color='black', linewidth=0.8)

# Bold value labels above bars
for xi, yi in zip(x, values):
    ax.text(
        xi, yi + 0.8, f"{yi:.1f}%",
        ha='center', va='bottom',
        fontsize=10, fontweight='bold'
    )

ax.set_title("User Impact", fontsize=12)

# Spine widths
for spine in ax.spines.values():
    spine.set_linewidth(1.0)


plt.tight_layout()
plt.tight_layout(pad=0)
plt.subplots_adjust(left=0.08, right=0.99, top=0.92, bottom=0.12)

plt.show()