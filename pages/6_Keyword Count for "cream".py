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

# The code `pd_keywords = pd.DataFrame(keywords)` is converting the result set retrieved from the
# database into a pandas DataFrame. The DataFrame will have the same number of rows as the result set
# and the columns will be automatically generated based on the column names in the result set.
pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns = [
    "wine_id",
    "vintages_name",
    "keyword",
    "keyword_count",
    "keyword_group",
]

# The line `cream = pd_keywords[pd_keywords['keyword'] == 'cream']` is creating a new DataFrame called
# `cream` by filtering the `pd_keywords` DataFrame. It selects only the rows where the value in the
# 'keyword' column is equal to 'cream'.
cream = pd_keywords[pd_keywords["keyword"] == "cream"]

# The line `cream_top_10 = cream.nlargest(10, 'keyword_count')` is creating a new DataFrame called
# `cream_top_10` by selecting the top 10 rows from the `cream` DataFrame based on the values in the
# 'keyword_count' column. The rows are selected in descending order, so the top 10 rows will have the
# highest values in the 'keyword_count' column.
cream_top_10 = cream.nlargest(10, "keyword_count")

# The line `plt.figure(figsize=(10, 10))` is setting the size of the figure (plot) that will be
# created. The `figsize` parameter takes a tuple of two values, which represent the width and height
# of the figure in inches. In this case, the figure will have a width of 10 inches and a height of 10
# inches.
plt.figure(figsize=(10, 10))
# The line `bars = plt.bar(cream_top_10['vintages_name'].tolist(), cream_top_10['keyword_count'])` is
# creating a bar plot using the `plt.bar()` function.
bars = plt.bar(cream_top_10["vintages_name"].tolist(), cream_top_10["keyword_count"])
font = {"family": "serif", "weight": "bold", "size": 22}
plt.rc("font", **font)

# `plt.xlabel('Vintages')` is setting the label for the x-axis of the plot. In this case, it is
# setting the label to "Vintages". This label helps to provide information about the data being
# plotted on the x-axis, which in this case represents different vintages of wines.
plt.xlabel("Vintages")

# The line `plt.ylabel('Keyword Count for "cream"')` is setting the label for the y-axis of the plot.
# In this case, it is setting the label to "Keyword Count for 'cream'". This label helps to provide
# information about the data being plotted on the y-axis, which in this case represents the count of
# the keyword "cream" for each vintage.
plt.ylabel('Keyword Count for "cream"')

# The line `plt.title('Keyword Count for "cream" in Top 10 Vintages')` is setting the title of the
# plot. It adds a title to the plot that describes what the plot is showing, which in this case is the
# keyword count for the keyword "cream" in the top 10 vintages.
plt.title('Keyword Count for "cream" in Top 10 Vintages')

# The line `plt.xticks(rotation=90)` is rotating the x-axis tick labels by 90 degrees. By default, the
# tick labels on the x-axis are displayed horizontally. However, in some cases, when there are many
# tick labels or when the labels are long, they may overlap and become unreadable.
plt.xticks(rotation=90)

# `plt.tight_layout()` is a function in matplotlib that automatically adjusts the padding between
# subplots to prevent overlapping of plot elements. It ensures that all plot elements, such as axis
# labels, tick labels, and titles, are properly displayed without overlapping or being cut off. This
# function is useful when creating multiple subplots or when there are long tick labels or titles that
# may extend beyond the plot area.
plt.tight_layout()

# The code `for bar, keyword_count in zip(bars, cream_top_10['keyword_count']):` is a for loop that
# iterates over each bar and keyword count in the `bars` and `cream_top_10['keyword_count']`
# variables, respectively.
for bar, keyword_count in zip(bars, cream_top_10["keyword_count"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        keyword_count + 5,
        round(keyword_count, 2),
        ha="center",
        va="bottom",
        color="black",
        fontsize=16,
    )

# Show the bar plot
st.pyplot(plt)
st.write("<h3 style='font-size: 20px;'>73 different vintages have at least 10 keywords 'cream'.</h3>", unsafe_allow_html=True)