import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

query2 = """
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
ORDER BY vintages.price_euros DESC
LIMIT 10
"""

prices = cursor.execute(query2)

pd_prices = pd.DataFrame(prices)
pd_prices.columns =['vintages.wine_id', 'vintages.name', 'vintages.year', 'vintages.price_euros', 'regions.name', 'grapes.name']

plt.figure(figsize=(10, 10))
plt.scatter(pd_prices['vintages.price_euros'][::-1], pd_prices['vintages.name'][::-1], color='blue')
plt.xlabel('Price (Euros)')
plt.ylabel('Vintages')
plt.title('Top 10 Wines by Price')

st.pyplot(plt)
