import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

query3 = """
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
"""

old = cursor.execute(query3)

pd_old = pd.DataFrame(old)

pd_old.columns =['vintages.wine_id', 'vintages.name', 'vintages.year', 'vintages.price_euros', 'regions.name', 'grapes.name']

drop_indices = pd_old[pd_old['vintages.year'] == 'N.V.'].index

# Drop rows with 'N.V.' in 'vintages.price_euros'
pd_old.drop(drop_indices, inplace=True)

plt.figure(figsize=(10, 6))
plt.scatter(pd_old['vintages.year'], pd_old['vintages.price_euros'])
plt.xlabel('Year')
plt.ylabel('Price (Euros)')
plt.title('Wine Prices by Year')
plt.tight_layout()

st.pyplot(plt)