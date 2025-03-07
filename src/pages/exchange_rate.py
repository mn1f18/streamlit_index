import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import streamlit as st
from bs4 import BeautifulSoup


# 卖汇
@st.cache_data(ttl=1800)
def parse_exchange_rates(html):
    """javascripe 转换后用soup的我查"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    driver.get(html)
    time.sleep(5)  


    html = driver.page_source
    driver.quit()
    try:
 
        soup = BeautifulSoup(html, "html.parser")
        #找对应标头
        p_element = soup.find('p', string=lambda text: text and "现汇卖出价" in text)
        next_p = p_element.find_next_sibling('p') if p_element else None

        if not p_element:
            return "Error: Could not find the <b> element."
        
        usd_to_cny = next_p.text.split('=')[1].split('元')[0]
        return usd_to_cny
    except Exception as e:
        return f"Error parsing data: {e}"


#美元兑雷埃厄，美元指数
@st.cache_data(ttl=1800)  # 30 min
def fetch_dxy(url):
    
    try:

        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(service=Service(), options=chrome_options)
    
        driver.get(url)

        time.sleep(5)
        
        #找对应标头
        dxy_element = driver.find_element(By.CSS_SELECTOR, "span.last-JWoJqCpY.js-symbol-last")
        dxy_value = dxy_element.text
       
        change_value = driver.find_element(By.CSS_SELECTOR, "div.change-JWoJqCpY span").text
        percentage_change = driver.find_element(By.CSS_SELECTOR, "div.change-JWoJqCpY span.js-symbol-change-pt").text
    except Exception as e:
        print("Error:", e)
        change_value, percentage_change = "N/A", "N/A"

    driver.quit()

    return dxy_value,change_value,percentage_change



def show():
    st.title("汇率")  
    url1 = "https://www.tradingview.com/symbols/TVC-DXY/"#tradingview
    url2 = 'https://www.tradingview.com/symbols/USDBRL/'#tradingview
    url3 = "https://chl.cn/huilv/?usd"#我查
    dxy,dxy1,dxy2 = fetch_dxy(url1)
    usd_br,usd_br_1,usd_br_2 = fetch_dxy(url2)
    st.metric(label="### 美元指数", value=dxy)
    st.write(dxy1,dxy2,"(对应昨天的数据)")
    st.metric(label="### 美元对巴西雷亚尔", value=usd_br)
    st.write(usd_br_1,usd_br_2,"(对应昨天的数据)")
    exchange_rates = parse_exchange_rates(url3)
    st.metric(label="### 美元对人名币（现汇卖出价）", value=exchange_rates)
    # 示例输入
    st.write('---')
    tit2, tit3 ,tit4 ,tit5 = st.columns([1, 1, 1, 1])
    with tit2:
        futures_price = st.number_input("### 请输入期货价格: (吨)", min_value=0.0)
    with tit3:
        fee_price = st.number_input("### 请输入杂费: （默认+500杂费)", min_value=0.0,value=500.0)
    with tit4:
        intax_price = st.number_input("### 请输入进口税: (默认1.12)", min_value=0.0,value=1.12)
    with tit5:
        outtax_price = st.number_input("### 请输入期货价格: (默认1.09)", min_value=0.0,value=1.09)
    # 计算现货价格
    spot_price = futures_price*intax_price*outtax_price*float(exchange_rates)+fee_price
    st.write(f"### 现货价格为: {spot_price/1000:.2f}元/千克")
    st.write('---')
    # 计算转换价格
    futures_change_price = st.number_input("### 请输入雷亚尔价格: ", min_value=0.0)
    change_price = futures_change_price/float(usd_br)/15
    st.write(f"### 转换成美元后价格为: {change_price:.2f}美元/千克")

    #刷新数据
    if st.button("刷新数据"):
        st.cache_data.clear()  # Clear the cache data
        st.rerun()  # Trigger a rerun
    

