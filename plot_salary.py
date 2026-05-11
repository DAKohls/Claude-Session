import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("toy_hr_data.csv")

mean_sal = df["salary"].mean()
median_sal = df["salary"].median()

fig, ax = plt.subplots(figsize=(9, 5))

ax.hist(df["salary"], bins=15, color="steelblue", edgecolor="white", alpha=0.85)

ax.axvline(mean_sal, color="red", linewidth=1.8, linestyle="--",
           label=f"Mean: ${mean_sal:,.0f}")
ax.axvline(median_sal, color="blue", linewidth=1.8, linestyle="--",
           label=f"Median: ${median_sal:,.0f}")

ax.text(mean_sal, ax.get_ylim()[1] * 0.95, f"${mean_sal:,.0f}",
        color="red", ha="center", va="top", fontsize=9, fontweight="bold")
ax.text(median_sal, ax.get_ylim()[1] * 0.85, f"${median_sal:,.0f}",
        color="blue", ha="center", va="top", fontsize=9, fontweight="bold")

ax.set_xlabel("Salary ($)", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title("Salary Distribution", fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig("salary_distribution.png", dpi=150)
print(f"Saved salary_distribution.png  |  Mean: ${mean_sal:,.0f}  |  Median: ${median_sal:,.0f}")
