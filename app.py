from tarfile import PAX_FIELDS
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Workout Dashboard",
                   page_icon=":running:",
                   layout="wide")
df = pd.read_csv("allWorkouts.csv")

st.dataframe(df)

st.sidebar.header("Filter:")
workoutTypes = st.sidebar.multiselect(
    "Select workout:",
    options=pd.Series(df["Type"]).unique(),
    default=pd.Series(df["Type"]).unique()
)