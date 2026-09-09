"""Validate the structure and contents of a laboratory dataset."""

import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(
    description="Validate laboratory data."
)

parser.add_argument(
    "input_file",
    nargs="?",
    default="data/laboratory_results.csv",
    help="CSV file to validate.",
)

args = parser.parse_args()
input_file_path = args.input_file

required_columns = [
    "Sample_ID",
    "Sample_Type",
    "Specimen_Type",
    "Test",
    "Result",
    "Unit",
    "Analyzer",
    "Date",
]

df = pd.read_csv(input_file_path)

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("Input file:", input_file_path)
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("Missing required columns:", missing_columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

numeric_results = pd.to_numeric(df["Result"], errors="coerce")

missing_result_mask = df["Result"].isna()

non_numeric_result_mask = (
    df["Result"].notna()
    & numeric_results.isna()
)

print("\nResult validation:")
print("Missing results:", missing_result_mask.sum())
print("Non-numeric results:", non_numeric_result_mask.sum())

print("\nRows with missing results:")
print(df.loc[missing_result_mask])

print("\nRows with non-numeric results:")
print(df.loc[non_numeric_result_mask])

parsed_dates = pd.to_datetime(
    df["Date"],
    errors="coerce",
    format="%Y-%m-%d",
)

missing_date_mask = df["Date"].isna()

invalid_date_mask = (
    df["Date"].notna()
    & parsed_dates.isna()
)

print("\nDate validation:")
print("Missing dates:", missing_date_mask.sum())
print("Invalid dates:", invalid_date_mask.sum())

print("\nRows with invalid dates:")
print(df.loc[invalid_date_mask])

complete_duplicate_mask = df.duplicated(keep=False)

duplicated_sample_id_mask = df["Sample_ID"].duplicated(
    keep=False
)

print("\nDuplicate validation:")
print(
    "Extra complete duplicate rows:",
    df.duplicated().sum(),
)
print(
    "Rows involved in complete duplicates:",
    complete_duplicate_mask.sum(),
)
print(
    "Repeated Sample ID occurrences:",
    df["Sample_ID"].duplicated().sum(),
)
print(
    "Rows involving duplicated Sample IDs:",
    duplicated_sample_id_mask.sum(),
)

print("\nComplete duplicate records:")
print(
    df.loc[complete_duplicate_mask]
    .sort_values("Sample_ID")
)

print("\nRecords with duplicated Sample IDs:")
print(
    df.loc[duplicated_sample_id_mask]
    .sort_values("Sample_ID")
)

valid_analyzers = {"Analyzer_A", "Analyzer_B"}
valid_units = {"mg/dL"}

invalid_analyzer_mask = ~df["Analyzer"].isin(
    valid_analyzers
)

invalid_unit_mask = ~df["Unit"].isin(
    valid_units
)

print("\nCategorical validation:")
print(
    "Invalid analyzers:",
    invalid_analyzer_mask.sum(),
)
print(
    "Invalid units:",
    invalid_unit_mask.sum(),
)

print("\nRows with invalid analyzers:")
print(df.loc[invalid_analyzer_mask])

print("\nRows with invalid units:")
print(df.loc[invalid_unit_mask])

validation_checks = {
    "missing_result": missing_result_mask,
    "non_numeric_result": non_numeric_result_mask,
    "missing_date": missing_date_mask,
    "invalid_date": invalid_date_mask,
    "complete_duplicate": complete_duplicate_mask,
    "duplicated_sample_id": duplicated_sample_id_mask,
    "invalid_analyzer": invalid_analyzer_mask,
    "invalid_unit": invalid_unit_mask,
}

df["Validation_Issues"] = ""

for issue_name, issue_mask in validation_checks.items():
    df.loc[issue_mask, "Validation_Issues"] += (
        issue_name + "; "
    )

df["Validation_Issues"] = (
    df["Validation_Issues"].str.rstrip("; ")
)

invalid_rows_mask = df["Validation_Issues"] != ""

print("\nValidation summary:")
print("Valid rows:", (~invalid_rows_mask).sum())
print("Invalid rows:", invalid_rows_mask.sum())

print("\nInvalid records and detected issues:")
print(
    df.loc[
        invalid_rows_mask,
        ["Sample_ID", "Validation_Issues"],
    ]
)

valid_df = df.loc[~invalid_rows_mask].copy()
invalid_df = df.loc[invalid_rows_mask].copy()

valid_df["Result"] = numeric_results.loc[
    ~invalid_rows_mask
]

valid_df["Date"] = parsed_dates.loc[
    ~invalid_rows_mask
]

valid_df = valid_df.drop(
    columns=["Validation_Issues"]
)

valid_output_path = "output/validated_results.csv"
error_output_path = "output/validation_errors.csv"

Path(valid_output_path).parent.mkdir(
    parents=True,
    exist_ok=True,
)

valid_df.to_csv(
    valid_output_path,
    index=False,
    date_format="%Y-%m-%d",
)

invalid_df.to_csv(
    error_output_path,
    index=False,
)

print("\nValidation files created:")
print("Valid data:", valid_output_path)
print("Validation errors:", error_output_path)
