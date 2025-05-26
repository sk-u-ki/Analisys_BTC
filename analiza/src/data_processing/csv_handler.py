def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def clean_data(df):
    df.dropna(inplace=True)
    return df

def transform_data(df):
    # Example transformation: converting a column to a specific type
    if 'column_name' in df.columns:
        df['column_name'] = df['column_name'].astype(float)
    return df

def load_and_process_csv(file_path):
    df = read_csv(file_path)
    df = clean_data(df)
    df = transform_data(df)
    return df