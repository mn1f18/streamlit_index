import streamlit as st
from src.utils.db import DatabaseConnection
from src.config import load_config
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#需求：对应表格对应图片总计和中国用堆叠柱状图
#国家翻译
country_dict = {
    "Bangladesh": "孟加拉",
    "Caimán, Islas": "开曼群岛",
    "China": "中国",
    "Chipre": "塞浦路斯",
    "Corea (Sur)": "韩国",
    "Grecia": "希腊",
    "Guinea": "几内亚",
    "Hong Kong": "香港",
    "Islas Marshall": "马绍尔群岛",
    "Italia": "意大利",
    "Japón": "日本",
    "Liberia": "利比里亚",
    "Malta": "马耳他",
    "Panamá": "巴拿马",
    "Países Bajos": "荷兰",
    "Portugal": "葡萄牙",
    "Singapur": "新加坡",
    "Alemania": "德国",
    "Antigua y Barbuda": "安提瓜和巴布达",
    "Arabia Saudita": "沙特阿拉伯",
    "Argelia": "阿尔及利亚",
    "Aruba": "阿鲁巴",
    "Bahamas": "巴哈马",
    "Bahrein": "巴林",
    "Bélgica": "比利时",
    "Chile": "智利",
    "Curazao": "库拉索",
    "Dinamarca": "丹麦",
    "Emiratos Árabes Unidos": "阿联酋",
    "España": "西班牙",
    "Estados Unidos": "美国",
    "Filipinas": "菲律宾",
    "Francia": "法国",
    "Guinea-Bissau": "几内亚比绍",
    "Isla de Man": "马恩岛",
    "Israel": "以色列",
    "Jordania": "约旦",
    "Kuwait": "科威特",
    "Líbano": "黎巴嫩",
    "Malasia": "马来西亚",
    "Montenegro": "黑山",
    "México": "墨西哥",
    "Noruega": "挪威",
    "Omán": "阿曼",
    "Palau": "帕劳",
    "Paraguay": "巴拉圭",
    "Perú": "秘鲁",
    "Puerto Rico": "波多黎各",
    "Qatar": "卡塔尔",
    "Reino Unido": "英国",
    "Suecia": "瑞典",
    "Suiza": "瑞士",
    "Tailandia": "泰国",
    "Turquía": "土耳其",
    "Uruguay": "乌拉圭",
    "Angola": "安哥拉",
    "Argentina": "阿根廷",
    "Brasil": "巴西",
    "Guyana": "圭亚那",
    "Marianas Septentrionales, Islas": "北马里亚纳群岛",
    "Marruecos": "摩洛哥",
    "Martinica": "马提尼克",
    "Tanzanía": "坦桑尼亚",
    "Viet Nam": "越南",
    "Acerbaiyan": "阿塞拜疆",
    "Albania": "阿尔巴尼亚",
    "Barbados": "巴巴多斯",
    "Bermuda": "百慕大",
    "Bolivia": "玻利维亚",
    "Cabo Verde": "佛得角",
    "Canadá": "加拿大",
    "Comoras": "科摩罗",
    "Congo": "刚果",
    "Costa de Marfil": "科特迪瓦",
    "Cuba": "古巴",
    "Egipto": "埃及",
    "Gabón": "加蓬",
    "Georgia": "格鲁吉亚",
    "Ghana": "加纳",
    "Indonesia": "印度尼西亚",
    "Irak": "伊拉克",
    "Libia": "利比亚",
    "Maldivas": "马尔代夫",
    "Mayotte": "马约特",
    "Palestina": "巴勒斯坦",
    "Polonia": "波兰",
    "Rusia": "俄罗斯",
    "Senegal": "塞内加尔",
    "Serbia": "塞尔维亚",
    "Sierra Leona": "塞拉利昂",
    "Sint Maarten": "圣马丁",
    "Suriname": "苏里南",
    "Tokelau": "托克劳",
    "Turkmenistán": "土库曼斯坦",
    "Túnez": "突尼斯",
    "Ucrania": "乌克兰",
    "Bhután": "不丹",
    "Guinea Ecuatorial": "赤道几内亚",
    "Laos": "老挝",
    "Myanmar": "缅甸",
    "Papua Nueva Guinea": "巴布亚新几内亚",
    "República Democrática del Congo": "刚果民主共和国",
    "India": "印度",
    "Bonaire, Saint Eustatius y Saba": "博奈尔、圣尤斯特歇斯和萨巴",
    "Gibraltar": "直布罗陀",
    "Seychelles": "塞舌尔",
    "Camerún": "喀麦隆",
    "Cook, Islas": "库克群岛",
    "Irán": "伊朗",
    "Macao": "澳门",
    "Mozambique": "莫桑比克",
    "Taiwán": "台湾",
    "Camboya": "柬埔寨",
    "Granada": "格林纳达",
    "Saint Kitts y Nevis": "圣基茨和尼维斯",
    "Belice": "伯利兹",
    "Lituania": "立陶宛",
    "Swazilandia": "斯威士兰",
    "San Vicente y las Granadinas": "圣文森特和格林纳丁斯",
    "Venezuela": "委内瑞拉",
    "Armenia": "亚美尼亚",
    "Gambia": "冈比亚",
    "Mauricio": "毛里求斯",
    "Timor Leste": "东帝汶",
    "Malvinas (Falkland), Islas": "马尔维纳斯群岛",
    "Nigeria": "尼日利亚",
    "Kenya": "肯尼亚",
    "Macedonia": "北马其顿",
    "Tayikistán": "塔吉克斯坦",
    "Luxemburgo": "卢森堡",
    "Mauritania": "毛里塔尼亚",
    "Djibouti": "吉布提",
    "Croacia": "克罗地亚",
    "Vanuatu": "瓦努阿图",
    "Irlanda": "爱尔兰",
    "Mónaco": "摩纳哥",
    "República Dominicana": "多米尼加共和国",
    "Finlandia": "芬兰",
    "Pitcairn": "皮特凯恩",
    "Honduras": "洪都拉斯",
    "Kazakhstán": "哈萨克斯坦",
    "Santo Tomé y Príncipe": "圣多美和普林西比",
    "Austria": "奥地利",
    "Letonia": "拉脱维亚",
    "Kirguistán": "吉尔吉斯斯坦",
    "Guam": "关岛",
    "Australia": "澳大利亚",
    "Rumania": "罗马尼亚",
    "Sudáfrica": "南非"
}

