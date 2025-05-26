import pandas as pd
import matplotlib.pyplot as plt                      
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#Load data
bikeday = pd.read_csv('bikeday.csv')
bikehour = pd.read_csv('bikehour.csv')

st.title('Bike Share Dashboard')
st.markdown('This dashboard provides insights into bike share usage patterns.')

# Sidebar filters
st.sidebar.header('Filters')
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

season= st.sidebar.selectbox(
    'Select Season',
    options=[0, 1, 2, 3, 4], format_func=lambda x: "Semua" if x == 0 else season_map[x])

# Filter data musiman jika dipilih
if season != 0:
    bikeday = bikeday[bikeday['season'] == season]
    bikehour = bikehour[bikehour['season'] == season]
    
# Statistik umum
total_rides = bikeday['cnt'].sum()
total_hours = bikehour['cnt'].sum()
avg_per_day = bikeday['cnt'].mean()
avg_per_hour = bikehour['cnt'].mean()

col1, col2 = st.columns(2)
col1.metric("Total peminjaman harian", f"{total_rides:,}")
col1.metric("Rata-rata per Hari", f"{avg_per_day:.2f}")
col2.metric("Total peminjaman per Jam", f"{total_hours:,}")
col2.metric("Rata-rata per Jam", f"{avg_per_hour:.2f}")

# Grafik Harian
st.subheader('Grafik Peminjaman Harian')
fig1, ax1 = plt.subplots(figsize=(12,4))
bikeday['dteday'] = pd.to_datetime(bikeday['dteday'])
sns.lineplot(data=bikeday, x='dteday', y='cnt', ax=ax1, marker='o', color='blue')
ax1.set_xlabel('Tanggal')
ax1.set_ylabel('Jumlah Peminjaman')
fig1.autofmt_xdate()
st.pyplot(fig1)

# Grafik Jam
st.subheader('Grafik Peminjaman per Jam')
fig2, ax2 = plt.subplots(figsize=(12,4))
avg_hour = bikehour.groupby('hr')['cnt'].mean().reset_index()
sns.barplot(data=avg_hour, x='hr', y='cnt', ax=ax2, palette='viridis')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Rata-rata Peminjaman')
st.pyplot(fig2)

#Visualisasi Musiman
st.subheader('Peminjaman Musiman')
fig3, ax3 = plt.subplots()
sns.boxplot(data=bikeday, x='season', y='cnt', ax=ax3, palette='Set2')
ax3.set_xticklabels([season_map[i] for i in sorted(season_map.keys())])
st.pyplot(fig3)

# Hari kerja vs libur
st.subheader("Hari kerja vs Hari libur")
labels = ['Hari kerja', 'Hari libur']
values = [bikeday[bikeday['workingday'] == 1]['cnt'].mean(), bikeday[bikeday['workingday'] == 0]['cnt'].mean()]
fig4, ax4 = plt.subplots()
sns.barplot(x=labels, y=values, ax=ax4, palette='pastel')
st.pyplot(fig4)