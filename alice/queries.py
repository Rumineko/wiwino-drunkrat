import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import os

current_dir = os.path.dirname(__file__)
previous_dir = os.path.dirname(current_dir)
db_path = os.path.join(previous_dir, "db/vivino.db")

con = sqlite3.connect(db_path)
cursor = con.cursor()


st.header("Vivino User Count Population Analysis")
st.write("This analysis is based on the Vivino user count per country.")

countries = """
    SELECT * FROM country_priority
    """

cntr = pd.read_sql_query(countries, con)

name_mapping = {
    "États-Unis": "United States",
    "France": "France",
    "Italie": "Italy",
    "Allemagne": "Germany",
    "Espagne": "Spain",
    "Argentine": "Argentina",
    "Suisse": "Switzerland",
    "Portugal": "Portugal",
    "Australie": "Australia",
    "Chili": "Chile",
    "Afrique du Sud": "South Africa",
    "Roumanie": "Romania",
    "Israël": "Israel",
    "Grèce": "Greece",
    "Hongrie": "Hungary",
    "Croatie": "Croatia",
    "Moldavie": "Moldova",
}

# Replace the names
cntr["name"] = cntr["name"].replace(name_mapping)

fig = px.bar(cntr, x="name", y="users_count", color="name", height=500, width=700)
fig.update_layout(
    title="User count per country",
    xaxis_title="Country",
    yaxis_title="User count",
    showlegend=False,
)
st.plotly_chart(fig)

# Calculate the total user count for all countries
total_user_count = cntr["users_count"].sum()

# Calculate the user count for 'États-Unis'
us_user_count = cntr[cntr["name"] == "United States"]["users_count"].sum()

# Calculate the percentage of user count for 'États-Unis' compared to total user count
us_percentage = (us_user_count / total_user_count) * 100

st.write(
    f"The percentage of user count for the 'United States' compared to total user count for all countries is {round(us_percentage, 2)}%"
)


grapes = """
    SELECT *
    from top_five_wines_per_grape        
"""

grps = pd.read_sql_query(grapes, con)
grps.set_index("grape", inplace=True)
grouped = grps.groupby("grape", sort=False)

# Get the unique grape types
grape_types = grps.index.unique()

st.header("Top Five Wines Per Grape Type")
st.write(
    "These are the top five wines for each grape type. They are sorted by how popular each grape type is, from most to least popular:"
)

# Create a select box for the grape types
selected_grape = st.selectbox("Select a grape type:", grape_types)

# Display the top wines for the selected grape type
group = grouped.get_group(selected_grape)
group = group.reset_index(drop=True)
group.index += 1
st.write(group)
