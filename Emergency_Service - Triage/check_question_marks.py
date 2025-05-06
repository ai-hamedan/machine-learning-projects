import pandas as pd

# Read the CSV file with proper encoding
df = pd.read_csv('data.csv', sep=';', encoding='latin1')

# Function to check if a column contains "?"
def check_question_marks(column):
    return df[column].astype(str).str.contains('[?]').any()

# Get all columns
columns = df.columns

# Check each column and count occurrences
columns_with_questions = []
for column in columns:
    mask = df[column].astype(str).str.contains('[?]', na=False)
    if mask.any():
        count = mask.sum()
        columns_with_questions.append((column, count))

print("Columns containing '?' values:")
for column, count in columns_with_questions:
    print(f"- {column} ({count} occurrences)")
    
    # Print some example rows containing "?"
    examples = df[df[column].astype(str).str.contains('[?]', na=False)][column].head(3)
    print(f"  Examples: {', '.join(map(str, examples))}\n") 