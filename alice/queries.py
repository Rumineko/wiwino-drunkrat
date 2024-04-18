import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os

current_dir = os.path.dirname(__file__)
previous_dir = os.path.dirname(current_dir)
db_path = os.path.join(previous_dir, "db/vivino.db")
con = sqlite3.connect(db_path)
cursor = con.cursor()


def country_pop_count():
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

    # Get the index of 'South Africa'
    index_sa = cntr[cntr["name"] == "South Africa"].index[0]

    # Filter the DataFrame to include only countries up until 'South Africa'
    cntr_filtered = cntr.loc[:index_sa]

    # Create the bar chart with the filtered DataFrame
    fig = px.bar(
        cntr_filtered, x="name", y="users_count", color="name", height=500, width=700
    )
    fig.update_layout(
        title="User Count per Country",
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


def top_wines_grapes():
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

    base_url = "https://www.vivino.com/search/wines?q="
    # Create a new column 'search_link' that contains the search URL for each wine
    group["search_link"] = (
        base_url
        + group["winery"].str.replace(" ", "+")
        + "+"
        + group["wine"].str.replace(" ", "+")
    )

    # Create a Plotly table without the 'search_link' column
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        col.capitalize()
                        for col in group.drop(columns="search_link").columns
                    ],
                    fill_color="#49243E",
                    font=dict(size=20),
                ),
                cells=dict(
                    values=[
                        group[col] for col in group.drop(columns="search_link").columns
                    ],
                    fill_color="#704264",
                    font=dict(size=14),
                ),
            )
        ]
    )

    fig.update_layout(
        title=f"Top Five Wines for {selected_grape} Grape Type", height=350, width=700
    )

    st.plotly_chart(fig)

    # Display the search links as a separate list
    st.header("Search Links for the Top Five Wines")
    for i, row in group.iterrows():
        st.markdown(f"[{row['winery']} {row['wine']}]({row['search_link']})")


button1 = st.sidebar.button("User Population by Country")
button2 = st.sidebar.button("Top Five Wines per Grape Type")

if button1:
    country_pop_count()
elif button2:
    top_wines_grapes()
