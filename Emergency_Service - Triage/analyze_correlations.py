import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
df = pd.read_csv('data.csv', sep=';', encoding='latin1')

# Convert categorical variables to numeric for correlation analysis
df['Diagnosis_numeric'] = pd.factorize(df['Diagnosis in ED'])[0]
df['KTAS_expert_numeric'] = pd.factorize(df['KTAS_expert'])[0]
df['mistriage_numeric'] = pd.factorize(df['mistriage'])[0]

# Select columns for correlation analysis
columns_to_analyze = [
    'NRS_pain', 
    'Saturation', 
    'Diagnosis_numeric',
    'KTAS_expert_numeric',
    'mistriage_numeric',
    'SBP', 'DBP', 'HR', 'RR', 'BT'  # Other potential grouping variables
]

# Calculate correlation matrix
correlation_matrix = df[columns_to_analyze].corr()

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Variables')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')

# Print specific correlations of interest
print("\nCorrelations with NRS_pain:")
print(correlation_matrix['NRS_pain'].sort_values(ascending=False))

print("\nCorrelations with Saturation:")
print(correlation_matrix['Saturation'].sort_values(ascending=False))

print("\nCorrelations with Diagnosis_numeric:")
print(correlation_matrix['Diagnosis_numeric'].sort_values(ascending=False))

# Analyze group means
print("\nMean values by KTAS_expert and mistriage groups:")
grouped_means = df.groupby(['KTAS_expert', 'mistriage'])[['NRS_pain', 'Saturation']].mean()
print(grouped_means) 