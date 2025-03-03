import streamlit as st

def setup_page():
    """
    设置页面基本配置
    """
    st.set_page_config(
        page_title="我的Streamlit应用",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    ) 
    