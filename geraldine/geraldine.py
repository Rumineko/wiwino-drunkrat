import sqlite3

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


