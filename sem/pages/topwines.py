import streamlit as st
import pandas as pd
from featuress import top_wines


def main():
    st.title("Top wines")

    score = st.slider("Select a score", min_value=0, max_value=10)

    if st.button("Wines with the chosen score"):
        wines = top_wines(score) 

        st.table(wines)

main()

