import streamlit as st
from applications import get_random_quotes



def home_page():
    st.title("Your Morning Buddy")
    st.markdown("---")
    st.subheader("A Thought for your Day")

    with st.spinner('Fetching your daily inspirations...'):
     if 'quote' not in st.session_state:
        quote=get_random_quotes()
        st.session_state.quote=quote
    st.info(f"{st.session_state.quote}")






# Sitebar Navigations

st.sidebar.title("Navigations")
st.sidebar.markdown('---')
page_option=st.sidebar.radio("Choose a Page:",("Home","Weather of your City","News by Interest","Smart Planner"))
st.sidebar.markdown('---')

if page_option=="Home":
    home_page()
elif page_option=="Weather of your City":
    st.title("Welcome to Whether Page")
elif page_option=="News by Interest":
    st.title("Welcome to News by Interest")
elif page_option=="Smart Planner":
    st.title("Welcome to Smart Planner page")
