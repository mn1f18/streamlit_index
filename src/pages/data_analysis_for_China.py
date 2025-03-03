import streamlit as st
from src.utils.db import DatabaseConnection
from src.config import load_config
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder #测试
import plotly.express as px
import plotly.graph_objects as go

# 在文件开头添加缓存装饰器
@st.cache_data
def load_data():
    """缓存数据库查询结果"""
    config = load_config()
    db = DatabaseConnection(config)
    df = db.query_to_df("SELECT * FROM muji_data.china_import_raw")
    db.close()
    
    # 预处理数据
    df['year'] = df['数据年月'].astype(str).str[:4]  # First 4 digits as year
    df['month'] = df['数据年月'].astype(str).str[4:6] #last 2 digits as month
    df['数量'] =pd.to_numeric(df['第一数量'], errors='coerce')#数据居然是str形式
    df['美元'] = df['美元'].str.replace(',', '', regex=False).str.strip()#数据居然是str形式且带有“，”不删除逗号无法转换成数字
    df['美元'] =pd.to_numeric(df['美元'], errors='coerce')#数据居然是str形式
    df['国家'] = df['贸易伙伴名称']
    df['t'] =(df['数量']/1000).round(2)
    df["平均KG价格(美元)"] = (df['美元']/df['数量']).round(3)
    df = df[['year','month', '商品名称', '国家', 't','平均KG价格(美元)','美元','数量']]
    return df

@st.cache_data
def process_data(df, select_country, select_year, select_year1):
    """缓存数据处理结果"""
    # 筛选年份范围
    mask = (df['year'].astype(int) >= int(select_year)) & (df['year'].astype(int) <= int(select_year1))
    filtered_df = df[mask].copy()
    
    # 计算价格表
    price_df = filtered_df[filtered_df['国家'] == select_country].groupby(["year", "month"])["平均KG价格(美元)"].mean().reset_index()
    # 计算数量表
    volume_total = filtered_df.groupby(["year", "month"])['t'].sum().reset_index()
    volume_country = filtered_df[filtered_df["国家"] == select_country].groupby(["year", "month"])['t'].sum().reset_index()
    
    return price_df, volume_total, volume_country

#测试用代码
def testmessage(df):
    
    gb = GridOptionsBuilder.from_dataframe(df)

    # Enable features: sorting, filtering, editing, and row selection
    gb.configure_default_column(filterable=True, sortable=True, editable=True)
    gb.configure_selection('multiple')  # Allow multiple row selection

    # Set pagination
    gb.configure_pagination(paginationPageSize=3)

    # Generate Grid options
    grid_options = gb.build()

    # Display Grid and capture events (row selection)
    response = AgGrid(df, gridOptions=grid_options,theme='ag-theme-alpine', update_mode='MODEL_CHANGED')
    return response


#线图
def create_tablemap(df,start_year,end_year,country):
        """线图"""
        colors = px.colors.qualitative.Set3  # 使用 Set3 色板，也可以选择 Set1, Set2 等
        year_colors = {year: colors[i % len(colors)] for i, year in enumerate(sorted(df['year'].unique()))}
        fig_seasonal_daily_r = px.line(
            df,
            x='month',
            y='平均KG价格(美元)',
            color='year',
            title='中国总进口价'+country+start_year+" ~ "+end_year,
            color_discrete_map=year_colors
        )
        fig_seasonal_daily_r.update_xaxes(
            title='月',
            ticktext=['一月', '二月', '三月', '四月', '五月', '六月', 
                        '七月', '八月', '九月', '十月', '十一月', '十二月'],
            tickvals=list(range(1, 13))
        )
        fig_seasonal_daily_r.update_yaxes(title='平均KG价格(美元)')
        
        # 添加网格线使图表更清晰
        fig_seasonal_daily_r.update_layout(
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            ),
            showlegend=True,
            legend_title="年份"
        )
        st.plotly_chart(fig_seasonal_daily_r)

#柱状图
def create_barchart(df, start_year, end_year,country):
    """柱状图"""
    fig = go.Figure()

    # Loop through unique values in the 'Año' column (i.e., years)
    for year in df['year'].unique():
        # Filter data for the current year
        year_data = df[df['year'] == year]


        # Add bars for the difference (t_总计 - t_中国)
        fig.add_trace(go.Bar(
            y=year_data["t_总计"],  
            name=f"Year {year} - t_总计",  # Name for the trace
            x=year_data["month"],
            offsetgroup=year  # Ensure bars for the same year are grouped together
        ))
        fig.add_trace(go.Bar(
            y=year_data["t_"+country],  
            name=f"Year {year} - t_"+country,  # Name for the trace
            x=year_data["month"],
            offsetgroup=year  # Ensure bars for the same year are grouped together
        ))



    # Update layout for better display
    fig.update_layout(
        title="数据图中国",
        xaxis_title="月",
        yaxis_title="t(吨)",
        barmode="group",  # Stacked bar chart within each year
        xaxis=dict(tickmode='array', tickvals=df['month']),  # Month names as ticks
        bargap=0.15,  # Controls the gap between groups of bars (for different years)
    )

    # Display the plot
    st.plotly_chart(fig)

