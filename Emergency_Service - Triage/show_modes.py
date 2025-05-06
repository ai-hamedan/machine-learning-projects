import pandas as pd

# Read the CSV file with proper encoding
df = pd.read_csv('data.csv', sep=';', encoding='latin1')

# Columns with question marks
columns_to_check = ['SBP', 'DBP', 'HR', 'RR', 'BT', 'Saturation']

print("Mode values for columns containing '?':")
for column in columns_to_check:
    # Convert to numeric, replacing '?' with NaN
    numeric_values = pd.to_numeric(df[column].replace('?', pd.NA), errors='coerce')
    mode_value = numeric_values.mode().iloc[0] if not numeric_values.mode().empty else None
    
    print(f"\n{column}:")
    print(f"  Mode: {mode_value}")
    print(f"  Number of '?' values: {df[column].astype(str).str.contains('[?]').sum()}")
    print(f"  Value distribution:")
    print(numeric_values.value_counts().head(5)) 