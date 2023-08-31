import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("sqlite:///../data/vivino.db")
cursor = conn.cursor()

# Query to Get Vintage Ratings by Country and Year:
# This query calculates the total number of ratings for each combination of country, year, and vintage.

query_vintage_ratings = """
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

query_rating_growth = """
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

# Query to Get Average Wine Rating by Country:
query_avg_wine_rating = """
SELECT
    c.name AS country,
    AVG(w.ratings_average) AS avg_wine_rating
FROM
    countries c
JOIN
    regions r ON c.code = r.country_code
JOIN
    wines w ON r.id = w.region_id
GROUP BY
    c.name;
"""

# Query to Get Average Vintage Rating by Country:
query_avg_vintage_rating = """
SELECT
    c.name AS country,
    AVG(v.ratings_average) AS avg_vintage_rating
FROM
    countries c
JOIN
    regions r ON c.code = r.country_code
JOIN
    wines w ON r.id = w.region_id
JOIN
    vintages v ON w.id = v.wine_id
GROUP BY
    c.name;
"""

# Execute the queries
cursor.execute(query_vintage_ratings)
results_vintage_ratings = cursor.fetchall()

cursor.execute(query_rating_growth)
results_rating_growth = cursor.fetchall()

cursor.execute(query_avg_wine_rating)
results_country_avg = cursor.fetchall()

cursor.execute(query_avg_vintage_rating)
results_vintage_avg = cursor.fetchall()

# Close the database connection
conn.close()

# Print or process the results as needed
print("Vintage Ratings by Country and Year:")
for row in results_vintage_ratings:
    print(row)

print("\nYearly Growth in Ratings:")
for row in results_rating_growth:
    print(row)

print("\nAverage Wine Ratings by Country:")
for row in results_country_avg:
    print(row)

print("\nAverage Wine Ratings by Vintage:")
for row in results_vintage_avg:
    print(row)
