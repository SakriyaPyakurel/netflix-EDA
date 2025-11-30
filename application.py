# importing necessary libraries
import streamlit as st
import pandas as pd 
import plotly.express as px

# loading the data 
df = pd.read_csv('netflix_titles_cleaned.csv')
df['year_added'] = pd.to_datetime(df['date_added']).dt.year
df = df.dropna(subset=['year_added'])
df['year_added'] = df['year_added'].astype(int)

# setting the title of the dashboard 
st.title("Netflix EDA Dashboard")

# setting the sidebar filters
st.sidebar.header("Filters")


genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=df['listed_in'].unique(),
    default=None
)

year_filter = st.sidebar.slider(
    "year_added",
    int(df.year_added.min()),
    int(df.year_added.max()),
    (2010, 2021)
)

# applying the filters to the dataframe 
filtered_df = df[
    df['year_added'].between(year_filter[0], year_filter[1])
]

type_count = filtered_df['type'].value_counts().reset_index()
type_count.columns = ['type', 'count']

fig_1 = px.pie(
    type_count,
    names='type',
    values='count',
    title="Movies vs TV Shows Distribution"
)

# Showing percentage labels
fig_1.update_traces(textposition='inside', textinfo='percent')

# Showing counts on hover
fig_1.update_traces(
    hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}'
) 

# displaying the pie chart
st.plotly_chart(fig_1, use_container_width=True)







