import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

def typewriter(text: str, speed: float = 0.1):
    token = text.split()
    container = st.empty()
    for index in range(len(token)+1):
        curr_text = " ".join(token[:index])
        container.markdown("# "+curr_text)
        time.sleep(speed)


typewriter("Hello! Welcome to ")
