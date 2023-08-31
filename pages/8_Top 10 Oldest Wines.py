import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# The code `connexion = sqlite3.connect("data/vivino.db")` establishes a connection to a SQLite
# database file named "vivino.db".
connexion = sqlite3.connect("data/vivino.db")
cursor = connexion.cursor()

# The `query4` is a SQL query that retrieves data from multiple tables in a SQLite database. It
# selects the following columns: `vintages.wine_id`, `vintages.name`, `vintages.year`,
# `vintages.price_euros`, `regions.name`, and `grapes.name`.
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

# The line `old_10 = cursor.execute(query4)` is executing the SQL query `query4` using the `cursor`
# object. It retrieves the result set from the query and assigns it to the variable `old_10`. The
# `cursor.execute()` method is used to execute SQL statements or queries in SQLite.
old_10 = cursor.execute(query4)

# The code `pd_old_10 = pd.DataFrame(old_10)` is creating a pandas DataFrame from the result set
# `old_10` obtained from executing the SQL query. The DataFrame will have the same number of rows as
# the result set and the columns will be automatically labeled with default column names.
pd_old_10 = pd.DataFrame(old_10)

# The line `pd_old_10.columns =['vintages.wine_id', 'vintages.name', 'vintages.year',
# 'vintages.price_euros', 'regions.name', 'grapes.name']` is assigning new column names to the
# DataFrame `pd_old_10`.
pd_old_10.columns = [
    "vintages.wine_id",
    "vintages.name",
    "vintages.year",
    "vintages.price_euros",
    "regions.name",
    "grapes.name",
]

# The code block you provided is creating a scatter plot using matplotlib. Here's a breakdown of what
# each line does:
plt.figure(figsize=(15, 9))
font = {"family": "serif", "weight": "bold", "size": 22}
plt.rc("font", **font)
plt.scatter(pd_old_10["vintages.name"], pd_old_10["vintages.year"])
plt.xlabel("Vintages")
plt.ylabel("Year")
plt.title("Top 10 the Oldest Vintages")
plt.tight_layout()
plt.xticks(rotation=90)

# `st.pyplot(plt)` is a function provided by the Streamlit library that allows you to display a
# matplotlib plot in a Streamlit app. In this case, it is displaying the scatter plot created using
# `plt.scatter()` in the Streamlit app.
st.pyplot(plt)
