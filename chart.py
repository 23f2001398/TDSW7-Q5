# chart.py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reproducibility
rng = np.random.default_rng(42)

# ----------------------------
# Generate synthetic data
# ----------------------------
# Assumptions:
# - Three customer segments with different spend distributions.
# - Right-skewed spending (log-normal) with realistic ranges.
# - Occasional high spend outliers to mimic real behavior.
n_per_segment = 400

segments = ["Budget", "Standard", "Premium"]

# Log-normal parameters chosen to create realistic medians and spreads
# Budget: lower typical spend, narrower spread
budget_spend = rng.lognormal(mean=np.log(20), sigma=0.6, size=n_per_segment)
# Standard: moderate spend
standard_spend = rng.lognormal(mean=np.log(45), sigma=0.55, size=n_per_segment)
# Premium: higher spend, slightly more spread
premium_spend = rng.lognormal(mean=np.log(90), sigma=0.5, size=n_per_segment)

# Inject a few high-value purchases per segment as realistic outliers
def add_outliers(arr, count, factor_range=(3, 6)):
    idx = rng.choice(len(arr), size=count, replace=False)
    factors = rng.uniform(factor_range[0], factor_range, size=count)
    arr[idx] = arr[idx] * factors
    return arr

budget_spend = add_outliers(budget_spend, count=6)
standard_spend = add_outliers(standard_spend, count=8)
premium_spend = add_outliers(premium_spend, count=10)

# Round to 2 decimals to mimic currency formatting
budget_spend = np.round(budget_spend, 2)
standard_spend = np.round(standard_spend, 2)
premium_spend = np.round(premium_spend, 2)

# Create a DataFrame in tidy format
df = pd.DataFrame({
    "segment": np.repeat(segments, n_per_segment),
    "spend": np.concatenate([budget_spend, standard_spend, premium_spend])
})

# Optional: clip extremely high values to reduce visual distortion (keep outliers)
# df["spend"] = df["spend"].clip(0, 1000)

# ----------------------------
# Seaborn best practices
# ----------------------------
# Professional appearance and context
sns.set_style("whitegrid")
sns.set_context("talk")  # presentation-ready text sizes

# Choose a qualitative palette with good contrast
palette = sns.color_palette("Set2", n_colors=len(segments))

# ----------------------------
# Create figure and boxplot
# ----------------------------
# For a 512x512 image: figsize=(8, 8) with dpi=64 -> 8*64 = 512 pixels
plt.figure(figsize=(8, 8))

ax = sns.boxplot(
    data=df,
    x="segment",
    y="spend",
    palette=palette,
    width=0.5,
    fliersize=3,     # control outlier marker size
    linewidth=1.25,  # box/whisker line width
    showmeans=True,  # show mean marker
    meanprops={"marker": "D", "markerfacecolor": "black", "markeredgecolor": "white", "markersize": 5}
)

# Titles and labels
ax.set_title("Customer Spending by Segment", pad=12)
ax.set_xlabel("Customer Segment")
ax.set_ylabel("Spend per Order ($)")

# Improve y-axis ticks (currency formatting)
# Keep simple formatting to avoid locale dependency
y_ticks = ax.get_yticks()
ax.set_yticklabels([f"${int(t):,}" if t >= 1 else f"${t:.2f}" for t in y_ticks])

# Lighten spines for a cleaner look
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

# Tight layout and save
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
# Optional: show() for local testing
# plt.show()
