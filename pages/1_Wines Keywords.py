import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

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

keywords = cursor.execute(query1)

pd_keywords = pd.DataFrame(keywords)
pd_keywords.columns =['wine_id', 'vintages_name', 'keyword', 'keyword_count', 'keyword_group']

# Calculate the maximum value for each keyword
max_values = pd_keywords.groupby('keyword')['keyword_count'].max()

plt.figure(figsize=(10, 6))
bars = plt.bar(pd_keywords['keyword'], pd_keywords['keyword_count'])
plt.xlabel('Keywords')
plt.ylabel('Keyword Count')
plt.title('Keyword Counts for Wines')
plt.xticks(rotation=45)
plt.tight_layout()

# Adding maximum value labels on top of the bars
for bar, keyword in zip(bars, pd_keywords['keyword']):
    if max_values[keyword] == bar.get_height():
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 5, round(yval, 2), ha='center', va='bottom', color='black', fontsize=9)

# Show the histogram
st.pyplot(plt)
st.write('1205 different vintages have at least 10 keywords "coffee", "toast", "green apple", "cream" and "citrus".')