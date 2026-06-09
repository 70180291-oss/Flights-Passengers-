```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Flight Passenger Dashboard",
    page_icon="✈️",
    layout="wide"
)

# --------------------
# LOAD DATA
# --------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/flights.csv")

df = load_data()

# --------------------
# SIDEBAR
# --------------------
st.sidebar.header("Filters")

selected_years = st.sidebar.multiselect(
    "Select Years",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

selected_months = st.sidebar.multiselect(
    "Select Months",
    options=df["month"].unique(),
    default=df["month"].unique()
)

min_pass = int(df["passengers"].min())
max_pass = int(df["passengers"].max())

selected_range = st.sidebar.slider(
    "Passenger Range",
    min_pass,
    max_pass,
    (min_pass, max_pass)
)

# --------------------
# FILTER DATA
# --------------------
filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["month"].isin(selected_months)) &
    (df["passengers"] >= selected_range[0]) &
    (df["passengers"] <= selected_range[1])
]

# --------------------
# TITLE
# --------------------
st.title("✈️ Flight Passenger Analytics Dashboard")
st.markdown("Airline Passenger Dataset (1949 - 1960)")

# --------------------
# KPI CARDS
# --------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Records", len(filtered_df))
c2.metric("Total Passengers", int(filtered_df["passengers"].sum()))
c3.metric("Average Passengers", round(filtered_df["passengers"].mean(), 2))
c4.metric("Max Passengers", int(filtered_df["passengers"].max()))

st.divider()

# --------------------
# LINE CHART
# --------------------
st.subheader("Passenger Trend")

line_data = filtered_df.copy()
line_data["index"] = range(len(line_data))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(line_data["index"], line_data["passengers"], marker="o")
ax.set_xlabel("Time")
ax.set_ylabel("Passengers")
ax.set_title("Passenger Trend")
st.pyplot(fig)

# --------------------
# BAR CHART
# --------------------
st.subheader("Passengers by Year")

yearly = filtered_df.groupby("year")["passengers"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(data=yearly, x="year", y="passengers", ax=ax)
st.pyplot(fig)

# --------------------
# HISTOGRAM
# --------------------
st.subheader("Histogram")

fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(filtered_df["passengers"], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# --------------------
# PIE CHART
# --------------------
st.subheader("Passenger Share By Month")

pie_df = filtered_df.groupby("month")["passengers"].sum()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    pie_df,
    labels=pie_df.index,
    autopct="%1.1f%%"
)
st.pyplot(fig)

# --------------------
# SCATTER PLOT
# --------------------
st.subheader("Scatter Plot")

fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(
    data=filtered_df,
    x="year",
    y="passengers",
    ax=ax
)
st.pyplot(fig)

# --------------------
# BOX PLOT
# --------------------
st.subheader("Box Plot")

fig, ax = plt.subplots(figsize=(10, 4))
sns.boxplot(
    y=filtered_df["passengers"],
    ax=ax
)
st.pyplot(fig)

# --------------------
# HEATMAP
# --------------------
st.subheader("Heatmap")

pivot = filtered_df.pivot_table(
    values="passengers",
    index="month",
    columns="year"
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(
    pivot,
    cmap="YlGnBu",
    ax=ax
)
st.pyplot(fig)

# --------------------
# AREA CHART
# --------------------
st.subheader("Area Chart")

area_data = filtered_df.groupby("year")["passengers"].sum()

st.area_chart(area_data)

# --------------------
# COUNT PLOT
# --------------------
st.subheader("Count Plot")

fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(
    data=filtered_df,
    x="year",
    ax=ax
)
st.pyplot(fig)

# --------------------
# VIOLIN PLOT
# --------------------
st.subheader("Violin Plot")

fig, ax = plt.subplots(figsize=(12, 5))
sns.violinplot(
    data=filtered_df,
    x="month",
    y="passengers",
    ax=ax
)

plt.xticks(rotation=45)
st.pyplot(fig)

# --------------------
# DATA TABLE
# --------------------
st.subheader("Dataset")

st.dataframe(filtered_df)

# --------------------
# DOWNLOAD BUTTON
# --------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_flights.csv",
    mime="text/csv"
)
```
