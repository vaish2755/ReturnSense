import os

import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()

BANK_ID = "returnsense"


@st.cache_resource
def get_hindsight_client():

    return Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.environ["HINDSIGHT_API_KEY"],
        timeout=60.0
    )


client = get_hindsight_client()


def close_client():
    # Do not close the cached client after every Streamlit interaction.
    # Streamlit reuses the cached Hindsight client.
    pass