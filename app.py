from cmath import isnan
from tarfile import PAX_FIELDS
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="Workout Dashboard",
                   page_icon=":running:",
                   layout="wide")
df = pd.read_csv("allWorkouts.csv")

# convert strings to dates
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])

# correct distance to values
def convertToFloat(x):
    try:
        return float(x.replace(",","."))
    except:
        return x

df["Distance"] = df.apply(lambda x: convertToFloat(x["Distance"]), axis=1)

# correct swimming distance
def convertPool(x, y):
    if x == "Pool Swimming":
        y /= 1000
    return y

df["Distance"] =  df.apply(lambda x: convertPool(x["Type"], x["Distance"]), axis=1)
# st.dataframe(df)

st.sidebar.header("Filter:")
workoutTypes = st.sidebar.multiselect(
    "Select workout:",
    options=pd.Series(df["Type"]).unique(),
    default=pd.Series(df["Type"]).unique()
)

df_selection = df.query(
    "Type == @workoutTypes"
)

st.dataframe(df_selection)


totalDistance = round(df_selection["Distance"].sum(), 2)

left_column, middle_column, right_column = st.columns(3)

# creates other category

pie_values = df_selection["Type"].value_counts().values
pie_index = df_selection["Type"].value_counts().index
category_values = pie_values[pie_values > 10]
category_index = pie_index[:len(category_values)]
other_values = pie_values[pie_values <= 10]
if len(other_values) > 0:
    np.append(category_values, np.sum(other_values))
    np.append(category_index.values, "Other")

fig = px.pie(
    df_selection,
    values=category_values,
    names=category_index,
    title='Workout Distribution',
    template="plotly_white"
    )
fig.update_traces(textposition='outside', textinfo='label')
fig.update(layout_showlegend=False)
st.plotly_chart(fig)

df_per_month = df_selection.groupby(pd.Grouper(key="Start",freq='M')).sum()

month_fig = px.bar(
    df_per_month,
    y="Distance",
    x=df_per_month.index
) 
month_fig.update_layout(
    xaxis_title="",
)
st.plotly_chart(month_fig)

with left_column:
    st.subheader("Total Distance:")
    st.subheader(f"{totalDistance:.2f} km")

with middle_column:
    st.subheader("Overview :)")
    

