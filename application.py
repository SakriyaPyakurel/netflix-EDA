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
    (int(df.year_added.min()), int(df.year_added.max()))
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
    title=f"Movies vs TV Shows Distribution for {genre_filter}" if genre_filter else "Movies vs TV Shows Distribution for all genres"
)

# Show percentage labels
fig_1.update_traces(textposition='inside', textinfo='percent')

# Showing counts on hover
fig_1.update_traces(
    hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}'
) 

# displaying the pie chart
st.plotly_chart(fig_1,width='stretch')

# Adding a new column for main genre
df['main_genre'] = df['listed_in'].str.split(',').str[0].str.strip()

# appliying filters for the bar chart

genre_list = ['All Genres'] + sorted(df['main_genre'].unique())
genre_filter = st.selectbox("Select Genre", genre_list)

filtered = df[(df['year_added'] >= year_filter[0]) &
              (df['year_added'] <= year_filter[1])]

if genre_filter != "All Genres":
    filtered = filtered[filtered['main_genre'] == genre_filter]

grouped = filtered.groupby(['year_added', 'type']).size().reset_index(name='count')

all_years = list(range(year_filter[0], year_filter[1] + 1))
fig_2 = px.bar(
    grouped,
    x="year_added",
    y="count",
    color="type",
    barmode="stack",
    title=f"Content Added Over the Years for {genre_filter}",
    category_orders={"year_added": all_years}
)

fig_2.update_layout(
    xaxis=dict(tickmode="array", tickvals=all_years)
)

# displaying the bar chart
st.plotly_chart(fig_2,width='stretch')

fig_3 = px.line(grouped,x="year_added",
    y="count",
    color="type",
    category_orders={"year_added": all_years})

fig_3.update_layout(
    xaxis=dict(tickmode="array", tickvals=all_years)
)

# displaying the linechart
st.plotly_chart(fig_3,width='stretch')




