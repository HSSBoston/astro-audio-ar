import numpy as np
import matplotlib.pyplot as plt

# Data
all_tasks = np.array([94.8, 95.7, 92.2, 92.2, 92.2, 90.5, 90.5, 93.0, 91.4, 90.5])
audio_to_image = np.array([94.8, 95.7, 92.2, 92.2, 92.2, 90.5, 90.5])
image_to_audio = np.array([93.0, 91.4, 90.5])

groups = [all_tasks, audio_to_image, image_to_audio]
labels = ["All\n10 Tasks", "Audio → Image\n7 Tasks", "Image → Audio\n3 Tasks"]

# Compute stats
means = [g.mean() for g in groups]
stds = [g.std(ddof=1) for g in groups]
ns = [len(g) for g in groups]

x = np.arange(len(groups))

# Figure
plt.figure(figsize=(4.5, 3.5))

# Bars with error bars
bars = plt.bar(x, means, yerr=stds, capsize=5)

# Add labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    # Bold stars
    plt.text(bar.get_x() + bar.get_width()/2, height + 5,
             f"{means[i]:.1f}%",
             ha='center', fontsize=10, fontweight="bold")

    # Normal percentage (slightly below)
    plt.text(bar.get_x() + bar.get_width()/2, height + 2.5,
             "p<0.01",
             ha='center', fontsize=10)

# Axis settings
plt.xticks(x, labels)
plt.ylabel("Recognition accuracy (%)", labelpad=0)
plt.title("Recognition accuracy by task type (n=116)", fontsize=12, pad=6)

# Y-axis from 50 to 100
plt.ylim(50, 100)
plt.yticks(np.arange(50, 101, 10))

# Grid and ticks
# plt.grid(axis='y', linestyle=':', linewidth=0.7)
plt.tick_params(axis='both', direction='in')

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout(pad=0)
plt.subplots_adjust(left=0.10, right=0.99, top=0.93, bottom=0.10)

# Show
plt.show()