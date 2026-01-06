import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import MaxNLocator

def generate_chart():
    # Load the data
    data_path = "../docs/assets/data/monthly_counts.csv"
    df = pd.read_csv(data_path, index_col=0)
    
    # Convert column names to strings and filter valid years
    df.columns = df.columns.astype(str)
    years = [col for col in df.columns if col.isdigit()]
    years = sorted(years, key=int)
    
    # Calculate historical average (1994-2024)
    historical_years = [str(y) for y in range(1994, 2025) if str(y) in df.columns]
    df['1994-2024 Avg'] = df[historical_years].mean(axis=1)
    
    # Create figure
    plt.figure(figsize=(14, 7))
    
    # Colors
    avg_color = '#555555'
    bar_colors = ['#1f77b4', '#ff7f0e']  # Blue for 2022, Orange for 2023
    line_colors = ['#2ca02c', '#d62728']   # Green for 2024, Red for 2025
    
    # Plot historical average (thick dashed line)
    plt.plot(df.index, df['1994-2024 Avg'], 
            color=avg_color, 
            linestyle='--', 
            linewidth=2.5,
            alpha=0.8,
            label='1994-2023 Average')
    
    # Plot current years as bars
    bar_width = 0.35
    for i, year in enumerate(['2025', '2026']):
        if year in df.columns:
            offset = bar_width * i
            plt.bar(df.index + offset, df[year], 
                   width=bar_width,
                   color=bar_colors[i],
                   alpha=0.7,
                   label=year)
    
    # Customize chart
    plt.title('SEC S-1 Filings: Historical Average vs Recent Trends', fontsize=14, pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Filings', fontsize=12)
    
    # X-axis settings
    plt.xticks(df.index, 
              ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.xlim(0.5, 12.5)
    
    # Y-axis settings
    max_value = max(df[[ '2025', '2026']].max().max(), df['1994-2024 Avg'].max())
    plt.ylim(0, max_value * 1.15)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Grid and legend
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right', framealpha=1)
    
    # Annotate the historical average line
    for month in df.index:
        plt.annotate(f"{df.loc[month, '1994-2024 Avg']:.1f}", 
                    (month, df.loc[month, '1994-2024 Avg']),
                    textcoords="offset points",
                    xytext=(0,5),
                    ha='center',
                    color=avg_color,
                    fontsize=8)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    os.makedirs("../docs/assets/images", exist_ok=True)
    output_path = "../docs/assets/images/s1_filings_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Chart generated successfully at {output_path}")
    print(f"Historical average calculated from {len(historical_years)} years (1994-2024)")

if __name__ == "__main__":
    generate_chart()
