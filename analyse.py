#%% import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import requests
import json

#%% 
##############################################################################
# settings
##############################################################################
odata_index_url = "https://opendata.cbs.nl/ODataApi/odata/00372eng"

# sns
sns.set(rc={"figure.figsize": (15, 5)})

#%%
##############################################################################
# fetch data
##############################################################################

# read index
odata_index = json.loads(requests.get(odata_index_url).text)

# read data files
data = {}
for data_file in odata_index["value"]:
    data[data_file["name"]] = json.loads(
        requests.get(data_file["url"]).text
    )

# keep only the required information...
summary = data["TableInfos"]
description = pd.DataFrame(data["DataProperties"]["value"])
df = pd.DataFrame(data["TypedDataSet"]["value"])

# ... and delete the rest
del data

##############################################################################
# data wrangling
##############################################################################

# turn into a data dictionary
description = description[description["Key"] != ""]
data_dictionary = description.set_index("Key")
data_dictionary = data_dictionary[
    [
        "Title",
        "Description",
        "Unit",
    ]
].to_dict("index")

##############################################################################
### df (dataframe)

df = df.fillna(0)  # replace null with zeros

# keep only the monthly records
df = df[df["Periods"].str.contains("MM")]

# create year, month, day column, and generate a date column (index)
df["Year"] = df["Periods"].apply(lambda x: int(x[0:4]))
df["Month"] = df["Periods"].apply(lambda x: int(x[6:9]))
df["MonthLabel"] = df["Month"].apply(lambda x: calendar.month_abbr[x])
df["Day"] = 1  # although it should probably be the last day of the month
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])

df["import"] = (  # create totals for import
    df["ImportsOfGaseousNaturalGas_4"] + \
        df["ImportsOfLiquefiedNaturalGasLng_5"]
)

df["export"] = (  # create totals for export
    df["ExportsOfGaseousNaturalGas_6"] + \
        df["ExportsOfLiquefiedNaturalGasLng_7"]
)

# product total
df["production"] = df["IndigenousProduction_2"] + \
    df["ProductionFromOtherSources_3"]

# total consumption (better label)
df["consumption"] = df["TotalConsumption_10"]

# in/out
df["in"] = df["import"] + df["production"]
df["out"] = df["export"] + df["consumption"]

# filter data to be limit to this century
# df = df[df['Year'] >= 1996]

#%% analyse data

# %%
sns.set_theme(style="dark")

##############################################################################
# PLOTS
##############################################################################

# set unit label for gas volumes
gas_volume_units = data_dictionary["IndigenousProduction_2"]["Unit"]

# Natural gas production by year
g = sns.relplot(
    data=df.query("IndigenousProduction_2 >= 0 and Year >= 1996"),
    x="MonthLabel",
    y="IndigenousProduction_2",
    col="Year",
    kind="line",
    linewidth=4,
    zorder=5,
    col_wrap=3,
    height=2,
    aspect=2.2,
    legend=True,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():
    ax.text(0.8, 0.85, year, transform=ax.transAxes, fontweight="bold")
    sns.lineplot(
        data=df,
        x="MonthLabel",
        y="IndigenousProduction_2",
        units="Year",
        estimator=None,
        color=".7",
        linewidth=1,
        ax=ax,
    )

g.set_titles("")
# g.fig.suptitle(data_dictionary["IndigenousProduction_2"]['Title'])
g.set_axis_labels("", gas_volume_units)

plt.show()

# %%
##############################################################################
# production / consumption
production_consumption_df = pd.melt(  # set data
    df, id_vars=["Year"], value_vars=["production", "consumption"]
)

sns.lineplot(  # plot
    x="Year",
    y="value",
    hue="variable",
    style="variable",
    markers=True,
    data=production_consumption_df,
)

# layout
plt.ylim(0, production_consumption_df["value"].max())
plt.ylabel(gas_volume_units)
plt.title("Production vs. Consumption of natural gas")
plt.show()

# %%
##############################################################################
# import vs export by state

import_export_state_df = pd.melt(  # set data
    df,
    id_vars=["Year"],
    value_vars=[
        "ImportsOfGaseousNaturalGas_4",
        "ImportsOfLiquefiedNaturalGasLng_5",
        "ExportsOfGaseousNaturalGas_6",
        "ExportsOfLiquefiedNaturalGasLng_7",
        "Bunkers_8"
    ],
)

# Gas import/export
ie = sns.lineplot(  # plot
    x="Year",
    y="value",
    hue="variable",
    style="variable",
    markers=True,
    data=import_export_state_df,
)

# layout
handles, labels = ie.get_legend_handles_labels()
ie.legend(
    handles,
    [data_dictionary[l]["Title"] for l in labels],
    loc="upper left"
)

plt.ylabel(gas_volume_units)
plt.title("Import vs. Export of natural gas (by state of matter)")
plt.show()

for l in labels:
    print(f"{data_dictionary[l]['Title']}: {data_dictionary[l]['Description']}")

# %%
##############################################################################
# import / export
import_export_df = pd.melt(  # set data
    df, id_vars=["Year"], value_vars=["import", "export"]
)

sns.lineplot(  # plot
    x="Year",
    y="value",
    hue="variable",
    style="variable",
    markers=True,
    data=import_export_df,
)

# layout
plt.ylim(0, import_export_df["value"].max())
plt.ylabel(gas_volume_units)
plt.title("Import vs. Export of natural gas")
plt.show()

# %%
##############################################################################
# in / out
in_out_df = pd.melt( # set data
    df, id_vars=["Year"], value_vars=["in", "out"]
)

sns.lineplot(
    x="Year",
    y="value",
    hue="variable",
    style="variable",
    markers=True,
    data=in_out_df
)

plt.ylim(0, in_out_df["value"].max())
plt.ylabel(gas_volume_units)
plt.title("Production + Import vs. Consumption + Export of natural gas")
plt.show()

# %%

# %%
##############################################################################
# stock

stock_df = pd.melt(  # set data
    df.query("Year >= 2000"),
    id_vars=["Date"],
    value_vars=[
        "StockChange_9"
    ],
)

# Stock in the Netherlands
stock = sns.lineplot(  # plot
    x="Date",
    y="value",
    hue="variable",
    style="variable",
    markers=True,
    data=stock_df,
)

# add line of current value
current_stock = stock_df.iloc[-1]['value']
stock.axhline(current_stock, color="red")

# layout
handles, labels = stock.get_legend_handles_labels()
stock.legend(
    handles,
    [data_dictionary[l]["Title"] for l in labels],
    loc="upper left"
)

plt.ylabel(gas_volume_units)
plt.title("Stock")
plt.show()

for l in labels:
    print(f"{data_dictionary[l]['Title']}: {data_dictionary[l]['Description']}")
# %%
