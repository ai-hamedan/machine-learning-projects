import pandas as pd

# Read the CSV file with proper encoding
df = pd.read_csv('data.csv', sep=';', encoding='latin1')

# Function to check if a column contains "00"
def check_00_column(column):
    return df[column].astype(str).str.contains('00').any()

# Get all columns
columns = df.columns

# Check each column
columns_with_00 = []
for column in columns:
    if check_00_column(column):
        columns_with_00.append(column)

print("Columns containing '00' values:")
for column in columns_with_00:
    print(f"- {column}")
    
    # Print some example values containing "00"
    examples = df[df[column].astype(str).str.contains('00', na=False)][column].head(3)
    print(f"  Examples: {', '.join(map(str, examples))}") 