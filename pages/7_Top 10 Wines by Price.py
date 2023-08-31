import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# The code `connexion = sqlite3.connect("data/vivino.db")` establishes a connection to the SQLite
# database file named "vivino.db" located in the "data" directory.
connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

# The `query2` is a SQL query that retrieves data from multiple tables in the SQLite database. It
# selects the following columns: `vintages.wine_id`, `vintages.name`, `vintages.year`,
# `vintages.price_euros`, `regions.name`, and `grapes.name`.
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

# The line `prices = cursor.execute(query2)` is executing the SQL query `query2` using the `cursor`
# object. It retrieves the result set from the query and assigns it to the variable `prices`.
prices = cursor.execute(query2)

# The code `pd_prices = pd.DataFrame(prices)` is converting the result set `prices` into a pandas
# DataFrame. This allows us to manipulate and analyze the data using pandas functions.
pd_prices = pd.DataFrame(prices)
pd_prices.columns =['vintages.wine_id', 'vintages.name', 'vintages.year', 'vintages.price_euros', 'regions.name', 'grapes.name']

# The code `plt.figure(figsize=(10, 10))` creates a new figure with a specified size of 10 inches by
# 10 inches. This sets the dimensions of the plot.
plt.figure(figsize=(10, 10))
plt.scatter(pd_prices['vintages.name'][::-1], pd_prices['vintages.price_euros'][::-1], color='blue')
plt.xlabel('Vintages')
plt.ylabel('Price (Euros)')
plt.title('Top 10 Wines by Price')
plt.xticks(rotation=90)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

plt.rc('font', **font)

# `st.pyplot(plt)` is a function provided by the Streamlit library that allows you to display a
# matplotlib plot in your Streamlit app. It takes a matplotlib figure (`plt`) as an argument and
# renders it in the app. In this case, it is displaying the scatter plot of the top 10 wines by price.
st.pyplot(plt)
