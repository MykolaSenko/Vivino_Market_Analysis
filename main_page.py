import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Main Page",
    page_icon="👋",
)

st.write("# Welcome to Vivino! 👋")
st.title('This is a webpage of the Vivino Market Analysis Project')
st.image('source/download.jpeg')


st.markdown(
    """
    Interactive text here. Example:
    
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)