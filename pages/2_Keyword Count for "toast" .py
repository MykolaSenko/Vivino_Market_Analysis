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

toast = pd_keywords[pd_keywords['keyword'] == 'toast']

toast_top_10 = toast.nlargest(10, 'keyword_count')

plt.figure(figsize=(10, 10))
bars = plt.bar(toast_top_10['vintages_name'].tolist(), toast_top_10['keyword_count'])
plt.xlabel('Vintages')
plt.ylabel('Keyword Count for "toast"')
plt.title('Keyword Count for "toast" in Top 10 Vintages')
plt.xticks(rotation=90)
plt.tight_layout()

for bar, keyword_count in zip(bars, toast_top_10['keyword_count']):
    plt.text(bar.get_x() + bar.get_width()/2, keyword_count + 5, round(keyword_count, 2), ha='center', va='bottom', color='black', fontsize=9)

# Show the bar plot
st.pyplot(plt)
st.write('71 different vintages have at least 10 keywords "toast".')