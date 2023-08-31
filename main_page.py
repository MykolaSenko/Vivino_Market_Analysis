# The code you provided is a Python script that uses the Streamlit library to create a webpage for the
# Vivino Market Analysis Project.
import streamlit as st
import pandas as pd

# The `st.set_page_config()` function is used to configure the settings of the Streamlit webpage. It
# takes two parameters:
st.set_page_config(
    page_title="Main Page",
    page_icon="👋",
)

# The code `st.write("# Welcome to Vivino! 👋")` is used to display a heading on the webpage that says
# "Welcome to Vivino! 👋".
st.write("# Welcome to Vivino! 👋")
st.title("This is a webpage of the Vivino Market Analysis Project")
st.image("source/download.jpeg")


# The `st.markdown()` function is used to display formatted text on the Streamlit webpage. It takes a
# string parameter that contains Markdown syntax, which allows for the formatting of text, including
# headings, links, bullet points, and more.
st.markdown(
    """
    The Vivino Market Analysis Project is aimed at analyzing the wine market based on data gathered by Vivino. 
    The section of the project presented on this webpage focuses on identifying wines that are associated 
    with keywords such as coffee, toast, green apple, cream, and citrus. Subsequently, the top 10 of these 
    wines are analyzed. The project also displays wine prices by year and examines the correlations among 
    them. This entire process is facilitated using Streamlit.

    You can access the project's repository [here](https://github.com/MykolaSenko/Vivino_Market_Analysis).

    The project was carried out by a team of three Junior Data Scientists from [BeCode](https://becode.org) between August 20 and 31, 2023.

    Team Leader:
    
    Weiying Zhao: [LinkedIn](https://www.linkedin.com/in/weiying-zhao-a4a307241/), [GitHub](https://github.com/Winzhao0545)
    
    Team Members:
    
    Bram Michielsen: [LinkedIn](https://www.linkedin.com/in/brammichielsen/), [GitHub](https://github.com/BramMichielsen)
    
    Mykola Senko: [LinkedIn](https://www.linkedin.com/in/mykola-senko-683510a4), [GitHub](https://github.com/MykolaSenko)
    
    Gent, Belgium
    
    August 31, 2023
"""
)
