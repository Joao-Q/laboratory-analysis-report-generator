# Laboratory Analysis Report Generator

A Python project for generating, analyzing, and reporting synthetic laboratory data.

## Project Overview

This project simulates a laboratory data analysis workflow using synthetic data.

The goal is to progressively develop a Python application capable of importing laboratory results, analyzing key metrics, generating visualizations, and producing automated reports.

## Current Features

- Synthetic laboratory data generation
- Patient and control sample generation
- Serum, plasma, and control material specimen types
- Multiple laboratory analyzers with weighted workload distribution
- Distinct synthetic variability for patient and control results
- CSV data export and import using Pandas
- Initial dataset inspection and structural analysis
- Data type inspection and date conversion
- Basic descriptive statistical summary
- Missing value detection
- Duplicate record and Sample ID detection
- Categorical value inspection
- Simplified adult calcium reference-range interpretation
- Validation of patient and control interpretations
- Patient result counts and percentages by interpretation
- Analyzer workload analysis
- Patient result and interpretation comparison by analyzer
- Control mean, standard deviation, and coefficient of variation by analyzer
- Patient specimen distribution and result comparison
- Dataset date-range analysis
- Export of enriched analysis results to CSV
- Patient result distribution histogram with KDE
- Reference-range interpretation count chart
- Patient result comparison by analyzer using box plots
- Control result monitoring over time
- Analyzer workload visualization
- Reproducible generation of deliberately corrupted test data
- Validation of required columns, results, dates, duplicates, analyzers, and units
- Separation of valid records from validation errors

## Installation

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run all commands from the project root directory.

## Workflow

The normal workflow uses one validation program for any input dataset:

```text
CSV data -> validation -> analysis -> visualizations
```

Generate a new clean synthetic dataset:

```powershell
python src/generate_data.py
```

Validate the clean dataset:

```powershell
python src/validate_data.py
```

Analyze the validated records:

```powershell
python src/analyze_data.py
```

Create and save the visualizations:

```powershell
python src/visualize_data.py
```

## Dirty-data test

Generate a reproducible corrupted copy of the clean dataset:

```powershell
python src/generate_dirty_data.py
```

Validate that copy:

```powershell
python src/validate_data.py data/laboratory_results_dirty.csv
```

The validator writes usable records to `output/validated_results.csv` and
rejected records, including their detected issues, to
`output/validation_errors.csv`. Each validation run replaces those two files.

After validating either dataset, run `analyze_data.py` and `visualize_data.py`
to continue the workflow with the latest validated records.

## Disclaimer

This project uses synthetic laboratory data and simplified reference intervals
for educational purposes. It is not intended for clinical use or medical
decision-making.

## Project Status

🚧 Work in progress — new features will be added as the data analysis workflow is developed.
