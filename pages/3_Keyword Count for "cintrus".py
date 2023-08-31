import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
# The code `connexion = sqlite3.connect("data/vivino.db")` establishes a connection to a SQLite
# database file named "vivino.db".
connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

# The `query1` is a SQL query that retrieves data from multiple tables in a SQLite database. It
# selects the following columns: `vintages.wine_id`, `vintages.name`, `keywords.name`,
# `keywords_wine.count`, and `keywords_wine.group_name`.
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
# object. It retrieves the result set from the database and assigns it to the `keywords` variable.
keywords = cursor.execute(query1)

# The code `pd_keywords = pd.DataFrame(keywords)` is converting the result set obtained from executing
# the SQL query into a pandas DataFrame. This allows us to work with the data in a tabular format and
# perform various operations on it.
pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns =['wine_id', 'vintages_name', 'keyword', 'keyword_count', 'keyword_group']

# The line `citrus = pd_keywords[pd_keywords['keyword'] == 'citrus']` is creating a new DataFrame
# called `citrus` by filtering the `pd_keywords` DataFrame. It selects only the rows where the value
# in the 'keyword' column is equal to 'citrus'. This allows us to isolate the data related to the
# keyword 'citrus' for further analysis or visualization.
citrus = pd_keywords[pd_keywords['keyword'] == 'citrus']


# `citrus_top_10 = citrus.nlargest(10, 'keyword_count')` is creating a new DataFrame called
# `citrus_top_10` by selecting the top 10 rows from the `citrus` DataFrame based on the values in the
# 'keyword_count' column.
citrus_top_10 = citrus.nlargest(10, 'keyword_count')

# The code `plt.figure(figsize=(10, 10))` is setting the size of the figure (plot) that will be
# created using matplotlib. The `figsize` parameter takes a tuple of two values, which represent the
# width and height of the figure in inches. In this case, the figure will have a width of 10 inches
# and a height of 10 inches.
plt.figure(figsize=(10, 10))
# The line `bars = plt.bar(citrus_top_10['vintages_name'].tolist(), citrus_top_10['keyword_count'])`
# is creating a bar plot using matplotlib.
bars = plt.bar(citrus_top_10['vintages_name'].tolist(), citrus_top_10['keyword_count'])
# The code `plt.xlabel('Vintages')` sets the label for the x-axis of the plot as "Vintages". This
# label represents the categories or values on the x-axis.
plt.xlabel('Vintages')
# The code `plt.ylabel('Keyword Count for "citrus"')` is setting the label for the y-axis of the plot
# as "Keyword Count for 'citrus'". This label represents the values on the y-axis, which in this case
# is the count of the keyword "citrus" for each vintage.
plt.ylabel('Keyword Count for "citrus"')
# The code `plt.title('Keyword Count for "citrus" in Top 10 Vintages')` is setting the title of the
# bar plot as "Keyword Count for 'citrus' in Top 10 Vintages". This title provides a brief description
# of what the plot represents, which is the count of the keyword "citrus" for the top 10 vintages.
plt.title('Keyword Count for "citrus" in Top 10 Vintages')
# The code `plt.xticks(rotation=90)` is rotating the x-axis tick labels by 90 degrees. This is done to
# prevent the tick labels from overlapping with each other when there are many categories or values on
# the x-axis. By rotating the tick labels, it makes them more readable and avoids any potential
# overlap.
plt.xticks(rotation=90)
# `plt.tight_layout()` is a function in matplotlib that automatically adjusts the padding between
# subplots or between the plot and the figure edges. It ensures that all elements of the plot are
# visible and properly spaced, preventing any overlap or cropping of labels, titles, or other plot
# elements. This function is useful when creating multiple subplots or when there is limited space
# within the figure.
plt.tight_layout()

# The code `for bar, keyword_count in zip(bars, citrus_top_10['keyword_count']):` is a loop that
# iterates over each bar in the bar plot and the corresponding keyword count value from the
# `citrus_top_10` DataFrame.
for bar, keyword_count in zip(bars, citrus_top_10['keyword_count']):
    plt.text(bar.get_x() + bar.get_width()/2, keyword_count + 5, round(keyword_count, 2), ha='center', va='bottom', color='black', fontsize=16)

# Show the bar plot
st.pyplot(plt)
st.write('68 different vintages have at least 10 keywords "citrus".')