import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load Dataset
@st.cache_data
def load_data():
    df_day = pd.read_csv("dashboard/day_cleandata.csv")
    df_hour = pd.read_csv("dashboard/hour_cleandata.csv")
    return df_day, df_hour

df_day, df_hour = load_data()

st.title("Bike Sharing Dashboard :sparkles:")

# Filter Pada Sidebar
min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.jpeg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Tanggal
date_filter_day = df_day[(df_day["dteday"] >= str(start_date)) & 
                        (df_day["dteday"] <= str(end_date))]
date_filter_hour = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                        (df_hour["dteday"] <= str(end_date))]

# Fungsi pola penggunaan sepeda berdasarkan musim
def create_seasonal(df):
    seasonal_df = date_filter_day.groupby("season")["cnt"].mean().reset_index()
    return seasonal_df

# Fungsi waktu paling sibuk untuk penyewaan sepeda dalam sehari
def create_daily_busy(df):
    daily_busy_df = date_filter_hour.groupby("kategori_waktu")["cnt"].mean().reset_index()
    return daily_busy_df

# Fungsi pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda setiap harinya
def create_weather(df):
    weather_df = date_filter_day.groupby("weathersit")["cnt"].mean().reset_index()
    return weather_df

# Fungsi pengaruh hari kerja terhadap jumlah penyewaan sepeda
def create_workingday(df):
    workingday_df = date_filter_day.groupby("workingday")["cnt"].mean().reset_index()
    return workingday_df

def create_cust_weekday(df):
    cust_weekday_df = date_filter_day.pivot_table(index="weekday", values="cnt", aggfunc="mean").reset_index()
    return cust_weekday_df

seasonal = create_seasonal(date_filter_day)
daily_busy = create_daily_busy(date_filter_hour)
weather = create_weather(date_filter_day)
workingday = create_workingday(date_filter_day)
cust_weekday = create_cust_weekday(date_filter_day)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = date_filter_day.casual.sum()
    st.metric("Total Casual Cust", value=total_casual)

with col2:
    total_registered = date_filter_day.registered.sum()
    st.metric("Total Registered Cust", value=total_registered)

with col3:
    total_cnt = date_filter_day.cnt.sum()
    st.metric("Total Cust", value=total_cnt)

# Fungsi untuk menentukan warna berdasarkan nilai tertinggi
def get_colors(data, column, base_color, highlight_color):
    max_value = data[column].max()
    return [highlight_color if val == max_value else base_color for val in data[column]]

col1, col2 = st.columns(2)

with col1:
    # Working Day
    st.subheader('Working Day')
    workingday_colors = get_colors(workingday, "cnt", "#D3D3D3", "#8BC43D")
    plt.figure(figsize=(5, 3))
    sns.barplot(data=workingday, x="workingday", y="cnt", palette=workingday_colors)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(plt)

with col2:
    # Customer Weekday
    st.subheader('Customer Weekday')
    cust_weekday_colors = get_colors(cust_weekday, "cnt", "#D3D3D3", "#8BC43D")
    plt.figure(figsize=(8, 5))
    sns.barplot(data=cust_weekday, x="weekday", y="cnt", palette=cust_weekday_colors)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(plt)

# Daily Busy Hour
st.subheader('Daily Busy Hour')
daily_busy_colors = get_colors(daily_busy, "cnt", "#D3D3D3", "#8BC43D")
plt.figure(figsize=(10, 5))
sns.barplot(data=daily_busy, x="kategori_waktu", y="cnt", palette=daily_busy_colors)
plt.xlabel(None)
plt.ylabel(None)
st.pyplot(plt)

tab1, tab2 = st.tabs(["Seasonal Impact", "Weather Impact"])

with tab1:
    # Seasonal Impact
    seasonal_colors = get_colors(seasonal, "cnt", "#D3D3D3", "#8BC43D")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=seasonal, x="season", y="cnt", palette=seasonal_colors)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(plt)

with tab2:
    # Weather Impact
    weather_colors = get_colors(weather, "cnt", "#D3D3D3", "#8BC43D")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=weather, x="weathersit", y="cnt", palette=weather_colors)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(plt)
