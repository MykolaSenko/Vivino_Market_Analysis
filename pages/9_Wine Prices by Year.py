import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# The code `connexion = sqlite3.connect("data/vivino.db")` establishes a connection to a SQLite
# database file named "vivino.db".
connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

# The `query3` is a SQL query that retrieves data from multiple tables in a database. It selects the
# following columns: `vintages.wine_id`, `vintages.name`, `vintages.year`, `vintages.price_euros`,
# `regions.name`, and `grapes.name`.
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

# The line `old = cursor.execute(query3)` is executing a SQL query using the `cursor` object. The
# query is stored in the variable `query3`.
old = cursor.execute(query3)

# The code `pd_old = pd.DataFrame(old)` is creating a pandas DataFrame from the result of the SQL
# query stored in the variable `old`. The DataFrame will have the same columns as the result of the
# query.
pd_old = pd.DataFrame(old)

# The line `pd_old.columns =['vintages.wine_id', 'vintages.name', 'vintages.year',
# 'vintages.price_euros', 'regions.name', 'grapes.name']` is assigning new column names to the
# DataFrame `pd_old`. It is specifying the column names as `vintages.wine_id`, `vintages.name`,
# `vintages.year`, `vintages.price_euros`, `regions.name`, and `grapes.name`.
pd_old.columns =['vintages.wine_id', 'vintages.name', 'vintages.year', 'vintages.price_euros', 'regions.name', 'grapes.name']

# The line `drop_indices = pd_old[pd_old['vintages.year'] == 'N.V.'].index` is creating a new variable
# `drop_indices` that stores the indices of rows in the DataFrame `pd_old` where the value in the
# column `vintages.year` is equal to 'N.V.'.
drop_indices = pd_old[pd_old['vintages.year'] == 'N.V.'].index

# Drop rows with 'N.V.' in 'vintages.price_euros'
pd_old.drop(drop_indices, inplace=True)

# The code block you provided is creating a scatter plot using the `matplotlib.pyplot` library. Here
# is a breakdown of what each line does:
plt.figure(figsize=(10, 9))
plt.scatter(pd_old['vintages.year'], pd_old['vintages.price_euros'])
plt.xlabel('Year')
plt.ylabel('Price (Euros)')
plt.title('Wine Prices by Year')
plt.tight_layout()

# `st.pyplot(plt)` is a function from the Streamlit library that allows you to display a Matplotlib
# plot in a Streamlit app. In this case, it is displaying the scatter plot created using
# `plt.scatter()` in the Streamlit app.
st.pyplot(plt)