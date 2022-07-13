from tarfile import PAX_FIELDS
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="Workout Dashboard",
                   page_icon=":running:",
                   layout="wide")
df = pd.read_csv("allWorkouts.csv")

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

dfDistance = df_selection["Distance"].dropna()
dfDistance = dfDistance.apply(lambda x: float(x.replace(",",".")))
totalDistance = round(dfDistance.sum(), 2)

left_column, middle_column, right_column = st.columns(3)

# creates other category

pie_values = df["Type"].value_counts().values
pie_index = df["Type"].value_counts().index
category_values = pie_values[pie_values > 10]
category_index = pie_index[:len(category_values)]
other_values = pie_values[pie_values <= 10]

fig = px.pie(
    df_selection,
    values=np.append(category_values, np.sum(other_values)),
    names=np.append(category_index.values, "Other"),
    title='Workout Distribution',
    template="plotly_white"
    )
fig.update_traces(textposition='outside', textinfo='label')
fig.update(layout_showlegend=False)
st.plotly_chart(fig)

with left_column:
    st.subheader("Total Distance:")
    st.subheader(f"{totalDistance:.2f} km")

with middle_column:
    st.subheader("Overview :)")
    

