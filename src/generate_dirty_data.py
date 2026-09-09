
"""Create a deliberately corrupted dataset for validation testing."""

import pandas as pd


source_file_path = "data/laboratory_results.csv"
dirty_file_path = "data/laboratory_results_dirty.csv"

clean_df = pd.read_csv(source_file_path)
dirty_df = clean_df.copy()

print("Source rows:", len(clean_df))
print("Dirty copy rows:", len(dirty_df))
print("\nFirst rows:")
print(dirty_df.head())

# Introduce a missing result in the first patient record
patient_indexes = dirty_df.index[
    dirty_df["Sample_Type"] == "Patient"
]

missing_result_index = patient_indexes[0]

dirty_df.loc[
    missing_result_index,
    "Result"
] = pd.NA

print("\nRecord with missing result:")
print(dirty_df.loc[missing_result_index])

print("\nMissing results:")
print(dirty_df["Result"].isna().sum())

# Allow the Result column to contain a deliberately invalid text value
dirty_df["Result"] = dirty_df["Result"].astype("object")

non_numeric_result_index = patient_indexes[1]

dirty_df.loc[
    non_numeric_result_index,
    "Result"
] = "not_available"

print("\nRecord with non-numeric result:")
print(dirty_df.loc[non_numeric_result_index])

print("\nInvalid result value:")
print(dirty_df.loc[non_numeric_result_index, "Result"])

invalid_date_index = patient_indexes[2]

# Introduce an invalid date in another patient record
dirty_df.loc[
    invalid_date_index,
    "Date"
] = "2026-99-99"

print("\nRecord with invalid date:")
print(dirty_df.loc[invalid_date_index])

print("\nInvalid date value:")
print(dirty_df.loc[invalid_date_index, "Date"])

duplicate_row_index = patient_indexes[3]
duplicate_row = dirty_df.loc[[duplicate_row_index]]

# Append a complete duplicate of an existing patient record
dirty_df = pd.concat(
    [dirty_df, duplicate_row],
    ignore_index=True
)

print("\nOriginal and duplicated records:")
sample_id_to_duplicate = duplicate_row["Sample_ID"].iloc[0]

print(
    dirty_df.loc[
        dirty_df["Sample_ID"] == sample_id_to_duplicate
    ]
)

print("\nTotal rows after duplication:", len(dirty_df))
print("Complete duplicate rows:", dirty_df.duplicated().sum())

id_source_index = patient_indexes[4]
id_target_index = patient_indexes[5]

# Duplicate a Sample ID without duplicating the remaining record
duplicated_sample_id = dirty_df.loc[
    id_source_index,
    "Sample_ID"
]

dirty_df.loc[
    id_target_index,
    "Sample_ID"
] = duplicated_sample_id

print("\nRecords sharing an ID but containing different data:")
print(
    dirty_df.loc[
        dirty_df["Sample_ID"] == duplicated_sample_id
    ]
)

print(
    "\nDuplicated Sample IDs:",
    dirty_df["Sample_ID"].duplicated().sum()
)

print(
    "Complete duplicate rows:",
    dirty_df.duplicated().sum()
)

invalid_analyzer_index = patient_indexes[6]
dirty_df.loc[
    invalid_analyzer_index,
    "Analyzer"
] = "Analyzer_X"

print("\nRecord with unsupported analyzer:")
print(dirty_df.loc[invalid_analyzer_index])

print("\nAnalyzer values:")
print(dirty_df["Analyzer"].value_counts())

invalid_unit_index = patient_indexes[7]
dirty_df.loc[invalid_unit_index, "Unit"] = "mmol/L"

print("\nRecord with unsupported unit:")
print(dirty_df.loc[invalid_unit_index])

print("\nUnit values:")
print(dirty_df["Unit"].value_counts())

dirty_df.to_csv(dirty_file_path, index=False)

print("\nDirty dataset created successfully.")
print("Output file:", dirty_file_path)
print("Total rows:", len(dirty_df))