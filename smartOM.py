import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
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
#calculate 30 day moving average of PR
new_df['PR_MA30'] = new_df['PR'].rolling(window=30).mean()

#calculate budget line dynamically, reduce by 0.8% per year 
start_date = new_df['Date'].min()
new_df['Year'] = (new_df['Date'] - start_date).dt.days // 365
new_df['Budget_PR'] = 73.9 - 0.8 * new_df['Year']

# Define color coding based on GHI
def get_color(ghi):
    if ghi < 2:
        return 'navy'
    elif 2 <= ghi < 4:
        return 'lightblue'
    elif 4 <= ghi < 6:
        return 'orange'
    else:
        return 'brown'

new_df['Color'] = new_df['GHI'].apply(get_color)

### Data visualisation 
fig, ax = plt.subplots(figsize=(15, 10))

# Scatter plot for PR with color coding based on GHI
scatter = ax.scatter(new_df['Date'], new_df['PR'], c=new_df['Color'], label=new_df['GHI'], marker='D', s=20)

# Plot the 30-day moving average of PR
ax.plot(new_df['Date'], new_df['PR_MA30'], color='red', label='30-d moving average of PR')

# Plot the budget line
ax.plot(new_df['Date'], new_df['Budget_PR'], color='darkgreen', label='Target Budget Yield Performance Ratio [1Y-73.9%, 2Y-73.3%, 3Y-72.7%]')


# Customize legend
legend_labels = {
    'navy': '< 2',
    'lightblue': '2 - 4',
    'orange': '4 - 6',
    'brown': '> 6'
}

scatter_legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_labels.keys()]
scatter_legend_labels = legend_labels.values()

line_legend_handles = [
    plt.Line2D([0], [0], color='darkgreen', lw=2, label='Target Budget Yield Performance Ratio'),
    plt.Line2D([0], [0], color='red', lw=2, label='30-d moving average of PR')
]

scatter_legend = ax.legend(scatter_legend_handles, scatter_legend_labels, title='Daily Irradiation [kWh/m2]', loc='upper left', bbox_to_anchor=(0.1, 1), ncol=5, frameon=False)
ax.add_artist(scatter_legend)  
line_legend = ax.legend(line_legend_handles, ['Target Budget Yield Performance Ratio', '30-d moving average of PR'], loc='center', frameon=False)
line_legend.get_texts()[0].set_fontsize(8)
line_legend.get_texts()[0].set_color('green')
line_legend.get_texts()[0].set_weight('bold')
line_legend.get_texts()[1].set_fontsize(8)
line_legend.get_texts()[1].set_color('red')
line_legend.get_texts()[1].set_weight('bold')
ax.add_artist(line_legend)  



# Adding annotations for averages
def add_avg_annotation(data, days, text_y):
    avg_value = data['PR'].rolling(window=days).mean().iloc[-1]
    ax.annotate(f'Average PR last {days}-d: {avg_value:.1f}%', xy=(0.8, text_y), xycoords='axes fraction', fontsize=8,
                ha='left', va='bottom')
    

add_avg_annotation(new_df, 7, 0.25)
add_avg_annotation(new_df, 30, 0.22)
add_avg_annotation(new_df, 60, 0.19)
add_avg_annotation(new_df, 90, 0.16)
add_avg_annotation(new_df, 365, 0.13)
avg_lifetime = new_df['PR'].mean()
ax.annotate(f'Average PR Lifetime: {avg_lifetime:.1f}%', xy=(0.8, 0.10), xycoords='axes fraction', fontsize=8,
            ha='left', va='bottom', weight='bold')

# Highlight points above budget PR
above_budget = new_df[new_df['PR'] > new_df['Budget_PR']]
points_above = len(above_budget)
total_points = len(new_df)
percentage_above = (points_above / total_points) * 100
ax.annotate(f'Points above Target Budget PR = {points_above}/{total_points} = {percentage_above:.1f}%', xy=(0.54, 0.46),
            xycoords='axes fraction', fontsize=8, ha='center', weight='bold')


# Formatting the y and x-axis 
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y')) 
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
fig.autofmt_xdate()
ax.tick_params(axis='x', labelsize=8)  # Adjust the font size
plt.setp(ax.get_xticklabels(), rotation=0)  

# Setting labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Performance Ratio [%]', labelpad=20)
ax.set_title('Performance Ratio Evolution\nFrom 2019-07-01 to 2022-03-24', weight='bold')
ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
plt.ylim(0,100)


# Show plot
plt.tight_layout()
plt.show()