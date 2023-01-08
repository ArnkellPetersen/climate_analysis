import streamlit as st
from Upload_EPW import hide_streamlit_style
from bokeh_plots.histo2D import histo2D
from bokeh_plots.heatmap import heatmap
from bokeh_plots.line_graph import lineGraph

st.set_page_config(
   page_title="EPW Explorer - Free Style",
   page_icon="🧭",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = st.session_state['df']

if st.session_state['df'] is not None:
    st.header("Hourly Values")
    st.subheader("Pick your variables")
    options = ['DB','RH','WB','GloHorzRad']
    col1, col2 = st.columns(2)
    with col1:
        option_l = st.selectbox('Variable for the left axis', options)
    with col2:
        option_r = st.selectbox('Variable for the right axis', options)
    with st.container():
        st.bokeh_chart(lineGraph(df, var1=option_l, var2=option_r), use_container_width=True)
    with st.container():
        st.header("Histogram 2D")
        st.subheader("Pick your variables")
        st.bokeh_chart(histo2D(df), use_container_width=True)
else:
    st.header("Upload an EPW weather file to visualise the plots")