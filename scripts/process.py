import json
import glob
import pandas as pd
import os
from datetime import datetime

def process_filings():
    filings = []
    processed_files = 0
    skipped_files = 0

    for filepath in glob.glob("../data/CIK*.json"):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Extract company information
                company_info = {
                    'cik': data['cik'],
                    'company_name': data['name'],
                    'industry': data.get('sicDescription', ''),
                    'state': data.get('stateOfIncorporationDescription', '')
                }
                
                # Process filings
                recent_filings = data['filings']['recent']
                num_filings = len(recent_filings['form'])
                
                for i in range(num_filings):
                    if recent_filings['form'][i] == 'S-1':
                        filings.append({
                            **company_info,
                            'form_type': recent_filings['form'][i],
                            'filing_date': recent_filings['filingDate'][i],
                            'accession_number': recent_filings['accessionNumber'][i],
                            'file_number': recent_filings.get('fileNumber', [''])[i],
                            'primary_document': recent_filings.get('primaryDocument', [''])[i]
                        })
                
                processed_files += 1
                
        except Exception as e:
            print(f"Skipping {filepath} due to error: {str(e)}")
            skipped_files += 1
            continue

    if not filings:
        print("Error: No S-1 filings found in any CIK files!")
        return None

    print(f"Processed {processed_files} CIK files ({skipped_files} skipped)")
    print(f"Found {len(filings)} S-1 filings")

    # Create DataFrame
    df = pd.DataFrame(filings)
    
    # Convert and extract date parts
    df['filing_date'] = pd.to_datetime(df['filing_date'], errors='coerce')
    df = df.dropna(subset=['filing_date'])  # Remove rows with invalid dates
    df['year'] = df['filing_date'].dt.year
    df['month'] = df['filing_date'].dt.month
    df['quarter'] = df['filing_date'].dt.quarter

    # Save full dataset
    os.makedirs("../docs/assets/data", exist_ok=True)
    full_data_path = "../docs/assets/data/all_s1_filings.csv"
    df.to_csv(full_data_path, index=False)
    
    # Create and save aggregated data
    monthly_counts = df.groupby(['year', 'month']).size().unstack(level=0, fill_value=0)
    monthly_counts.to_csv("../docs/assets/data/monthly_counts.csv")
    
    # Additional useful aggregations
    company_counts = df['company_name'].value_counts().reset_index()
    company_counts.columns = ['company_name', 's1_filings_count']
    company_counts.to_csv("../docs/assets/data/company_counts.csv", index=False)
    
    industry_counts = df['industry'].value_counts().reset_index()
    industry_counts.columns = ['industry', 's1_filings_count']
    industry_counts.to_csv("../docs/assets/data/industry_counts.csv", index=False)

    print(f"Results saved to docs/assets/data/")
    print(f"- Full data: {len(df)} filings in all_s1_filings.csv")
    print(f"- Monthly counts: monthly_counts.csv")
    print(f"- Company counts: company_counts.csv")
    print(f"- Industry counts: industry_counts.csv")
    
    return df

if __name__ == "__main__":
    process_filings()