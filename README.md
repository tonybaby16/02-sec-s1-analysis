# SEC S-1 Filing Analysis

![S-1 Filings Visualization]

A data analysis project that tracks S-1 filing trends with the U.S. Securities and Exchange Commission (SEC) from 1994 to present.

## Features

- **Historical Trends**: Compares current filing activity against 1994-2021 monthly averages
- **Recent Analysis**: 
  - Bar charts for current year (2024-2025) filings
- **Key Metrics**:
  - Monthly filing counts
  - Year-over-year comparisons

## Data Pipeline

    A[SEC EDGAR] -->|submissions.zip| B(Download)
    B --> C(Extract CIK JSONs)
    C --> D(Process Filings)
    D --> E[Monthly Counts CSV]
    D --> F[Company Stats CSV]
    E --> G(Visualize)