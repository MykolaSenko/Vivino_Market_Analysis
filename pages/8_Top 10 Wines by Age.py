import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

query4 = """
SELECT 
    vintages.wine_id,
    vintages.name,
    vintages.year,
    vintages.price_euros,
    regions.name,
    grapes.name
    
FROM
    vintages
    JOIN wines ON vintages.wine_id = wines.id
    JOIN regions ON wines.region_id = regions.id
    JOIN most_used_grapes_per_country ON regions.country_code = most_used_grapes_per_country.country_code
    JOIN grapes ON most_used_grapes_per_country.grape_id = grapes.id
GROUP BY vintages.name
ORDER BY vintages.year
LIMIT 10
"""

old_10 = cursor.execute(query4)

pd_old_10 = pd.DataFrame(old_10)

pd_old_10.columns =['vintages.wine_id', 'vintages.name', 'vintages.year', 'vintages.price_euros', 'regions.name', 'grapes.name']

plt.figure(figsize=(14, 8))
plt.scatter(pd_old_10['vintages.year'], pd_old_10['vintages.name'])
plt.xlabel('Year')
plt.ylabel('Vintages')
plt.title('Top 10 Vintages by Age')
plt.tight_layout()

st.pyplot(plt)