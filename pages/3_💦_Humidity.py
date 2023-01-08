import streamlit as st
from Upload_EPW import hide_streamlit_style
from bokeh_plots.monthly_graph import monthlyGraph

st.set_page_config(
   page_title="EPW Reader - Humidity",
   page_icon="👓",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = st.session_state['df']

if st.session_state['df'] is not None:
    pass
else:
    st.header("Upload an EPW weather file to visualise the plots")