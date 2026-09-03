import random
import csv
from datetime import datetime, timedelta

"""Generate synthetic laboratory results and export them to CSV."""

# Available laboratory analyzers and their expected workload distribution
analyzers = ["Analyzer_A", "Analyzer_B"]
analyzer_weights = [60, 40]

# Most laboratory records represent patient samples rather than controls
sample_types = ["Patient", "Control"]
sample_type_weights = [90, 10]

# Available patient specimen types and their synthetic workload distribution
specimen_types = ["Serum", "Plasma"]
specimen_type_weights = [90, 10]

# Reference date used to generate sample dates within the last 90 days
today = datetime.now()

# Current synthetic test configuration
test_name = "Calcium"
unit = "mg/dL"

# Store all generated laboratory records before exporting them
records = []

# Generate synthetic laboratory records
for i in range(1,201):
    sample_id = f"S{i:04d}"
    sample_type = random.choices(population= sample_types, weights= sample_type_weights )[0]
    # Assign a biological specimen to patients and control material to controls
    if sample_type == "Patient":
        specimen_type = random.choices( population=specimen_types, weights=specimen_type_weights)[0]
    else:
        specimen_type = "Control_Material"
    analyzer = random.choices(population=analyzers, weights=analyzer_weights)[0]
    
    # Generate patient and control results with different variability
    if sample_type == "Control":
        result = round(random.gauss(9.2, 0.15), 2)
    else:
        result = round(random.gauss(9.2, 0.6), 2)
    
    # Assign a random sample date within the previous 90 days
    sample_date = today - timedelta(days=random.randint(0,90))
    final_date = sample_date.strftime("%Y-%m-%d")
    record = {
        "Sample_ID": sample_id,
        "Sample_Type": sample_type,
        "Specimen_Type": specimen_type,
        "Test": test_name,
        "Result": result,
        "Unit": unit,
        "Analyzer": analyzer,
        "Date": final_date
    }
    records.append(record)
    
print("Records",len(records))

# Define the output CSV structure and export the generated records
file_path = "data/laboratory_results.csv"
fieldnames = ["Sample_ID", "Sample_Type", "Specimen_Type", "Test", "Result", "Unit", "Analyzer", "Date"]

with open (file=file_path,mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print("CSV written successfully")