#编号翻译
code_dict = {
"020120": "鲜或冷的带骨牛肉",
"020130": "鲜或冷的去骨牛肉",
"020210": "冻整头及半头牛肉",
"020220": "冻带骨牛肉",
"020230": "冻去骨牛肉",
"020629": "其他冻牛杂碎"
}

# 在文件开头添加缓存装饰器
@st.cache_data
def load_data():
    """缓存数据库查询结果"""
    config = load_config()
    db = DatabaseConnection(config)
    df = db.query_to_df("SELECT * FROM brazil_beef_export_meta_data")
    db.close()
    
    # 预处理数据
    df.columns = ["Año", "Mes", "Código SA6", "Descripción SA6", "País", "Valor US$ FOB", "Peso (kg)"]
    df["对应翻译"] = df['Código SA6'].map(code_dict).fillna(df['Código SA6'])
    df["国家"] = df['País'].map(country_dict).fillna(df['País'])
    df["平均KG价格(美元)"] = (df['Valor US$ FOB']/df['Peso (kg)']).round(3)
    df['t'] = (df['Peso (kg)']/1000).round(2)
    return df

@st.cache_data
def process_data(df, select_country, select_year, select_year1):
    """缓存数据处理结果"""
    # 筛选年份范围
    mask = (df['Año'].astype(int) >= int(select_year)) & (df['Año'].astype(int) <= int(select_year1))
    filtered_df = df[mask].copy()
    
    # 计算价格表
    price_df = filtered_df[filtered_df["国家"] == select_country].groupby(["Año", "Mes"])["平均KG价格(美元)"].mean().reset_index()
    
    # 计算数量表
    volume_total = filtered_df.groupby(["Año", "Mes"])['t'].sum().reset_index()
    volume_country = filtered_df[filtered_df["国家"] == select_country].groupby(["Año", "Mes"])['t'].sum().reset_index()
    
    return price_df, volume_total, volume_country


