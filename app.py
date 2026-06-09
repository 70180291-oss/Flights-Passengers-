```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Flight Passenger Dashboard",
    page_icon="✈️",
    layout="wide"
)

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/flights.csv")
    return df

df = load_data()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.title("Filters")

years = sorted(df["year"].unique())
months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

selected_months = st.sidebar.multiselect(
    "Select Month",
    months,
    default=months
)

min_pass = int(df["passengers"].min())
max_pass = int(df["passengers"].max())

passenger_range = st.sidebar.slider(
    "Passenger Range",
    min_pass,
    max_pass,
    (min_pass, max_pass)
)

search_month = st.sidebar.text_input(
    "Search Month"
)

filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["month"].isin(selected_months)) &
    (df["passengers"] >= passenger_range[0]) &
    (df["passengers"] <= passenger_range[1])
]

if search_month:
    filtered_df = filtered_df[
        filtered_df["month"].str.contains(
            search_month,
            case=False
        )
    ]

# ----------------------------
# TITLE
# ----------------------------
st.title("✈️ Airline Passenger Analytics Dashboard")
st.markdown("Analysis of airline passengers from 1949 to 1960")

# ----------------------------
# KPI CARDS
# ----------------------------
total_records = len(filtered_df)
total_passengers = filtered_df["passengers"].sum()
avg_passengers = round(filtered_df["passengers"].mean(), 2)
max_passengers = filtered_df["passengers"].max()
min_passengers = filtered_df["passengers"].min()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Records", total_records)
c2.metric("Total Passengers", f"{total_passengers:,}")
c3.metric("Average", avg_passengers)
c4.metric("Maximum", max_passengers)
c5.metric("Minimum", min_passengers)

st.divider()

# ----------------------------
# LINE CHART
# ----------------------------
st.subheader("Passenger Trend")

line_df = filtered_df.copy()
line_df["date"] = (
    line_df["month"] + " " +
    line_df["year"].astype(str)
)

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(
    range(len(line_df)),
    line_df["passengers"],
    marker="o"
)
ax.set_title("Passenger Trend")
ax.set_ylabel("Passengers")
st.pyplot(fig)

# ----------------------------
# BAR CHART
# ----------------------------
st.subheader("Passengers by Year")

yearly = (
    filtered_df
    .groupby("year")["passengers"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    data=yearly,
    x="year",
    y="passengers",
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# HISTOGRAM
# ----------------------------
st.subheader("Passenger Distribution")

fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(
    filtered_df["passengers"],
    bins=20,
    kde=True,
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# PIE CHART
# ----------------------------
st.subheader("Monthly Share")

pie_df = (
    filtered_df
    .groupby("month")["passengers"]
    .sum()
)

fig, ax = plt.subplots(figsize=(8,8))
ax.pie(
    pie_df,
    labels=pie_df.index,
    autopct="%1.1f%%"
)
st.pyplot(fig)

# ----------------------------
# SCATTER
# ----------------------------
st.subheader("Year vs Passengers")

fig, ax = plt.subplots(figsize=(10,5))
sns.scatterplot(
    data=filtered_df,
    x="year",
    y="passengers",
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# BOXPLOT
# ----------------------------
st.subheader("Passenger Boxplot")

fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(
    data=filtered_df,
    y="passengers",
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# HEATMAP
# ----------------------------
st.subheader("Heatmap")

heat_df = filtered_df.pivot_table(
    values="passengers",
    index="month",
    columns="year"
)

fig, ax = plt.subplots(figsize=(12,8))
sns.heatmap(
    heat_df,
    cmap="YlGnBu",
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# AREA CHART
# ----------------------------
st.subheader("Area Chart")

area_df = (
    filtered_df
    .groupby("year")["passengers"]
    .sum()
)

st.area_chart(area_df)

# ----------------------------
# COUNT PLOT
# ----------------------------
st.subheader("Count Plot")

fig, ax = plt.subplots(figsize=(10,5))
sns.countplot(
    data=filtered_df,
    x="year",
    ax=ax
)
st.pyplot(fig)

# ----------------------------
# VIOLIN PLOT
# ----------------------------
st.subheader("Violin Plot")

fig, ax = plt.subplots(figsize=(12,5))
sns.violinplot(
    data=filtered_df,
    x="month",
    y="passengers",
    ax=ax
)
plt.xticks(rotation=45)
st.pyplot(fig)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df)

# ----------------------------
# DOWNLOAD
# ----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_flights.csv",
    "text/csv"
)
```
