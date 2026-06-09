```python
import matplotlib.pyplot as plt
import seaborn as sns

def yearly_bar_chart(df):
    fig, ax = plt.subplots()
    yearly = df.groupby("year")["passengers"].sum()
    yearly.plot(kind="bar", ax=ax)
    return fig

def histogram_chart(df):
    fig, ax = plt.subplots()
    sns.histplot(df["passengers"], kde=True, ax=ax)
    return fig

def box_plot(df):
    fig, ax = plt.subplots()
    sns.boxplot(y=df["passengers"], ax=ax)
    return fig
```
