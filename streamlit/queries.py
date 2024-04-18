import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os

def display_top_vintages(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to select the top 10 vintages based on appearances in top lists
        cursor.execute("""
            SELECT vintages.name, 
            COUNT(*) AS total_appearances, 
            SUM(CASE WHEN vintage_toplists_rankings.rank = 1 THEN 1 ELSE 0 END) AS appearances_rank_1,
            SUM(CASE WHEN vintage_toplists_rankings.rank = 2 THEN 1 ELSE 0 END) AS appearances_rank_2,
            SUM(CASE WHEN vintage_toplists_rankings.rank = 3 THEN 1 ELSE 0 END) AS appearances_rank_3
            FROM vintages
            JOIN vintage_toplists_rankings ON vintage_toplists_rankings.vintage_id = vintages.id
            GROUP BY vintages.name
            ORDER BY total_appearances DESC, appearances_rank_1 DESC, appearances_rank_2 DESC, appearances_rank_3 DESC
            LIMIT 10;             
        """)

        # Fetch the results
        results = cursor.fetchall()

        # Reversing the results to display in descending order
        results.reverse()

        # Extracting data for visualization
        vintages = [row[0] for row in results]
        total_appearances = [row[1] for row in results]
        appearances_rank_1 = [row[2] for row in results]
        appearances_rank_2 = [row[3] for row in results]
        appearances_rank_3 = [row[4] for row in results]

        # Plotting bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(y=vintages, x=total_appearances, name='Total Awards', marker_color='blue', orientation='h'))
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_1, name='1st place', marker_color='green', orientation='h'))
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_2, name='2nd place', marker_color='orange', orientation='h'))
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_3, name='3rd place', marker_color='red', orientation='h'))

        fig.update_layout(barmode='group', 
                          title='Top Vintages Based on Toplists Rankings', 
                          yaxis_title='Vintages', 
                          xaxis_title='Number of Awards')
        
        # Reorder the traces to match the order of the legend
        fig.data = fig.data[::-1]

        # Manually specify the order of legend items
        fig.update_layout(legend=dict(traceorder='reversed'))


        # Show the chart
        st.plotly_chart(fig)

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def display_top_wineries(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to select the top 10 wineries with the most appearances in top lists
        cursor.execute("""
           SELECT 
                wineries.name,
                COUNT(*) AS total_appearances,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 1 THEN 1 ELSE 0 END) AS appearances_rank_1,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 2 THEN 1 ELSE 0 END) AS appearances_rank_2,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 3 THEN 1 ELSE 0 END) AS appearances_rank_3
            FROM 
                wineries
            JOIN 
                wines ON wineries.id = wines.winery_id
            JOIN 
                vintages ON wines.id = vintages.wine_id
            JOIN 
                vintage_toplists_rankings ON vintages.id = vintage_toplists_rankings.vintage_id
            JOIN 
                toplists ON vintage_toplists_rankings.top_list_id = toplists.id
            GROUP BY 
                wineries.name
            ORDER BY 
                total_appearances DESC,
                appearances_rank_1 DESC,
                appearances_rank_2 DESC,
                appearances_rank_3 DESC
            LIMIT 
                10;        
        """)

        # Fetch the results
        results = cursor.fetchall()

        # Reversing the results to display in descending order
        results.reverse()

        # Extracting data for visualization
        wineries = [row[0] for row in results]
        total_appearances = [row[1] for row in results]
        appearances_rank_1 = [row[2] for row in results]
        appearances_rank_2 = [row[3] for row in results]
        appearances_rank_3 = [row[4] for row in results]

        # Plotting bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(y=wineries, x=total_appearances, name='Total Awards', marker_color='blue', orientation='h'))
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_1, name='1st place', marker_color='green', orientation='h'))
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_2, name='2nd place', marker_color='orange', orientation='h'))
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_3, name='3rd place', marker_color='red', orientation='h'))

        fig.update_layout(barmode='group', 
                          title='Top Wineries Based on Toplists Rankings', 
                          yaxis_title='Wineries', 
                          xaxis_title='Number of Awards')
        
        # Reorder the traces to match the order of the legend
        fig.data = fig.data[::-1]

        # Manually specify the order of legend items
        fig.update_layout(legend=dict(traceorder='reversed'))

        # Show the chart
        st.plotly_chart(fig)

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def get_top_wineries(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to select the top 3 wineries with the most rank 1 awards
        cursor.execute("""
           SELECT 
                wineries.name,
                COUNT(*) AS total_appearances,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 1 THEN 1 ELSE 0 END) AS appearances_rank_1,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 2 THEN 1 ELSE 0 END) AS appearances_rank_2,
                SUM(CASE WHEN vintage_toplists_rankings.rank = 3 THEN 1 ELSE 0 END) AS appearances_rank_3
            FROM 
                wineries
            JOIN 
                wines ON wineries.id = wines.winery_id
            JOIN 
                vintages ON wines.id = vintages.wine_id
            JOIN 
                vintage_toplists_rankings ON vintages.id = vintage_toplists_rankings.vintage_id
            JOIN 
                toplists ON vintage_toplists_rankings.top_list_id = toplists.id
            GROUP BY 
                wineries.name
            ORDER BY 
                total_appearances DESC,
                appearances_rank_1 DESC,
                appearances_rank_2 DESC,
                appearances_rank_3 DESC
            LIMIT 
                10;        
        """)

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        st.write('#### Wineries Based on Toplists Rankings')
        for idx, row in enumerate(results, start=1):
            st.write(f"{idx}. {row[0]}")

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def get_avg_wine_rating_per_country(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    try:
        # Execute SQL query to retrieve the top wine for each country
        query = """
            SELECT 
                countries.code, 
                countries.name AS country_name,
                AVG(wines.ratings_average) AS avg_rating,
                wines.name AS top_wine_name
            FROM 
                wines
            JOIN 
                regions ON wines.region_id = regions.id
            JOIN 
                countries ON regions.country_code = countries.code
            GROUP BY 
                countries.code
        """
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        data = [{'code': convert_to_alpha3(row[0]), 'country_name': row[1], 'avg_rating': row[2]} for row in rows]

        return data
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def get_avg_vintage_rating_per_country(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    try:
        # Execute SQL query to calculate the average vintage rating for each country
        query = """
            SELECT 
                countries.code, 
                countries.name AS country_name,
                AVG(vintages.ratings_average) AS avg_rating
            FROM 
                vintages
            JOIN 
                wines ON vintages.wine_id = wines.id
            JOIN 
                regions ON wines.region_id = regions.id
            JOIN 
                countries ON regions.country_code = countries.code
            WHERE
                vintages.ratings_average > 0  -- Ignore vintages with zero rating
            GROUP BY 
                countries.code
        """
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        data = [{'code': convert_to_alpha3(row[0]), 'country_name': row[1], 'avg_rating': row[2]} for row in rows]

        return data

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

# Function to convert two-letter country code to ISO 3166-1 alpha-3 format
def convert_to_alpha3(code):
    country_codes = {
        'ar': 'ARG', 'au': 'AUS', 'ch': 'CHE', 'cl': 'CHL', 'de': 'DEU', 'es': 'ESP', 'fr': 'FRA', 'gr': 'GRC',
        'hr': 'HRV', 'hu': 'HUN', 'il': 'ISR', 'it': 'ITA', 'md': 'MDA', 'pt': 'PRT', 'ro': 'ROU', 'us': 'USA',
        'za': 'ZAF'
    }
    return country_codes.get(code, code)  # Return the alpha-3 code if available, otherwise return the original code

def display_wine_country_map(db_file):
   # Call the function to retrieve the data
    data = get_avg_wine_rating_per_country(db_file_path)

    # If data is not None, create a choropleth map using Plotly Express
    if data:
        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create a choropleth map using Plotly Express
        fig = px.choropleth(df, 
                            locations='code', 
                            color='avg_rating',
                            color_continuous_scale="RdYlGn",
                            hover_name="country_name",
                            hover_data={'avg_rating': ':.2f'},
                            projection="natural earth",
                            labels={'avg_rating': 'Avg Rating'})
        
        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>Avg Rating: %{customdata[0]:.2f}')

        # Update layout settings
        fig.update_layout(
            title_text='Country Leaderboard: Wine Reviews',
            geo=dict(
                showland=True,
                showcountries=True,
                showcoastlines=True,
                projection_type='natural earth'
            )
        )

        # Display the choropleth map in Streamlit
        st.plotly_chart(fig)

def display_vintage_country_map (db_file):

    # Call the function to retrieve the data
    data = get_avg_vintage_rating_per_country(db_file)

    # If data is not None, create a choropleth map using Plotly Express
    if data:
        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create a choropleth map using Plotly Express
        fig = px.choropleth(df, 
                            locations='code', 
                            color='avg_rating',
                            color_continuous_scale="RdYlGn",
                            hover_name="country_name",
                            hover_data={'avg_rating': ':.2f'},
                            projection="natural earth",
                            labels={'avg_rating': 'Avg Rating'})
        
        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>Avg Rating: %{customdata[0]:.2f}')

        # Update layout settings
        fig.update_layout(
            title_text='Country Leaderboard: Vintage Reviews',
            geo=dict(
                showland=True,
                showcountries=True,
                showcoastlines=True,
                projection_type='natural earth'
            )
        )

        # Display the choropleth map in Streamlit
        st.plotly_chart(fig)

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

def top_wines(score: float):
    connexion = sqlite3.connect("../db/vivino.db")
    cursor = connexion.cursor()
    cursor.execute("""
        SELECT w.name, ROUND((w.ratings_average + v.ratings_average), 3) AS total_score
        FROM wines AS w
        JOIN vintages AS v ON w.id = v.wine_id
        JOIN wineries AS wi ON w.winery_id = wi.id
        WHERE ROUND((w.ratings_average + v.ratings_average), 3) >= ?
        ORDER BY ROUND((w.ratings_average + v.ratings_average), 3) ASC
    """, (score,))
    result = cursor.fetchall()
    return result

def wines_keynotes(k1, **kwargs):
    connexion = sqlite3.connect("../db/vivino.db")
    cursor = connexion.cursor()
    # Combine k1 and additional keyword arguments
    keywords = [k1, *kwargs.values()]

    # Filter out None values and convert to strings
    keywords = [str(k) for k in keywords if k is not None]

    # Create the SQL IN clause string with the keywords
    in_clause = ",".join(f"'{k}'" for k in keywords)

    # Construct the SQL query dynamically
    query = f"""
    SELECT w.name AS wine_name,
        GROUP_CONCAT(DISTINCT k.name) AS keywords
    FROM wines AS w
    JOIN keywords_wine AS kw ON w.id = kw.wine_id
    JOIN keywords AS k ON kw.keyword_id = k.id
    WHERE k.name IN ({in_clause})
    GROUP BY w.name
    HAVING MIN(kw.count) >= 10;
    """

    # Execute the query
    cursor.execute(query)
    result = cursor.fetchall()

    # Return the result
    return result

def keywords():
    connexion = sqlite3.connect("../db/vivino.db")
    cursor = connexion.cursor()
     
    kl =[]
    query = f"""
        select name
        from keywords

        """

    # Execute the query
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        for r in row:
            kl.append(r)

    return kl

def semstreamlit():
    st.title("Top wines")

    keywords_list = keywords()  # Your list of keywords

    # Selectbox for choosing keywords
    k1 = st.selectbox("Select a keyword for k1", keywords_list, key="k1")
    k2 = st.selectbox("Select a keyword for k2", [None] + keywords_list, key="k2")
    k3 = st.selectbox("Select a keyword for k3", [None] + keywords_list, key="k3")
    k4 = st.selectbox("Select a keyword for k4", [None] + keywords_list, key="k4")
    k5 = st.selectbox("Select a keyword for k5", [None] + keywords_list, key="k5")


    if st.button("Wines with the chosen keywords"):
        wines = wines_keynotes(k1=k1, k2=k2, k3=k3, k4=k4, k5=k5)

        st.table(wines)

def topwines():
    st.title("Top wines")

    score = st.slider("Select a score", min_value=0, max_value=10)

    if st.button("Wines with the chosen score"):
        wines = top_wines(score) 

        st.table(wines)

current_dir = os.path.dirname(__file__)
previous_dir = os.path.dirname(current_dir)
db_path = os.path.join(previous_dir, "db/vivino.db")
con = sqlite3.connect(db_path)
cursor = con.cursor()

# Provide the path to your SQLite database file
db_file_path = "../db/vivino.db"

# Create buttons in the sidebar
st.sidebar.write('# Wiwimo Drunkrat')

st.sidebar.write('### Top Wines')
button6 = st.sidebar.button('Per Grape Type')
button7 = st.sidebar.button('Per Customer Rating')
button8 = st.sidebar.button('Per Taste')

st.sidebar.write('### Top Awards')
button3 = st.sidebar.button('Vintages')
button4 = st.sidebar.button('Wineries')

st.sidebar.write("### Country Leaderboard")
button2 = st.sidebar.button("Vintage Reviews")
button1 = st.sidebar.button("Wine Reviews")

st.sidebar.write('### Population Analysis')
button5 = st.sidebar.button('User Population by Country')

# Display different content based on which button is clicked
if button1:
    display_wine_country_map(db_file_path)
elif button2:
    display_vintage_country_map(db_file_path)
elif button3:
    display_top_vintages(db_file_path)
elif button4:    
    display_top_wineries(db_file_path)
elif button5:
    country_pop_count()
elif button6:
    top_wines_grapes()
elif button7:
    semstreamlit()
elif button8:
    topwines()
else:
    st.write('Welcome')
