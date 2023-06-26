import streamlit as st
from Upload_EPW import hide_streamlit_style
from bokeh_plots.histo2D import histo2D

# st.set_page_config(
#    page_title="EPW Explorer - Histogram 2D",
#    page_icon="🔎",
#    layout="wide",
#    initial_sidebar_state="expanded",
# )

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = st.session_state['df']
st.header("Page under construction")
# if st.session_state['loc']:
#     st.header("Hourly Values")
#     st.subheader("Pick your variable")
#     options = ['DB','RH','DirNormRad','DifHorzRad']
#     option = st.selectbox('Select variable', options, index=0)
#     variables=[]
#     with st.container():
#         st.header("Histogram 2D")
#         st.bokeh_chart(histo2D(df,variables), use_container_width=False)
# else:
#     st.header("Upload an EPW weather file to visualise the plots")