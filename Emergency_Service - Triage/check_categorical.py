import pandas as pd

# Read the data
df = pd.read_csv('data.csv', sep=';', encoding='latin1')

# Function to identify categorical columns
def identify_categorical_columns(df, threshold=10):
    categorical_cols = []
    for column in df.columns:
        # Check if column has few unique values (potential categorical)
        if df[column].nunique() <= threshold:
            print(f"\n{column}:")
            print(f"Number of unique values: {df[column].nunique()}")
            print(f"Unique values: {df[column].unique()}")
            print(f"Data type: {df[column].dtype}")
            categorical_cols.append(column)
    return categorical_cols

# Identify categorical columns
print("Categorical columns in the dataset:")
categorical_columns = identify_categorical_columns(df)
print("\nList of categorical columns:", categorical_columns) 