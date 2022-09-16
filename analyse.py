#%% import required libraries
import pandas as pd
import matplotlib
import seaborn as sns
import requests
import json

#%% settings
odata_index_url = "https://opendata.cbs.nl/ODataApi/odata/00372eng"

#%% load data

# read index
odata_index = json.loads(requests.get(odata_index_url).text)

# read data files
data = {}
for data_file in odata_index['value']:
    data[data_file['name']] = json.loads(
        requests.get(data_file['url']).text
    )

# keep only the required information...
summary = data['TableInfos']
description = pd.DataFrame(data['DataProperties']['value'])
df = pd.DataFrame(data['TypedDataSet']['value'])

# ... and delete the rest
del data

#%% wrangle data

##############################################################################
### description
# turn into a data dictionary
description = description[description['Key'] != '']
data_dictionary = description.set_index('Key')
data_dictionary = data_dictionary[
    [
        'Title',
        'Description',
        'Unit',
    ]
].to_dict('index')

##############################################################################
### df (dataframe)

#%%
# keep only the monthly records
df = df[df['Periods'].str.contains('MM')]

# create year, month, day column, and generate a date column (index)
df['Year'] = df['Periods'].apply(lambda x: int(x[0:4]))
df['Month'] = df['Periods'].apply(lambda x: int(x[6:9]))
df['Day'] = 1 # although it should probably be the last day of the month
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df = df.set_index('Date')
#%% analyse data

# %%
sns.set_theme(style="dark")

for col in [
        'TotalSupply_1',
        'IndigenousProduction_2',
        'ProductionFromOtherSources_3',
        'Bunkers_8'
    ]:

    # Plot each year's time series in its own facet
    g = sns.relplot(
        data=df[df[col] >= 0],
        x="Month", y=col, col="Year", hue="Year",
        kind="line", palette="crest", linewidth=4, zorder=5,
        col_wrap=3, height=2, aspect=1.5, legend=False,
    )

    # Iterate over each subplot to customize further
    for year, ax in g.axes_dict.items():

        # Add the title as an annotation within the plot
        ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

        # Plot every year's time series in the background
        sns.lineplot(
            data=df, x="Month", y=col, units="Year",
            estimator=None, color=".7", linewidth=1, ax=ax,
        )

    # Reduce the frequency of the x axis ticks
    ax.set_xticks(ax.get_xticks()[::2])

    # Tweak the supporting aspects of the plot
    g.set_titles("")
    g.set_axis_labels("", data_dictionary[col]['Title'])
    g.tight_layout()
# %%
df.columns
# %%
