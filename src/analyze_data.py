import pandas as pd

"""Import, validate, interpret, and analyze laboratory result data."""

df = pd.read_csv('data/laboratory_results.csv')

print("\n First rows:")
print(df.head())

print("\n Dataset dimensions:")
print(df.shape)

print("\n Column names:")
print(df.columns)

print("\n Data types:")
print(df.dtypes)

print("\n Structural info:")
df.info()

print("\n Statistical summary:")
print(df.describe())

print("\n Data validation:")

print("\n Count null values:")
print(df.isna().sum())

print("\n Count duplicate rows:")
print(df.duplicated().sum())

print("\n Verify if there is duplicate IDs:")
print(df["Sample_ID"].duplicated().sum())

print("\n Show the unique values of Sample type, Specimen Type, Test, Unit and Analyzer:")
print("Sample type:", df["Sample_Type"].unique())
print("Specimen Type:", df["Specimen_Type"].unique())
print("Test:", df["Test"].unique())
print("Unit:", df["Unit"].unique())
print("Analyzer:", df["Analyzer"].unique())

print("\n Data type check:")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print(df["Date"].dtype)

print("\n Count invalid date: ")
print(df["Date"].isna().sum())

# Simplified adult reference interval for synthetic total calcium results
reference_low = 8.6
reference_high = 10.0

# Initialize all results as not clinically applicable
df["Interpretation"] = "Not applicable"

# Identify patient samples eligible for clinical interpretation
patient_mask = df["Sample_Type"] == "Patient"
control_mask = df["Sample_Type"] == "Control"

# Classify patient results according to the reference interval
df.loc[
    patient_mask & (df["Result"] < reference_low),
    "Interpretation"
] = "Below reference range"

df.loc[
    patient_mask & (df["Result"] > reference_high),
    "Interpretation"
] = "Above reference range"

df.loc[
    patient_mask & df["Result"].between(
        reference_low,
        reference_high,
        inclusive="both"
    ),
    "Interpretation"
] = "Within reference range"

# Display and summarize the assigned interpretations
print("\nResult interpretation:")
print(
    df[
        ["Sample_ID", "Sample_Type", "Result", "Unit", "Interpretation"]
    ].head(10)
)

print("\nInterpretation counts:")
print(df["Interpretation"].value_counts())


# Validate interpretation assignments
unclassified_patients = (
    patient_mask
    & (df["Interpretation"] == "Not applicable")
).sum()

clinically_classified_controls = (
    control_mask
    & (df["Interpretation"] != "Not applicable")
).sum()

missing_interpretations = df["Interpretation"].isna().sum()
total_interpretations = df["Interpretation"].notna().sum()

print("\nInterpretation validation:")
print("Unclassified patients:", unclassified_patients)
print("Clinically classified controls:", clinically_classified_controls)
print("Missing interpretations:", missing_interpretations)
print("Total interpretations:", total_interpretations)

# Calculate key performance indicators

# Calculate interpretation KPIs using patient results only
patient_results = df.loc[patient_mask]

interpretation_counts = patient_results["Interpretation"].value_counts()

interpretation_percentages = (
    patient_results["Interpretation"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nPatient result KPIs:")
print("Total patient results:", len(patient_results))

print("\nInterpretation counts:")
print(interpretation_counts)

print("\nInterpretation percentages:")
print(interpretation_percentages)

# Calculate workload distribution by analyzer
analyzer_counts = df["Analyzer"].value_counts()

analyzer_percentages = (
    analyzer_counts / len(df) * 100
).round(2)

print("\nAnalyzer workload:")
print(analyzer_counts)

print("\nAnalyzer workload percentages:")
print(analyzer_percentages)

# Summarize patient results by analyzer
patient_results_by_analyzer = (
    patient_results
    .groupby("Analyzer")["Result"]
    .agg(["count", "mean", "median", "std"])
    .round(2)
)


print("\nPatient results by analyzer:")
print(patient_results_by_analyzer)

# Compare patient interpretation counts by analyzer
interpretation_by_analyzer = pd.crosstab(
    patient_results["Analyzer"],
    patient_results["Interpretation"]
)

print("\nPatient interpretation counts by analyzer:")
print(interpretation_by_analyzer)

interpretation_percentage_by_analyzer = (
    pd.crosstab(
        patient_results["Analyzer"],
        patient_results["Interpretation"],
        normalize="index"
    )
    .mul(100)
    .round(2)
)

print("\nPatient interpretation percentages by analyzer:")
print(interpretation_percentage_by_analyzer)

# Summarize control results by analyzer
control_results = df.loc[control_mask]

control_results_by_analyzer = (
    control_results
    .groupby("Analyzer")["Result"]
    .agg(["count", "mean", "std"])
)

control_results_by_analyzer["cv_percent"] = (
    control_results_by_analyzer["std"]
    / control_results_by_analyzer["mean"]
    * 100
)

print("\nControl results with coefficient of variation:")
print(control_results_by_analyzer.round(2))

# Calculate patient specimen distribution
patient_specimen_counts = (
    patient_results["Specimen_Type"].value_counts()
)

patient_specimen_percentages = (
    patient_specimen_counts
    / len(patient_results)
    * 100
).round(2)

print("\nPatient specimen counts:")
print(patient_specimen_counts)

print("\nPatient specimen percentages:")
print(patient_specimen_percentages)

# Summarize patient results by specimen type
patient_results_by_specimen = (
    patient_results
    .groupby("Specimen_Type")["Result"]
    .agg(["count", "mean", "median", "std"])
)

print("\nPatient results by specimen type:")
print(patient_results_by_specimen.round(2))

# Calculate the dataset date range
earliest_date = df["Date"].min()
latest_date = df["Date"].max()
covered_days = (latest_date - earliest_date).days

print("\nDataset date range:")
print("Earliest date:", earliest_date.date())
print("Latest date:", latest_date.date())
print("Covered days:", covered_days)

# Export the analyzed dataset with derived interpretation
output_file_path = "output/analyzed_results.csv"

df.to_csv(
    output_file_path,
    index=False,
    date_format="%Y-%m-%d"
)

print("\nAnalyzed data exported successfully:")
print(output_file_path)
