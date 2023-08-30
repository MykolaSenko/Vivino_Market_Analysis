import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
# The code `connexion = sqlite3.connect("data/vivino.db")` establishes a connection to a SQLite
# database file named "vivino.db" located in the "data" directory.
connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

# The `query1` is a SQL query that retrieves data from multiple tables in a SQLite database.
query1 = """
SELECT
    vintages.wine_id,
    vintages.name,
    keywords.name,
    keywords_wine.count,
    keywords_wine.group_name
FROM
    vintages
    JOIN wines ON vintages.wine_id = wines.id
    JOIN keywords_wine ON wines.id = keywords_wine.wine_id
    JOIN keywords ON keywords_wine.keyword_id = keywords.id
WHERE keywords.name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus') 
    AND keywords_wine.count >= 10
GROUP BY vintages.name
ORDER BY keywords_wine.count DESC
"""

# The line `keywords = cursor.execute(query1)` is executing the SQL query `query1` using the `cursor`
# object. It retrieves the result of the query, which is a set of rows from the database, and assigns
# it to the variable `keywords`.
keywords = cursor.execute(query1)

# The code `pd_keywords = pd.DataFrame(keywords)` is converting the result of the SQL query `keywords`
# into a pandas DataFrame. This allows us to manipulate and analyze the data using pandas functions.
pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns =['wine_id', 'vintages_name', 'keyword', 'keyword_count', 'keyword_group']

# The line `green_apple = pd_keywords[pd_keywords['keyword'] == 'green apple']` is filtering the
# DataFrame `pd_keywords` to only include rows where the value in the 'keyword' column is equal to
# 'green apple'.
green_apple = pd_keywords[pd_keywords['keyword'] == 'green apple']

# The line `green_apple_top_10 = green_apple.nlargest(10, 'keyword_count')` is selecting the top 10
# rows from the DataFrame `green_apple` based on the values in the 'keyword_count' column. It returns
# a new DataFrame `green_apple_top_10` that contains the 10 rows with the highest values in the
# 'keyword_count' column.
green_apple_top_10 = green_apple.nlargest(10, 'keyword_count')

# The code `plt.figure(figsize=(10, 10))` is setting the size of the figure (plot) that will be
# created using matplotlib. The `figsize` parameter takes a tuple of two values, which represent the
# width and height of the figure in inches. In this case, the figure will have a width of 10 inches
# and a height of 10 inches.
plt.figure(figsize=(10, 10))
# The line `bars = plt.bar(green_apple_top_10['vintages_name'].tolist(),
# green_apple_top_10['keyword_count'])` is creating a bar plot using matplotlib.
bars = plt.bar(green_apple_top_10['vintages_name'].tolist(), green_apple_top_10['keyword_count'])

# `plt.xlabel('Vintages')` is setting the label for the x-axis of the plot. In this case, it is
# setting the label to "Vintages". This label helps to provide a clear understanding of what the
# values on the x-axis represent in the plot.
plt.xlabel('Vintages')
# The code `plt.ylabel('Keyword Count for "green apple"')` is setting the label for the y-axis of the
# plot. In this case, it is setting the label to "Keyword Count for 'green apple'". This label helps
# to provide a clear understanding of what the values on the y-axis represent in the plot, which is
# the count of keywords "green apple" for each vintage.
plt.ylabel('Keyword Count for "green apple"')
# The line `plt.title('Keyword Count for "green apple" in Top 10 Vintages')` is setting the title of
# the plot. It adds a title to the bar plot, which helps to provide a clear understanding of what the
# plot represents. In this case, the title is "Keyword Count for 'green apple' in Top 10 Vintages".
plt.title('Keyword Count for "green apple" in Top 10 Vintages')
# `plt.xticks(rotation=90)` is a matplotlib function that rotates the x-axis tick labels by 90
# degrees. By default, the tick labels on the x-axis are displayed horizontally. However, in some
# cases, when there are many tick labels or when the labels are long, they can overlap and become
# unreadable.
plt.xticks(rotation=90)
# `plt.tight_layout()` is a function in matplotlib that automatically adjusts the padding between
# subplots to ensure that all elements of the plot are visible and properly spaced. It helps to
# prevent overlapping of plot elements and ensures that the plot fits within the specified figure
# size.
plt.tight_layout()

# The code `for bar, keyword_count in zip(bars, green_apple_top_10['keyword_count']):` is a for loop
# that iterates over each bar and keyword count in the `bars` and
# `green_apple_top_10['keyword_count']` lists, respectively.
for bar, keyword_count in zip(bars, green_apple_top_10['keyword_count']):
    plt.text(bar.get_x() + bar.get_width()/2, keyword_count + 5, round(keyword_count, 2), ha='center', va='bottom', color='black', fontsize=9)

# Show the bar plot
st.pyplot(plt)
st.write('31 different vintages have at least 10 keywords "green apple".')