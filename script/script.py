import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("sqlite///../data/vivino.db")
cursor = conn.cursor()


# Query to Get Vintage Ratings by Country and Year:
# This query calculates the total number of ratings for each combination of country, year, and vintage.

query1 = """
SELECT
    c.name AS country,
    v.year,
    SUM(v.ratings_count) AS total_ratings
FROM
    vintages v
JOIN
    wines w ON v.wine_id = w.id
JOIN
    regions r ON w.region_id = r.id
JOIN
    countries c ON r.country_code = c.code
GROUP BY
    c.name, v.year;
"""

# Query to Calculate Yearly Growth in Ratings:
# This query calculates the growth rate of ratings from one year to the next for each country.

query2 = """
WITH ratings_by_year AS (
    SELECT
        c.name AS country,
        v.year,
        SUM(v.ratings_count) AS total_ratings
    FROM
        vintages v
    JOIN
        wines w ON v.wine_id = w.id
    JOIN
        regions r ON w.region_id = r.id
    JOIN
        countries c ON r.country_code = c.code
    GROUP BY
        c.name, v.year
)
SELECT
    r1.country,
    r1.year AS current_year,
    r1.total_ratings AS current_ratings,
    r2.year AS previous_year,
    r2.total_ratings AS previous_ratings,
    (r1.total_ratings - r2.total_ratings) AS rating_growth
FROM
    ratings_by_year r1
JOIN
    ratings_by_year r2 ON r1.country = r2.country AND r1.year = r2.year + 1;
"""

# Execute the queries
cursor.execute(query1)
results1 = cursor.fetchall()

cursor.execute(query2)
results2 = cursor.fetchall()

# Close the database connection
conn.close()

# Print or process the results as needed
print("Vintage Ratings by Country and Year:")
for row in results1:
    print(row)

print("\nYearly Growth in Ratings:")
for row in results2:
    print(row)