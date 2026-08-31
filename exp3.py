import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------
# 1. SAMPLE DATA (14 Data Points / Days)
# ---------------------------------------------------------
data = {
    "Day": [f"Day {i}" for i in range(1, 15)],
    "Deployments": [1, 2, 1, 0, 3, 1, 2, 1, 0, 2, 1, 4, 1, 2],  # Total = 21
    "Lead_Time_Hours": [
        10.5,
        14.0,
        8.2,
        0,
        12.0,
        15.5,
        9.0,
        11.0,
        0,
        13.5,
        7.8,
        16.0,
        10.0,
        12.5,
    ],
    "Failed_Deployments": [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # Total = 2
    "MTTR_Hours": [
        0,
        0,
        1.5,
        0,
        0,
        0,
        0,
        2.0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],  # 2 Incidents (1.5h & 2.0h)
}

df = pd.DataFrame(data)

# ---------------------------------------------------------
# 2. METRIC CALCULATIONS
# ---------------------------------------------------------
total_days = len(df)
total_deployments = df["Deployments"].sum()
total_failures = df["Failed_Deployments"].sum()

# Metric 1: Deployment Frequency (Deployments / Day)
dp_freq = total_deployments / total_days

# Metric 2: Lead Time for Changes (Average hours for active deploy days)
lead_time_avg = df[df["Lead_Time_Hours"] > 0]["Lead_Time_Hours"].mean()

# Metric 3: Change Failure Rate (%)
cfr = (total_failures / total_deployments) * 100

# Metric 4: Mean Time to Restore (Average hours for incidents)
mttr_avg = df[df["MTTR_Hours"] > 0]["MTTR_Hours"].mean()

# ---------------------------------------------------------
# 3. DASHBOARD VISUALIZATION
# ---------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle(
    "EXP 3: DORA Metrics Performance Dashboard", fontsize=16, fontweight="bold"
)

# --- Chart 1: Deployment Frequency ---
axs[0, 0].bar(df["Day"], df["Deployments"], color="#2b5c8f")
axs[0, 0].set_title(
    f"1. Deployment Frequency (Avg: {dp_freq:.2f}/day - HIGH)",
    fontweight="bold",
)
axs[0, 0].set_ylabel("Number of Deployments")
axs[0, 0].tick_params(axis="x", rotation=45)

# --- Chart 2: Lead Time for Changes ---
axs[0, 1].plot(
    df["Day"],
    df["Lead_Time_Hours"],
    marker="o",
    color="#e67e22",
    linewidth=2,
)
axs[0, 1].axhline(
    y=lead_time_avg,
    color="red",
    linestyle="--",
    label=f"Avg: {lead_time_avg:.1f} hrs",
)
axs[0, 1].set_title(
    f"2. Lead Time for Changes (Avg: {lead_time_avg:.1f} hrs - HIGH)",
    fontweight="bold",
)
axs[0, 1].set_ylabel("Hours")
axs[0, 1].tick_params(axis="x", rotation=45)
axs[0, 1].legend()

# --- Chart 3: Change Failure Rate ---
successful_deploys = total_deployments - total_failures
axs[1, 0].pie(
    [successful_deploys, total_failures],
    labels=["Successful", "Failed"],
    autopct="%1.1f%%",
    colors=["#2ecc71", "#e74c3c"],
    explode=(0, 0.1),
    startangle=90,
)
axs[1, 0].set_title(
    f"3. Change Failure Rate (CFR: {cfr:.2f}% - HIGH)", fontweight="bold"
)

# --- Chart 4: Mean Time to Restore (MTTR) ---
incidents_df = df[df["MTTR_Hours"] > 0]
axs[1, 1].bar(
    incidents_df["Day"], incidents_df["MTTR_Hours"], color="#9b59b6", width=0.4
)
axs[1, 1].axhline(
    y=mttr_avg,
    color="black",
    linestyle="--",
    label=f"Avg MTTR: {mttr_avg:.1f} hrs",
)
axs[1, 1].set_title(
    f"4. Time to Restore Service (Avg: {mttr_avg:.1f} hrs - HIGH)",
    fontweight="bold",
)
axs[1, 1].set_ylabel("Recovery Time (Hours)")
axs[1, 1].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("dora_metrics_dashboard.png", dpi=300)
plt.show()