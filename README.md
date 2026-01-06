# SEC S-1 Filing Analysis
See the chart at https://tonybaby16.github.io/02-sec-s1-analysis/

![S-1 Filings Visualization]

A data analysis project that tracks S-1 filing trends with the U.S. Securities and Exchange Commission (SEC) from 1994 to present. Data updates daily at 8 am ET.

## Features

- **Historical Trends**: Compares current filing activity against 1994-previous_year's monthly averages
- **Recent Analysis**: 
  - Bar charts for current and previous year filings
- **Key Metrics**:
  - Monthly filing counts
  - Year-over-year comparisons

## Data Pipeline

    A[SEC EDGAR] -->|submissions.zip| B(Download)
    B --> C(Extract CIK JSONs)
    C --> D(Process Filings)
    D --> E[Monthly Counts CSV]
    E --> F(Visualize)
