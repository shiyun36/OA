import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

### Data retrieval 
pr_directory = 'data/PR'
ghi_directory = 'data/GHI'
pr_data = []
ghi_data = []

# Function to read all CSV files in a directory
def load_data(directory, column_name):
    df_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                df.columns = ['Date', column_name]
                df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


ghi_data = load_data(ghi_directory, 'GHI')
pr_data = load_data(pr_directory, 'PR')
ghi_data['Date'] = pd.to_datetime(ghi_data['Date'])
pr_data['Date'] = pd.to_datetime(pr_data['Date'])

merged_df = pd.merge(ghi_data, pr_data, on='Date', how='inner')
new_df = merged_df.drop_duplicates()
new_df = new_df[['Date', 'GHI', 'PR']]
new_df = new_df.sort_values(by='Date')

new_df.to_csv('new_df.csv', index=False)
print(len(new_df)) 

### Data transformation 





### Data visualisation 