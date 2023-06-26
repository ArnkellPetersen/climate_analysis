import streamlit as st
from Upload_EPW import hide_streamlit_style
from bokeh_plots.hourly import lineGraph

# st.set_page_config(
#    page_title="EPW Explorer - Hourly",
#    page_icon="🕘",
#    layout="wide",
#    initial_sidebar_state="expanded",
# )

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = st.session_state['df']

if st.session_state['df'] is not None:
    st.header("Hourly Values")
    st.subheader("Pick your variables")
    options = ['DryBulb','RelativeHumidity','DewPoint','WindSpeed','GlobalHorizontalRadiation','DirectNormalRadiation','DiffuseHorizontalRadiation']
    col1, col2 = st.columns(2)
    with col1:
        option_l = st.selectbox('Variable for the left axis', options, index=0)
    with col2:
        option_r = st.selectbox('Variable for the right axis', options, index=1)
    with st.container():
        st.bokeh_chart(lineGraph(df, var1=option_l, var2=option_r), use_container_width=False)
else:
    st.header("Upload an EPW weather file to visualise the plots")