import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sqlite3
import pandas as pd

connexion = sqlite3.connect("../data/vivino.db")
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
display(pd_keywords)

plt.figure(figsize=(10, 6))
plt.bar(pd_keywords['keyword'], pd_keywords['keyword_count'])
plt.xlabel('Keyword')
plt.ylabel('Keyword Count')
plt.title('Keyword Counts for Wines')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the histogram
st.plt.show()
st.sidebar.title('Choose your visualization')
st.sidebar.selectbox('Choose one of the following', ['---------------', 'Keyword Counts for Wines', 'Keyword Count for "toast" in Top 10 Vintages', 'Keyword Count for "cintrus" in Top 10 Vintages', 'Keyword Count for "coffee" in Top 10 Vintage', 'Keyword Count for "green apple" in Top 10 Vintages', 'Keyword Count for "cream" in Top 10 Vintages', 'Top 10 Wines by Price', 'Top 10 Vintages by Year', 'Wine Prices by Year'])