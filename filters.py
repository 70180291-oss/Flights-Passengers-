```python
def apply_filters(
    df,
    years,
    months,
    passenger_range
):
    filtered = df[
        (df["year"].isin(years)) &
        (df["month"].isin(months)) &
        (df["passengers"] >= passenger_range[0]) &
        (df["passengers"] <= passenger_range[1])
    ]
    return filtered
```