def create_ranking_tables(df, start_year, end_year):
    """创建排名表格"""
    # 筛选年份范围
    mask = (df['year'].astype(int) >= int(start_year)) & (df['year'].astype(int) <= int(end_year))
    filtered_df = df[mask].copy()
    
    st.write("### 各国进口数据分析")
    
    # 创建年份选择器
    selected_year = st.selectbox(
        "选择要查看的年份",
        sorted(filtered_df['year'].unique()),
        index=len(filtered_df['year'].unique())-1
    )
    
    # 创建月份选择器
    selected_month = st.selectbox(
        "选择要查看的月份",
        sorted(filtered_df['month'].unique()),
        index=len(filtered_df['month'].unique())-1
    )
    selected_num = st.selectbox(
        "选择要查看的数量",
        list(range(len(filtered_df['国家'].unique())+1)),
        index=10 if  10 <= len(filtered_df['国家'].unique()) else len(filtered_df['国家'].unique())
    )
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    # 首先计算选定月份的总出口量
    month_data = filtered_df[
        (filtered_df['year'] == selected_year) & 
        (filtered_df['month'] == selected_month)
    ]
    total_volume = month_data['t'].sum()
    
    with col1:
        st.write(f"#### {selected_year}年{selected_month}月进口量排名")
        # 计算各国出口量和占比
        volume_ranking = (month_data
            .groupby('国家')
            .agg({
                't': 'sum',
                '平均KG价格(美元)': 'mean'
            })
            .sort_values('t', ascending=False)
            .reset_index()
            .head(selected_num))  # 只显示前10名
        
        # 添加排名列和计算占比
        volume_ranking.insert(0, '排名', range(1, len(volume_ranking) + 1))
        volume_ranking['占比%'] = (volume_ranking['t'] / total_volume * 100).round(2)
        volume_ranking['t'] = volume_ranking['t'].round(2)
        
        # 重命名列
        volume_ranking.columns = ['排名', '国家', '进口量(吨)', '平均价格', '占比%']
        
        # 显示表格
        st.dataframe(
            volume_ranking[['排名', '国家', '进口量(吨)', '占比%']],
            column_config={
                "排名": st.column_config.NumberColumn(width=60),
                "国家": st.column_config.TextColumn(width=100),
                "进口量(吨)": st.column_config.NumberColumn(
                    format="%.2f",
                    width=100
                ),
                "占比%": st.column_config.NumberColumn(
                    format="%.2f",
                    width=80
                )
            },
            hide_index=True
        )
    
    with col2:
        st.write(f"#### {selected_year}年{selected_month}月主要进口国价格")
        # 使用出口量排名前10的国家的价格数据
        price_data = volume_ranking[['排名', '国家', '平均价格']]
        price_data['平均价格'] = price_data['平均价格'].round(3)
        price_data.columns = ['排名', '国家', '平均价格(USD/kg)']
        
        # 显示表格
        st.dataframe(
            price_data,
            column_config={
                "排名": st.column_config.NumberColumn(width=60),
                "国家": st.column_config.TextColumn(width=100),
                "平均价格(USD/kg)": st.column_config.NumberColumn(
                    format="%.3f",
                    width=120
                )
            },
            hide_index=True
        )

def show():
    st.title("中国数据进口分析")
    
    # 加载数据（使用缓存）
    df = load_data()


    if df is not None:
        # 用户界面部分
        years = sorted(df["year"].unique())
        
        # 将国家列表按照交易量排序，确保重要国家在前面
        country_volume = df.groupby("国家")['t'].sum().sort_values(ascending=False)
        top_countries = country_volume.index.tolist()
        
        # 确保巴西在列表最前面
        if "巴西" in top_countries:
            top_countries.remove("巴西")
            top_countries.insert(0, "巴西")
        
        tit1, tit2, tit3 = st.columns([1, 1, 1])
        
        #选最近的时间
        closest_year = max(map(int, years))

        with tit1:
            # 添加搜索框
            search_country = st.text_input("搜索国家", "")
            
            # 过滤国家列表
            if search_country:
                filtered_countries = [
                    country for country in top_countries 
                    if search_country.lower() in country.lower()
                ]
            else:
                filtered_countries = top_countries
            
            # 国家选择器，默认选中巴西
            select_country = st.selectbox(
                "选择国家",
                filtered_countries,
                index=filtered_countries.index("巴西") if "巴西" in filtered_countries else 0
            )
        with tit2:
            select_year = st.selectbox(
                "请选择开始年",
                years,
                index=years.index(closest_year) if closest_year in years else len(years)-1,  # 默认选择2025年
                key='start_year'
            )
        with tit3:
            select_year1 = st.selectbox(
                "请选择结束年",
                years,
                index=years.index(closest_year) if closest_year in years else len(years)-1,  # 默认选择2025年
                key='end_year'
            )
        
        # 处理数据（使用缓存）
        price_df, volume_total, volume_country = process_data(df, select_country, select_year, select_year1)
        
        # 显示结果
        st.write(f"中国总进口价 {select_country} {select_year} ~ {select_year1}")
        
        #测试代码
        chinainput = testmessage(price_df)
        st.write(chinainput['selected_rows'])
        st.write(create_tablemap(price_df,select_year,select_year1,search_country))
        #结束代码        
        
        st.write(f"中国总进口量占比 {select_country} {select_year} ~ {select_year1}")
        # 计算并显示占比
        volume_df = pd.merge(volume_total, volume_country, on=["year", "month"], suffixes=('_总计', f'_{select_country}'))
        volume_df['占比%'] = (volume_df[f't_{select_country}'] / volume_df['t_总计'] * 100).round(2)
        
        #测试代码
        abctest = testmessage(volume_df)
        st.write(abctest['selected_rows'])
        st.write(create_barchart(volume_df,select_year,select_year1,select_country))
        #结束代码


        # 添加排名分析
        st.markdown("---")  # 添加分隔线
        create_ranking_tables(df, select_year, select_year1)

    # 示例交互组件
    if st.button("点击我"):
        st.balloons() 