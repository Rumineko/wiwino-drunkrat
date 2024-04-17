import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

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
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_1, name='Rank 1', marker_color='green', orientation='h'))
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_2, name='Rank 2', marker_color='orange', orientation='h'))
        fig.add_trace(go.Bar(y=vintages, x=appearances_rank_3, name='Rank 3', marker_color='red', orientation='h'))

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
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_1, name='Rank 1', marker_color='green', orientation='h'))
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_2, name='Rank 2', marker_color='orange', orientation='h'))
        fig.add_trace(go.Bar(y=wineries, x=appearances_rank_3, name='Rank 3', marker_color='red', orientation='h'))

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

# Provide the path to your SQLite database file
db_file_path = "../../db/vivino.db"

# Create buttons in the sidebar
st.sidebar.write('# Wiwimo Drunkat')

st.sidebar.write('### Top Awards')
button3 = st.sidebar.button('Vintages')
button4 = st.sidebar.button('Wineries')

st.sidebar.write("### Country Leaderboard")
button2 = st.sidebar.button("Vintage Reviews")
button1 = st.sidebar.button("Wine Reviews")

# Display different content based on which button is clicked
if button1:
    display_wine_country_map(db_file_path)
elif button2:
    display_vintage_country_map(db_file_path)
elif button3:
    display_top_vintages(db_file_path)
elif button4:    
    display_top_wineries(db_file_path)
else:
    st.write('Welcome')
