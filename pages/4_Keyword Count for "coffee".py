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
# database into a Pandas DataFrame. The DataFrame will have the same number of rows as the result set
# and the columns will be automatically generated based on the column names in the result set.
pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns =['wine_id', 'vintages_name', 'keyword', 'keyword_count', 'keyword_group']

# The line `coffee = pd_keywords[pd_keywords['keyword'] == 'coffee']` is creating a new DataFrame
# called `coffee` by filtering the `pd_keywords` DataFrame. It selects only the rows where the value
# in the 'keyword' column is equal to 'coffee'.
coffee = pd_keywords[pd_keywords['keyword'] == 'coffee']

# The line `coffee_top_10 = coffee.nlargest(10, 'keyword_count')` is creating a new DataFrame called
# `coffee_top_10` by selecting the top 10 rows from the `coffee` DataFrame based on the values in the
# 'keyword_count' column. The `nlargest()` function is used to retrieve the rows with the largest
# values in the specified column. In this case, it selects the 10 rows with the highest values in the
# 'keyword_count' column.
coffee_top_10 = coffee.nlargest(10, 'keyword_count')

# The line `plt.figure(figsize=(10, 10))` is setting the figure size of the plot to be 10 inches by 10
# inches. This allows you to control the dimensions of the plot and adjust it to your desired size. In
# this case, it is creating a square plot with equal width and height.
plt.figure(figsize=(10, 10))
# The line `bars = plt.bar(coffee_top_10['vintages_name'].tolist(), coffee_top_10['keyword_count'])`
# is creating a bar plot using the `plt.bar()` function.
bars = plt.bar(coffee_top_10['vintages_name'].tolist(), coffee_top_10['keyword_count'])
# `plt.xlabel('Vintages')` is setting the label for the x-axis of the plot. In this case, it is
# setting the label to "Vintages". This label helps to provide a clear description of what the values
# on the x-axis represent.
plt.xlabel('Vintages')
# The line `plt.ylabel('Keyword Count for "coffee"')` is setting the label for the y-axis of the plot.
# In this case, it is setting the label to "Keyword Count for 'coffee'". This label helps to provide a
# clear description of what the values on the y-axis represent, which is the count of the keyword
# "coffee" for each vintage.
plt.ylabel('Keyword Count for "coffee"')
# The line `plt.title('Keyword Count for "coffee" in Top 10 Vintages')` is setting the title of the
# plot. It assigns the string "Keyword Count for "coffee" in Top 10 Vintages" as the title for the
# plot. This title provides a brief description of what the plot represents, which is the count of the
# keyword "coffee" in the top 10 vintages.
plt.title('Keyword Count for "coffee" in Top 10 Vintages')
# The line `plt.xticks(rotation=90)` is rotating the x-axis tick labels by 90 degrees. By default, the
# tick labels on the x-axis are displayed horizontally. However, in some cases, when there are long
# tick labels or a large number of tick labels, they may overlap and become unreadable.
plt.xticks(rotation=90)
# The `plt.tight_layout()` function is used to automatically adjust the padding and spacing between
# subplots in a figure. It ensures that all the elements in the plot, such as the axis labels, tick
# labels, and titles, are properly displayed without overlapping or being cut off. This function is
# particularly useful when creating plots with multiple subplots or when there is limited space
# available for the plot.
plt.tight_layout()

# The code `for bar, keyword_count in zip(bars, coffee_top_10['keyword_count']):` is a for loop that
# iterates over each bar and keyword_count value in the `bars` and `coffee_top_10['keyword_count']`
# lists, respectively.
for bar, keyword_count in zip(bars, coffee_top_10['keyword_count']):
    plt.text(bar.get_x() + bar.get_width()/2, keyword_count + 5, round(keyword_count, 2), ha='center', va='bottom', color='black', fontsize=9)

# Show the bar plot
st.pyplot(plt)
st.write('962 different vintages have at least 10 keywords "coffee".')