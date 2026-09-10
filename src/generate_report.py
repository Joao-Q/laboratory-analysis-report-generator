"""Combine analyzed results and existing charts into a local HTML report."""

import argparse
from datetime import datetime
from html import escape
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("output")
INPUT_FILE = OUTPUT_DIR / "analyzed_results.csv"
REPORT_FILE = OUTPUT_DIR / "laboratory_report.html"

CHARTS = [
    ("patient_result_distribution.png", "Patient calcium result distribution"),
    ("patient_interpretation_counts.png", "Patient reference-range interpretations"),
    ("patient_results_by_analyzer.png", "Patient results by analyzer"),
    ("control_results_over_time.png", "Control results over time"),
    ("analyzer_workload.png", "Analyzer workload"),
]

INTERPRETATIONS = [
    "Below reference range",
    "Within reference range",
    "Above reference range",
]


def build_report(df):
    """Summarize the CSV without changing its interpretation assignments."""
    patients = df.loc[df["Sample_Type"] == "Patient"]
    control_count = int((df["Sample_Type"] == "Control").sum())
    dates = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="raise")
    if dates.isna().any():
        raise ValueError("Missing dates. Run validation and analysis again.")
    if not df["Sample_Type"].isin(["Patient", "Control"]).all():
        raise ValueError("Unexpected sample types in analyzed results.")
    if not patients["Interpretation"].isin(INTERPRETATIONS).all():
        raise ValueError("Unexpected patient interpretations. Run analysis again.")

    # Reindex keeps all three categories visible, including zero counts.
    counts = patients["Interpretation"].value_counts().reindex(
        INTERPRETATIONS, fill_value=0
    )
    rows = []
    for interpretation, count in counts.items():
        percentage = f"{count / len(patients) * 100:.2f}%" if len(patients) else "N/A"
        rows.append(
            f"<tr><th scope='row'>{escape(interpretation)}</th>"
            f"<td>{count}</td><td>{percentage}</td></tr>"
        )

    figures = []
    for filename, title in CHARTS:
        # Relative paths work when the report and PNGs stay in one folder.
        figures.append(
            f"<figure><img src='{escape(filename)}' alt='{escape(title)}'>"
            f"<figcaption>{escape(title)}</figcaption></figure>"
        )

    period = f"{dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}"
    generated_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Laboratory Analysis Report</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #f1f5f9; color: #172b3a;
           font-family: Arial, sans-serif; line-height: 1.6; }}
    main {{ max-width: 1050px; margin: auto; padding: 32px 20px; }}
    header {{ border-top: 5px solid #147d82; margin-bottom: 28px; }}
    h1 {{ line-height: 1.2; margin-bottom: 12px; }}
    h2 {{ margin-top: 0; }}
    .muted, figcaption {{ color: #496070; }}
    .summary {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .card, section, figure {{ background: white; border: 1px solid #d5e0e7;
                            border-radius: 8px; padding: 20px; }}
    .card strong {{ display: block; font-size: 2rem; color: #12656a; }}
    section {{ margin-top: 24px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    caption {{ text-align: left; margin-bottom: 12px; }}
    th, td {{ padding: 12px 8px; border-bottom: 1px solid #d5e0e7; text-align: right; }}
    th:first-child {{ text-align: left; }}
    tbody th {{ font-weight: normal; }}
    figure {{ margin: 20px 0; break-inside: avoid; }}
    img {{ display: block; width: 100%; height: auto; }}
    figcaption {{ text-align: center; margin-top: 8px; }}
    footer {{ margin-top: 28px; font-size: 0.9rem; }}
    @media (max-width: 600px) {{ .summary {{ grid-template-columns: 1fr; }}
      main {{ padding: 20px 12px; }} section, figure {{ padding: 12px; }} }}
    @media print {{ body {{ background: white; }} main {{ padding: 0; }} }}
  </style>
</head>
<body>
<main>
  <header>
    <p class="muted">SYNTHETIC LABORATORY DATA · CALCIUM</p>
    <h1>Laboratory Analysis Report</h1>
    <p>Data period: {period}<br>Generated: {escape(generated_at)}</p>
    <p class="muted">Source: output/analyzed_results.csv</p>
  </header>
  <div class="summary" aria-label="Result counts">
    <div class="card">Total results<strong>{len(df)}</strong></div>
    <div class="card">Patient results<strong>{len(patients)}</strong></div>
    <div class="card">Control results<strong>{control_count}</strong></div>
  </div>
  <section>
    <h2>Patient interpretations</h2>
    <p>Interpretations are reused from the analyzed CSV. The analysis uses a
    simplified adult calcium reference interval of 8.6–10.0 mg/dL (inclusive).
    Controls are excluded from these counts and percentages.</p>
    <table>
      <caption>Percentages use all {len(patients)} patient results.
      N/A means there are no patient results.</caption>
      <thead><tr><th scope="col">Interpretation</th><th scope="col">Results</th>
      <th scope="col">Percentage</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </section>
  <section>
    <h2>Visualizations</h2>
    <p>Five charts generated from the analyzed results.</p>
    {''.join(figures)}
  </section>
  <footer>Synthetic data and simplified reference intervals for educational
  purposes only. Not intended for clinical use or medical decision-making.</footer>
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Create output/laboratory_report.html from analyzed data and charts."
    )
    parser.parse_args()
    if not INPUT_FILE.is_file():
        parser.error(f"Missing {INPUT_FILE}. Run src/analyze_data.py first.")

    try:
        df = pd.read_csv(INPUT_FILE)
        required = {"Sample_Type", "Date", "Interpretation"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}.")
        if df.empty:
            raise ValueError("No analyzed records available to report.")
        for filename, _ in CHARTS:
            chart = OUTPUT_DIR / filename
            if not chart.is_file():
                raise ValueError(f"Missing {chart}. Run src/visualize_data.py first.")
            if chart.stat().st_mtime_ns < INPUT_FILE.stat().st_mtime_ns:
                raise ValueError(f"Outdated {chart}. Run src/visualize_data.py again.")
        html = build_report(df)
        REPORT_FILE.write_text(html, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Report created: {REPORT_FILE}")
    print("Open it in a browser. Keep the five PNG files in the same folder.")


if __name__ == "__main__":
    main()
