import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Professional style
sns.set_style("whitegrid")

# Create synthetic but realistic engagement data (7 days x 4 channels)
np.random.seed(42)
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
channels = ["Email","App","Web","Support"]
data = np.clip(np.random.normal(loc=70, scale=15, size=(len(days), len(channels))), 20, 100)
df = pd.DataFrame(data, index=days, columns=channels)

# Exact output size: 512x512 pixels at 128 DPI -> 4x4 inches
plt.figure(figsize=(4, 4), dpi=128)

ax = sns.heatmap(
    df,
    annot=True,
    fmt=".0f",
    cmap="viridis",
    cbar_kws={"label": "Engagement score"},
    linewidths=0.5,
    linecolor="white",
    square=True
)

ax.set_title("Weekly Customer Engagement Heatmap", pad=10)
ax.set_xlabel("Channel")
ax.set_ylabel("Day")

# Tight layout to match validation and avoid cropping
plt.tight_layout()

# Save exactly 512x512 with bbox_inches='tight' disabled to keep exact canvas
plt.savefig("chart.png", dpi=128)
plt.close()