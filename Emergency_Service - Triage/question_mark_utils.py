import pandas as pd

def check_question_marks(df):
    """
    Check which columns contain question marks and return their counts.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to analyze
        
    Returns:
    --------
    dict
        Dictionary with column names as keys and (count, examples) as values
    """
    results = {}
    
    for column in df.columns:
        mask = df[column].astype(str).str.contains('[?]', na=False)
        if mask.any():
            count = mask.sum()
            examples = df[mask][column].head(3).tolist()
            results[column] = (count, examples)
    
    return results

def print_question_mark_results(results):
    """
    Print the results from check_question_marks in a readable format.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from check_question_marks
    """
    print("Columns containing '?' values:")
    for column, (count, examples) in results.items():
        print(f"- {column} ({count} occurrences)")
        print(f"  Examples: {', '.join(map(str, examples))}\n") 