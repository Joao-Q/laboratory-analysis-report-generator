# Laboratory Analysis Report Generator

A Python project for generating, analyzing, and reporting synthetic laboratory data.

## Project Overview

This project simulates a laboratory data analysis workflow using synthetic data.

The first educational version is complete. It imports synthetic calcium results, validates records, analyzes key metrics, generates five charts, and produces an automatic HTML report.

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
- Automatic HTML report with result counts, date range, patient interpretations, and five charts

## Installation

Tested on Windows with Python 3.12.14 in a fresh virtual environment using the
published repository. Other Python versions and operating systems have not been
verified.

Download the repository using **Code > Download ZIP** on GitHub and extract it,
or clone it with Git. Install Python 3.12, then open PowerShell in the project
folder (the folder containing `README.md` and `requirements.txt`).

Create a virtual environment and install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run all commands from the project root directory. The commands below use the
virtual environment directly, so activation and changes to PowerShell execution
policy are not required.

## Workflow

The normal workflow uses one validation program for any input dataset:

```text
CSV data -> validation -> analysis -> visualizations -> HTML report
```

The repository includes a sample CSV ready for validation. Optionally generate
a new clean synthetic dataset (this replaces the included CSV):

```powershell
.\.venv\Scripts\python.exe src/generate_data.py
```

Validate the clean dataset:

```powershell
.\.venv\Scripts\python.exe src/validate_data.py
```

Analyze the validated records:

```powershell
.\.venv\Scripts\python.exe src/analyze_data.py
```

Create and save the visualizations:

```powershell
.\.venv\Scripts\python.exe src/visualize_data.py
```

Close each chart window to let the visualization program continue.

Create the HTML report:

```powershell
.\.venv\Scripts\python.exe src/generate_report.py
Start-Process output/laboratory_report.html
```

The report reads `output/analyzed_results.csv` and reuses the five PNG charts
created by `visualize_data.py`. It includes total, patient, and control counts,
the data period, and patient interpretation counts and percentages. Existing
interpretations are preserved; controls are excluded from the interpretation table.

Run the steps in order after changing the input data. The report generator
stops with an explanatory message if the CSV is missing or empty, or if a chart
is missing or older than the CSV. This timestamp check catches charts left over
from a previous analysis; it does not verify their contents.

Open `output/laboratory_report.html` in a browser. No web server or new Python
dependencies are needed. Keep the five PNGs alongside the HTML when copying or
sharing the report. Generated files remain excluded from Git. Each successful
report run replaces the previous HTML file.

## Save as PDF

Open the generated HTML report in Chrome, press **Ctrl + P**, and choose
**Save as PDF**. Select A4 paper and disable browser headers and footers.
Check the preview before saving. This is a manual browser export; the Python
workflow generates HTML, not PDF.

## Dirty-data test

Generate a reproducible corrupted copy of the clean dataset:

```powershell
.\.venv\Scripts\python.exe src/generate_dirty_data.py
```

Validate that copy:

```powershell
.\.venv\Scripts\python.exe src/validate_data.py data/laboratory_results_dirty.csv
```

The validator writes usable records to `output/validated_results.csv` and
rejected records, including their detected issues, to
`output/validation_errors.csv`. Each validation run replaces those two files.

After validating either dataset, run `analyze_data.py`, `visualize_data.py`, and `generate_report.py`
to continue the workflow with the latest validated records.

## Disclaimer

This project uses synthetic laboratory data and simplified reference intervals
for educational purposes. It is not intended for clinical use or medical
decision-making.

## Project Status

The first educational version is complete for the synthetic calcium workflow.

A fresh download of commit `b486fcf` was tested on Windows with Python 3.12.14:

- Included CSV: 200 accepted records and no rejected records.
- Newly generated synthetic CSV: 200 accepted records and no rejected records.
- Deliberately corrupted CSV: 192 accepted records and 9 rejected records.
- Analysis, all five charts, and the HTML report were generated in each case.
- The final report opened in Chrome with all five images loading successfully.

The automated check generated charts without opening interactive chart windows.
New synthetic data are random, so patient/control counts and statistics can vary.

The current analysis is specific to calcium, the configured analyzers, mg/dL units,
and simplified reference intervals. Other tests or data formats require code
changes. Future enhancements are optional extensions to this completed scope.
