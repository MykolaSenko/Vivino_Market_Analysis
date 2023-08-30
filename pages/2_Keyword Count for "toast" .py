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
# object. It retrieves the result set from the query, which contains the data selected from the
# database tables. The `cursor.execute()` method is used to execute SQL statements or queries in
# SQLite. In this case, it is executing the query and storing the result in the `keywords` variable.
keywords = cursor.execute(query1)

# The code `pd_keywords = pd.DataFrame(keywords)` is converting the result set obtained from the SQL
# query into a pandas DataFrame. The DataFrame is a two-dimensional tabular data structure with
# labeled axes (rows and columns).
pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns =['wine_id', 'vintages_name', 'keyword', 'keyword_count', 'keyword_group']

# The code `toast = pd_keywords[pd_keywords['keyword'] == 'toast']` is filtering the DataFrame
# `pd_keywords` to only include rows where the value in the 'keyword' column is equal to 'toast'. This
# creates a new DataFrame called `toast` that contains only the rows related to the keyword 'toast'.
toast = pd_keywords[pd_keywords['keyword'] == 'toast']
toast_top_10 = toast.nlargest(10, 'keyword_count')

# The code `plt.figure(figsize=(10, 10))` sets the size of the figure (plot) to be 10 inches in width
# and 10 inches in height.
plt.figure(figsize=(10, 10))
# The line `bars = plt.bar(toast_top_10['vintages_name'].tolist(), toast_top_10['keyword_count'])` is
# creating a bar plot using the `plt.bar()` function from the matplotlib library.
bars = plt.bar(toast_top_10['vintages_name'].tolist(), toast_top_10['keyword_count'])
# The code `plt.xlabel('Vintages')` sets the label for the x-axis of the plot as "Vintages". This
# label represents the categories or values on the x-axis.
plt.xlabel('Vintages')
# The code `plt.ylabel('Keyword Count for "toast"')` is setting the label for the y-axis of the plot
# as "Keyword Count for 'toast'". This label represents the values on the y-axis, which in this case
# is the count of the keyword "toast" for each vintage.
plt.ylabel('Keyword Count for "toast"')
# The code `plt.title('Keyword Count for "toast" in Top 10 Vintages')` is setting the title of the bar
# plot as "Keyword Count for 'toast' in Top 10 Vintages". This title provides a brief description of
# what the plot represents, which is the count of the keyword "toast" for the top 10 vintages.
plt.title('Keyword Count for "toast" in Top 10 Vintages')
# The code `plt.xticks(rotation=90)` is rotating the x-axis tick labels by 90 degrees. This is done to
# prevent the tick labels from overlapping with each other when there are many categories or values on
# the x-axis. By rotating the tick labels, it makes them more readable and avoids any overlapping
# issues.
plt.xticks(rotation=90)
# The `plt.tight_layout()` function is used to automatically adjust the padding between subplots or
# between the plot and the figure edges. It ensures that all elements of the plot are properly visible
# and not cut off. This function is particularly useful when there are multiple subplots or when the
# plot has a complex layout. It helps to improve the overall appearance and readability of the plot by
# optimizing the spacing between elements.
plt.tight_layout()

# The code `for bar, keyword_count in zip(bars, toast_top_10['keyword_count']):` is a loop that
# iterates over each bar in the bar plot and the corresponding keyword count value from the DataFrame
# `toast_top_10['keyword_count']`.
for bar, keyword_count in zip(bars, toast_top_10['keyword_count']):
    plt.text(bar.get_x() + bar.get_width()/2, keyword_count + 5, round(keyword_count, 2), ha='center', va='bottom', color='black', fontsize=9)

# Show the bar plot
st.pyplot(plt)
st.write('71 different vintages have at least 10 keywords "toast".')