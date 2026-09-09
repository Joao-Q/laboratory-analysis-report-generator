import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

"""Create visualizations from analyzed laboratory result data."""

df = pd.read_csv("output/analyzed_results.csv", parse_dates=["Date"])

patient_results = df.loc[df["Sample_Type"] == "Patient"]


# Simplified adult reference interval for synthetic total calcium results
reference_low = 8.6
reference_high = 10.0

# Create the patient result distribution chart
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.histplot(
    data=patient_results,
    x="Result",
    bins=15,
    kde=True,
    color="steelblue"
)

plt.axvline(
    reference_low,
    color="orange",
    linestyle="--",
    label="Lower reference limit"
)

plt.axvline(
    reference_high,
    color="red",
    linestyle="--",
    label="Upper reference limit"
)

plt.title("Distribution of Patient Calcium Results")
plt.xlabel("Calcium result (mg/dL)")
plt.ylabel("Number of patient results")
plt.legend()
plt.tight_layout()

plt.savefig(
    "output/patient_result_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Define a meaningful category order
interpretation_order = [
    "Below reference range",
    "Within reference range",
    "Above reference range"
]

interpretation_colors = {
    "Below reference range": "orange",
    "Within reference range": "seagreen",
    "Above reference range": "red"
}

# Create the patient interpretation count chart
plt.figure(figsize=(10, 6))

ax = sns.countplot(
    data=patient_results,
    x="Interpretation",
    order=interpretation_order,
    hue="Interpretation",
    palette=interpretation_colors,
    legend=False
)

plt.title("Patient Results by Reference-Range Interpretation")
plt.xlabel("Interpretation")
plt.ylabel("Number of patient results")

for container in ax.containers:
    ax.bar_label(container)

plt.tight_layout()

plt.savefig(
    "output/patient_interpretation_counts.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Compare patient result distributions across analyzers
plt.figure(figsize=(9, 6))

sns.boxplot(
    data=patient_results,
    x="Analyzer",
    y="Result",
    hue="Analyzer",
    palette="Set2",
    legend=False
)

plt.axhline(
    reference_low,
    color="orange",
    linestyle="--",
    label="Lower reference limit"
)

plt.axhline(
    reference_high,
    color="red",
    linestyle="--",
    label="Upper reference limit"
)

plt.title("Patient Calcium Results by Analyzer")
plt.xlabel("Analyzer")
plt.ylabel("Calcium result (mg/dL)")
plt.legend()
plt.tight_layout()

plt.savefig(
    "output/patient_results_by_analyzer.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Select and order control results chronologically
control_results = (
    df.loc[df["Sample_Type"] == "Control"]
    .sort_values("Date")
)

# Plot control results over time
plt.figure(figsize=(11, 6))

sns.scatterplot(
    data=control_results,
    x="Date",
    y="Result",
    hue="Analyzer",
    style="Analyzer",
    s=90
)
control_target = 9.2

plt.axhline(
    control_target,
    color="black",
    linestyle="--",
    label="Synthetic control target"
)

plt.title("Control Calcium Results Over Time")
plt.xlabel("Date")
plt.ylabel("Calcium result (mg/dL)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    "output/control_results_over_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Create the analyzer workload chart
analyzer_order = ["Analyzer_A", "Analyzer_B"]

plt.figure(figsize=(8, 6))

ax = sns.countplot(
    data=df,
    x="Analyzer",
    order=analyzer_order,
    hue="Analyzer",
    palette={
        "Analyzer_A": "steelblue",
        "Analyzer_B": "darkorange"
    },
    legend=False
)

for container in ax.containers:
    ax.bar_label(container)

plt.title("Laboratory Workload by Analyzer")
plt.xlabel("Analyzer")
plt.ylabel("Number of laboratory results")
plt.tight_layout()

plt.savefig(
    "output/analyzer_workload.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()