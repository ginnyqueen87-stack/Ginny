# ============================================================
# 練習 15 ── Amazon 運送城市地圖（Scatter Mapbox）
# ============================================================
# 學習重點：
#   1. 使用 Amazon 訂單資料
#   2. groupby 統計各城市訂單數
#   3. scatter_mapbox 繪製城市分布
#   4. 點大小代表訂單量
#
# 執行：
# streamlit run amazon_map.py
# ============================================================

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------
# Streamlit 頁面設定
# ------------------------------------------------
st.set_page_config(
    page_title="Amazon 運送城市地圖",
    layout="wide"
)

st.title("Amazon 訂單運送城市地圖")

st.caption("資料來源：Amazon Sale Report.csv")

# ------------------------------------------------
# 讀取資料
# ------------------------------------------------
orders = pd.read_csv(
    "./Amazon Sale Report.csv"
)

# ------------------------------------------------
# 清理資料
# ------------------------------------------------
orders = orders.dropna(subset=["ship-city"])

# ------------------------------------------------
# 統計每個城市訂單量
# ------------------------------------------------
city_orders = (
    orders.groupby("ship-city")
    .size()
    .reset_index(name="訂單數")
)

# ------------------------------------------------
# 建立城市座標
# ------------------------------------------------
city_coords = {
    "BENGALURU": [12.9716, 77.5946],
    "HYDERABAD": [17.3850, 78.4867],
    "MUMBAI": [19.0760, 72.8777],
    "NEW DELHI": [28.6139, 77.2090],
    "CHENNAI": [13.0827, 80.2707],
    "PUNE": [18.5204, 73.8567],
    "KOLKATA": [22.5726, 88.3639],
    "AHMEDABAD": [23.0225, 72.5714],
    "JAIPUR": [26.9124, 75.7873],
}

# ------------------------------------------------
# 加入經緯度
# ------------------------------------------------
city_orders["latitude"] = city_orders["ship-city"].map(
    lambda x: city_coords.get(
        str(x).upper(),
        [None, None]
    )[0]
)

city_orders["longitude"] = city_orders["ship-city"].map(
    lambda x: city_coords.get(
        str(x).upper(),
        [None, None]
    )[1]
)

# ------------------------------------------------
# 移除沒有座標的城市
# ------------------------------------------------
city_orders = city_orders.dropna(
    subset=["latitude", "longitude"]
)

# ------------------------------------------------
# KPI
# ------------------------------------------------
st.metric(
    "地圖中的城市數",
    f"{len(city_orders):,} 個"
)

# ------------------------------------------------
# 左右版面
# ------------------------------------------------
col1, col2 = st.columns([1, 3])

# ------------------------------------------------
# 左側：資料表
# ------------------------------------------------
with col1:

    st.subheader("訂單最多城市")

    st.dataframe(
        city_orders
        .sort_values("訂單數", ascending=False)
        .head(20),

        use_container_width=True
    )

# ------------------------------------------------
# 右側：地圖
# ------------------------------------------------
with col2:

    fig = px.scatter_mapbox(
        city_orders,

        lat="latitude",
        lon="longitude",

        size="訂單數",
        color="訂單數",

        hover_name="ship-city",

        hover_data={
            "訂單數": True,
            "latitude": False,
            "longitude": False,
        },

        mapbox_style="open-street-map",

        zoom=3,

        center={
            "lat": 22.0,
            "lon": 78.0
        },

        height=600,

        color_continuous_scale="YlOrRd",

        title="Amazon 訂單城市分布"
    )

    fig.update_layout(
        margin={
            "r": 0,
            "t": 40,
            "l": 0,
            "b": 0
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )




