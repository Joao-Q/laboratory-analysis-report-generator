import random
import csv
from datetime import datetime, timedelta

# Available laboratory analyzers and their expected workload distribution
analyzers = ["Analyzer_A", "Analyzer_B"]
analyzer_weights = [60, 40]

# Most laboratory records represent patient samples rather than controls
sample_types = ["Patient", "Control"]
sample_type_weights = [95, 5]

sample_type = random.choices(population= sample_types, weights= sample_type_weights )[0]


analyzer = random.choices(population=analyzers, weights=analyzer_weights)[0]

today = datetime.now()

test_name = "Calcium"
unit = "mg/dL"

records = []
# Generate synthetic laboratory records
for i in range(1,101):
    sample_id = f"S{i:04d}"
    sample_type = random.choices(population= sample_types, weights= sample_type_weights )[0]
    analyzer = random.choices(population=analyzers, weights=analyzer_weights)[0]
    result = round(random.gauss(9.2,0.6),2)
    sample_date = today - timedelta(days=random.randint(0,90))
    final_date = sample_date.strftime("%Y-%m-%d")
    record = {
        "Sample_ID": sample_id,
        "Sample_Type": sample_type,
        "Test": test_name,
        "Result": result,
        "Unit": unit,
        "Analyzer": analyzer,
        "Date": final_date
    }
    records.append(record)
    
print("Records",len(records))


file_path = "data/laboratory_results.csv"
fieldnames = ["Sample_ID", "Sample_Type", "Test", "Result", "Unit", "Analyzer", "Date"]

with open (file=file_path,mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print("CSV written successfully")