import sqlite3

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