#线图
def create_tablemap(df,start_year,end_year,country):
        """线图"""
        colors = px.colors.qualitative.Set3  # 使用 Set3 色板，也可以选择 Set1, Set2 等
        year_colors = {year: colors[i % len(colors)] for i, year in enumerate(sorted(df['Año'].unique()))}

        fig_seasonal_daily_r = px.line(
            df,
            x="Mes",
            y='平均KG价格(美元)',
            color="Año",
            title='巴西总进口价'+country+start_year+" ~ "+end_year,
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

def create_barchart(df, start_year, end_year,country):
    """柱状图"""
    fig = go.Figure()

    # Loop through unique values in the 'Año' column (i.e., years)
    for year in df['Año'].unique():
        # Filter data for the current year
        year_data = df[df['Año'] == year]

        # Add bars for t_中国 (Chinese total)


        # Add bars for the difference (t_总计 - t_中国)
        fig.add_trace(go.Bar(
            y=year_data["t_总计"],  
            name=f"Year {year} - t_总计",  # Name for the trace
            x=year_data["Mes"],
            offsetgroup=year  # Ensure bars for the same year are grouped together
        ))
        fig.add_trace(go.Bar(
            y=year_data["t_"+country],  
            name=f"Year {year} - t_"+country,  # Name for the trace
            x=year_data["Mes"],
            offsetgroup=year  # Ensure bars for the same year are grouped together
        ))



    # Update layout for better display
    fig.update_layout(
        title="数据图",
        xaxis_title="月",
        yaxis_title="t(吨)",
        barmode="group",  # Stacked bar chart within each year
        xaxis=dict(tickmode='array', tickvals=df['Mes']),  # Month names as ticks
        bargap=0.15,  # Controls the gap between groups of bars (for different years)
    )

    # Display the plot
    st.plotly_chart(fig)

def create_ranking_tables(df, start_year, end_year):
    """创建排名表格"""
    # 筛选年份范围
    mask = (df['Año'].astype(int) >= int(start_year)) & (df['Año'].astype(int) <= int(end_year))
    filtered_df = df[mask].copy()
    
    st.write("### 各国出口数据分析")
    
    # 创建年份选择器
    selected_year = st.selectbox(
        "选择要查看的年份",
        sorted(filtered_df['Año'].unique()),
        index=len(filtered_df['Año'].unique())-1
    )
    
    # 创建月份选择器
    selected_month = st.selectbox(
        "选择要查看的月份",
        sorted(filtered_df['Mes'].unique()),
        index=len(filtered_df['Mes'].unique())-1
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
        (filtered_df['Año'] == selected_year) & 
        (filtered_df['Mes'] == selected_month)
    ]
    total_volume = month_data['t'].sum()
    
    with col1:
        st.write(f"#### {selected_year}年{selected_month}月出口量排名")
        # 计算各国出口量和占比
        volume_ranking = (month_data
            .groupby('国家')
            .agg({
                't': 'sum',
                '平均KG价格(美元)': 'mean'
            })
            .sort_values('t', ascending=False)
            .reset_index()
            .head(selected_num))  # 只显示选择的前多少名
        
        # 添加排名列和计算占比
        volume_ranking.insert(0, '排名', range(1, len(volume_ranking) + 1))
        volume_ranking['占比%'] = (volume_ranking['t'] / total_volume * 100).round(2)
        volume_ranking['t'] = volume_ranking['t'].round(2)
        
        # 重命名列
        volume_ranking.columns = ['排名', '国家', '出口量(吨)', '平均价格', '占比%']
        
        # 显示表格
        st.dataframe(
            volume_ranking[['排名', '国家', '出口量(吨)', '占比%']],
            column_config={
                "排名": st.column_config.NumberColumn(width=60),
                "国家": st.column_config.TextColumn(width=100),
                "出口量(吨)": st.column_config.NumberColumn(
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
    st.title("巴西数据出口分析")
    
    # 加载数据（使用缓存）
    df = load_data()
    
    if df is not None:
        # 用户界面部分
        years = sorted(df["Año"].unique())
        
        # 将国家列表按照交易量排序，确保重要国家在前面
        country_volume = df.groupby("国家")['t'].sum().sort_values(ascending=False)
        top_countries = country_volume.index.tolist()
        
        # 确保中国在列表最前面
        if "中国" in top_countries:
            top_countries.remove("中国")
            top_countries.insert(0, "中国")
        
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
            
            # 国家选择器，默认选中中国
            select_country = st.selectbox(
                "选择国家",
                filtered_countries,
                index=filtered_countries.index("中国") if "中国" in filtered_countries else 0
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
        st.write(f"巴西总出口价 {select_country} {select_year} ~ {select_year1}")
        st.write(price_df)
        st.write(create_tablemap(price_df,select_year,select_year1,select_country))
        st.write(f"巴西总出口量占比 {select_country} {select_year} ~ {select_year1}")
        # 计算并显示占比
        volume_df = pd.merge(volume_total, volume_country, on=["Año", "Mes"], suffixes=('_总计', f'_{select_country}'))
        volume_df['占比%'] = (volume_df[f't_{select_country}'] / volume_df['t_总计'] * 100).round(2)
        st.write(volume_df)
        st.write(create_barchart(volume_df,select_year,select_year1,select_country))

        # 添加排名分析
        st.markdown("---")  # 添加分隔线
        create_ranking_tables(df, select_year, select_year1)

    # 示例交互组件
    if st.button("点击我"):
        st.balloons() 