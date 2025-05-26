import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='dark')

# Load data
bikeday = pd.read_csv("bikeday.csv")
bikehour = pd.read_csv("bikehour.csv")

st.title("Dashboard Peminjaman Sepeda")
st.markdown("Menampilkan data peminjaman sepeda berdasarkan waktu dan musim.")

# Filter musim dari sidebar
season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season = st.sidebar.selectbox(
    "Pilih Musim", options=[0, 1, 2, 3, 4],
    format_func=lambda x: "Semua" if x == 0 else season_dict[x]
)

# Jika musim dipilih, maka akan filter datanya
if season != 0:
    bikeday = bikeday[bikeday["season"] == season]
    bikehour = bikehour[bikehour["season"] == season]

# Statistik dasar
st.subheader("Statistik Umum")
col1, col2 = st.columns(2)
col1.metric("Total Harian", f"{bikeday['cnt'].sum():,}")
col1.metric("Rata-rata per Hari", f"{bikeday['cnt'].mean():.2f}")
col2.metric("Total per Jam", f"{bikehour['cnt'].sum():,}")
col2.metric("Rata-rata per Jam", f"{bikehour['cnt'].mean():.2f}")

# Grafik per Jam
st.subheader("Rata-rata Peminjaman per Jam")
avg_hour = bikehour.groupby("hr")["cnt"].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(12, 4))
sns.barplot(data=avg_hour, x="hr", y="cnt", palette="viridis", ax=ax1)
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig1)

# Grafik Harian
st.subheader("Peminjaman Sepeda per Hari")
bikeday["dteday"] = pd.to_datetime(bikeday["dteday"])
fig2, ax2 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=bikeday, x="dteday", y="cnt", marker="o", color="blue", ax=ax2)
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig2)

# Boxplot Musiman
st.subheader("Distribusi Musiman")
fig3, ax3 = plt.subplots()
sns.boxplot(data=bikeday, x="season", y="cnt", palette="Set2", ax=ax3)
ax3.set_xticklabels([season_dict[i] for i in sorted(season_dict.keys())])
st.pyplot(fig3)

# Hari kerja vs libur
st.subheader("Hari Kerja vs Hari Libur")
labels = ["Hari Kerja", "Hari Libur"]
values = [
    bikeday[bikeday["workingday"] == 1]["cnt"].mean(),
    bikeday[bikeday["workingday"] == 0]["cnt"].mean()
]
fig4, ax4 = plt.subplots()
sns.barplot(x=labels, y=values, palette="pastel", ax=ax4)
st.pyplot(fig4)
