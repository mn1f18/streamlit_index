import streamlit as st
from src.config import load_config
from src.pages import data_analysis,data_analysis_for_brazil,data_analysis_for_China
from src.utils.helpers import setup_page

def main():
    # 加载配置
    config = load_config()
    
    # 设置页面基本配置
    setup_page()
    
    # 创建侧边栏导航
    st.sidebar.title("导航")
    page = st.sidebar.selectbox(
        "选择页面",
        ["巴西数据出口分析", "牛肉数据分析", "中国数据进口分析"]
    )
    
    # 页面路由
    if page == "巴西数据出口分析":
        data_analysis_for_brazil.show()
    elif page == "牛肉数据分析":
        data_analysis.show()
    elif page == "中国数据进口分析":
        data_analysis_for_China.show()

if __name__ == "__main__":
    main()
