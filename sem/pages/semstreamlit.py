import streamlit as st
import pandas as pd
from featuress import top_wines
from featuress import wines_keynotes
from featuress import keywords

def main():
    st.title("Top wines")

    keywords_list = keywords()  # Your list of keywords

    # Selectbox for choosing keywords
    k1 = st.selectbox("Select a keyword for k1", keywords_list, key="k1")
    k2 = st.selectbox("Select a keyword for k2", [None] + keywords_list, key="k2")
    k3 = st.selectbox("Select a keyword for k3", [None] + keywords_list, key="k3")
    k4 = st.selectbox("Select a keyword for k4", [None] + keywords_list, key="k4")
    k5 = st.selectbox("Select a keyword for k5", [None] + keywords_list, key="k5")


    if st.button("Wines with the chosen keywords"):
        wines = wines_keynotes(k1=k1, k2=k2, k3=k3, k4=k4, k5=k5)

        st.table(wines)

main()
