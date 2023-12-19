import pandas as pd

car_to_adjust = "df3_original.csv"  # the car to adjust
car_to_diff   = "stk_original.csv"  # the car to compare against

def compare_csvs(csv1, csv2):
    # Load CSVs
    df1 = pd.read_csv(csv1, header=None, dtype=str)
    df2 = pd.read_csv(csv2, header=None, dtype=str)

    # Get first row of each CSV
    row1 = df1.iloc[0]
    row2 = df2.iloc[0]

    # Only keep columns where both values are strings
    is_string = row1.combine(row2, lambda x, y: isinstance(x, str) and isinstance(y, str))
    row1 = row1[is_string]
    row2 = row2[is_string]

    # Calculate percentage difference for numeric columns
    numeric_columns = row1.str.replace('.', '', regex=False).str.isnumeric() & row2.str.replace('.', '', regex=False).str.isnumeric()
    diff = (row2[numeric_columns].astype(float) - row1[numeric_columns].astype(float)) / row1[numeric_columns].astype(float) * 100

    return diff

# Usage
diffs = compare_csvs(car_to_adjust, car_to_diff)
for diff in diffs:
    print(diff)
    