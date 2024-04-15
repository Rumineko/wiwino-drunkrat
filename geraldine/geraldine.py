import sqlite3

def view_db(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Replace 'your_table_name' with the name of the table you want to view
        cursor.execute("SELECT * FROM regions")

        columns = [description[0] for description in cursor.description]
        print("Columns:", columns)
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Display the fetched data
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def count_names_by_country(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to count names by country code
        cursor.execute("SELECT country_code, COUNT(name) FROM wines GROUP BY country_code")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Display the fetched data
        for row in rows:
            country_code, name_count = row
            print(f"Country Code: {country_code}, Number of Names: {name_count}")
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

def find_unique_region_ids(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Find region IDs in wines table that are not in regions table
        cursor.execute("""
            SELECT DISTINCT wines.region_id
            FROM wines
            LEFT JOIN regions ON wines.region_id = regions.id
            WHERE regions.id IS NULL
        """)
        
        wine_unique_region_ids = cursor.fetchall()

        # Find region IDs in regions table that are not in wines table
        cursor.execute("""
            SELECT DISTINCT regions.id
            FROM regions
            LEFT JOIN wines ON wines.region_id = regions.id
            WHERE wines.region_id IS NULL
        """)
        
        region_unique_region_ids = cursor.fetchall()

        # Display the fetched data
        if wine_unique_region_ids:
            print("Region IDs in wines table not present in regions table:")
            for row in wine_unique_region_ids:
                print(row[0])
        else:
            print("No unique region IDs found in wines table.")

        if region_unique_region_ids:
            print("\nRegion IDs in regions table not present in wines table:")
            for row in region_unique_region_ids:
                print(row[0])
        else:
            print("\nNo unique region IDs found in regions table.")
            
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()


def add_wine_regions_count_column(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to add the wine_regions_count column to countries table
        cursor.execute("""
            ALTER TABLE countries
            ADD COLUMN wine_regions_count INTEGER
        """)

        print("Added wine_regions_count column to countries table successfully.")
        
        # Commit the transaction
        conn.commit()
            
    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes if there's an error
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()


def update_country_wine_regions_count(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to count the number of regions per country code
        cursor.execute("""
            SELECT regions.country_code, COUNT(regions.id) AS wine_regions_count
            FROM regions
            GROUP BY regions.country_code
        """)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Update the countries table with the wine regions count
        for row in rows:
            country_code, wine_regions_count = row
            cursor.execute("""
                UPDATE countries
                SET wine_regions_count = ?
                WHERE code = ?
            """, (wine_regions_count, country_code))
        
        # Commit the transaction
        conn.commit()
        
        print("Updated countries table with wine regions count successfully.")
            
    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes if there's an error
        print("SQLite error:", e)
    finally:
        # Close the connection
        conn.close()

db_file_path = "db/vivino.db"

add_wine_regions_count_column(db_file_path)
update_country_wine_regions_count(db_file_path)


