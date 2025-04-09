# We are creating a Streamlit application for Akbank's Bank Analysis Platform.
# Import necessary libraries.
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
import base64
import unicodedata
import os
from markdown2 import markdown
from bs4 import BeautifulSoup
import tempfile
import pydeck as pdk
import joblib


import streamlit as st
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder


import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder




import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


# Set the page title, layout and other configurations.

# Set page config
st.set_page_config(page_title="Akbank Banka Analiz Platformu", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .css-1d391kg {
            padding-top: 2rem;
        }
        .header-container {
            display: flex;
            align-items: center;
            background-color: #d50000;
            padding: 20px;
            color: white;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .header-container img {
            height: 60px;
            margin-right: 20px;
        }
        .header-text {
            font-size: 28px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Load local logo
logo = Image.open("akbank_logo.png")

# Header section with local image
col1, col2 = st.columns([1, 2.5])
with col1:
    st.image(logo, width=8000)
with col2:
    st.markdown(
        "<h1 style='color: red; margin-top: 20px;'>Banka Analiz Platformu</h1>",
        unsafe_allow_html=True
    )


# We are writing the functionality of the application in the main section.
# The logic of the application is divided into different sections, each with its own functionality.

# 🧩 Function Definitions (Stubs — fill in later)
def run_financial_tables():
    st.subheader("📊 Finansal Tablolar")
    st.write("Finansal tabloların gösterileceği alan.")

def run_pivot_tables():
    st.subheader("📊 Pivot Tablolar")
    st.write("Pivot tabloların gösterileceği alan.")

def run_raw_data_tables():
    st.subheader("📊 Ham Veri")
    st.write("Ham verilerin gösterileceği alan.")

def filtered_chart_section(df, key_prefix="chart"):
    st.markdown("### 📋 Tablo")
    df = df.copy()

    # Filter by year
    years = df["Yıllar"].unique()
    selected_years = st.multiselect("Yıllara Göre Filtrele", years, default=years, key=f"{key_prefix}_years")
    df = df[df["Yıllar"].isin(selected_years)]

    # Filter by columns (excluding Yıllar)
    all_columns = df.columns.drop("Yıllar")
    selected_columns = st.multiselect("Değişkenleri Seçin", all_columns, default=all_columns[:3], key=f"{key_prefix}_cols")
    filtered_df = df[["Yıllar"] + selected_columns]
    st.dataframe(filtered_df)

    # Chart builder with export
    chart_creator_with_export(filtered_df, key_prefix=key_prefix)


def chart_creator_with_export(df, key_prefix="chart"):
    st.markdown("---")
    st.markdown("### 📊 Görsel Oluştur")

    if f"{key_prefix}_charts" not in st.session_state:
        st.session_state[f"{key_prefix}_charts"] = []

    with st.form(key=f"{key_prefix}_form"):
        chart_type = st.selectbox("Grafik Türü Seçin", ["Çizgi (Line)", "Bar", "Alan (Area)", "Pasta (Pie)", "Dağılım (Scatter)"], key=f"{key_prefix}_chart_type")
        x_col = st.selectbox("X Eksen Kolonu", df.columns, index=0, key=f"{key_prefix}_x")
        y_col = st.selectbox("Y Eksen Kolonu", df.columns, index=1 if len(df.columns) > 1 else 0, key=f"{key_prefix}_y")
        add_chart = st.form_submit_button("Grafiği Ekle")

        if add_chart:
            st.session_state[f"{key_prefix}_charts"].append((chart_type, x_col, y_col))

    # Display and export charts
    for idx, (chart_type, x_col, y_col) in enumerate(st.session_state[f"{key_prefix}_charts"]):
        st.markdown(f"#### Grafik {idx+1}: {chart_type} ({x_col} vs {y_col})")
        try:
            if chart_type == "Çizgi (Line)":
                fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "Alan (Area)":
                fig = px.area(df, x=x_col, y=y_col)
            elif chart_type == "Pasta (Pie)":
                fig = px.pie(df, names=x_col, values=y_col)
            elif chart_type == "Dağılım (Scatter)":
                fig = px.scatter(df, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)

            if st.session_state.get("reports"):
                export_to = st.selectbox(f"Grafik {idx+1} için rapor seçin", list(st.session_state["reports"].keys()), key=f"{key_prefix}_export_{idx}")
                if st.button(f"Grafiği '{export_to}' raporuna aktar", key=f"{key_prefix}_export_btn_{idx}"):
                    st.session_state["reports"][export_to]["charts"].append(fig)
                    st.success(f"Görsel '{export_to}' raporuna eklendi.")
        except Exception as e:
            st.warning(f"Grafik çizilirken hata oluştu: {e}")

            
def run_common_size_analysis():
    st.subheader("📈 Yüzde Analizi")
    st.write("Yüzde (common-size) analizlerinin gösterileceği alan.")
    st.markdown("## 📊 Yüzde Yöntemi ile Analiz (Common-Size Analysis)")

    # Load both datasets
    df_bilanco = pd.read_excel("AKBNK_balance_2.xlsx", index_col=0)
    df_gelir = pd.read_excel("AKBNK_income_2.xlsx", index_col=0)
    if "Unnamed: 1" in df_gelir.columns:
        df_gelir = df_gelir.drop(columns=["Unnamed: 1"])

    # ----------- BİLANÇO ANALİZİ -----------
    st.markdown("### 📘 Bilanço")
    bilanco_columns = df_bilanco.columns.tolist()

    selected_cols_bilanco = st.multiselect(
        "Görüntülenecek Yıllar (Bilanço)",
        bilanco_columns,
        default=bilanco_columns,
        key="bilanco_years"
    )

    if selected_cols_bilanco:
        base_column_bilanco = st.selectbox(
            "Baz Alınacak Yıl (Bilanço)",
            selected_cols_bilanco,
            key="bilanco_base"
        )

        df_bilanco_view = df_bilanco[selected_cols_bilanco]
        df_bilanco_common = df_bilanco_view.divide(df_bilanco_view[base_column_bilanco], axis=0) * 100
        st.dataframe(df_bilanco_common.style.format("{:.2f} %"))

    st.markdown("---")

    # ----------- GELİR TABLOSU ANALİZİ -----------
    st.markdown("### 📙 Gelir Tablosu")
    gelir_columns = df_gelir.columns.tolist()

    selected_cols_gelir = st.multiselect(
        "Görüntülenecek Yıllar (Gelir Tablosu)",
        gelir_columns,
        default=gelir_columns,
        key="gelir_years"
    )

    if selected_cols_gelir:
        base_column_gelir = st.selectbox(
            "Baz Alınacak Yıl (Gelir Tablosu)",
            selected_cols_gelir,
            key="gelir_base"
        )

        df_gelir_view = df_gelir[selected_cols_gelir]
        df_gelir_common = df_gelir_view.divide(df_gelir_view[base_column_gelir], axis=0) * 100
        st.dataframe(df_gelir_common.style.format("{:.2f} %"))


def run_trend_analysis():
    st.subheader("📈 Trend Analizi")
    st.write("Trend analizlerinin gösterileceği alan.")
    st.markdown("## 📈 Trend Analizi (Yatay Yüzde Değişim)")

    # ---- BİLANÇO TREND ANALİZİ ----
    # Load balance sheet data (assumes first column is "Yıllar")
    df_bilanco = pd.read_excel("AKBNK_balance_2.xlsx")
    # Pivot: set "Yıllar" as index and then transpose so that rows = financial items, columns = years.
    df_bilanco_pivot = df_bilanco.set_index("Yıllar").T

    # Get the list of available years (now from the columns)
    bilanco_years = df_bilanco_pivot.columns.tolist()
    selected_bilanco_years = st.multiselect(
        "Görüntülenecek Yıllar (Bilanço)",
        bilanco_years,
        default=bilanco_years,
        key="trend_bilanco_years"
    )

    if selected_bilanco_years:
        base_year_bilanco = st.selectbox(
            "Baz Yıl (Bilanço)",
            selected_bilanco_years,
            key="trend_bilanco_base"
        )

        # Work on the selected columns
        df_bilanco_selected = df_bilanco_pivot[selected_bilanco_years].copy()
        df_bilanco_trend = df_bilanco_selected.copy()

        # For each financial item (row), compute the trend relative to the base year
        for idx in df_bilanco_trend.index:
            base_val = df_bilanco_selected.loc[idx, base_year_bilanco]
            if base_val != 0:
                df_bilanco_trend.loc[idx] = (df_bilanco_selected.loc[idx] / base_val) * 100
            else:
                df_bilanco_trend.loc[idx] = 0

        st.dataframe(df_bilanco_trend.style.format("{:.2f} %"))

    st.markdown("---")

    # ---- GELİR TABLOSU TREND ANALİZİ ----
    df_gelir = pd.read_excel("AKBNK_income_2.xlsx")
    # Drop unnecessary column if exists
    if "Unnamed: 1" in df_gelir.columns:
        df_gelir = df_gelir.drop(columns=["Unnamed: 1"])
    df_gelir_pivot = df_gelir.set_index("Yıllar").T

    gelir_years = df_gelir_pivot.columns.tolist()
    selected_gelir_years = st.multiselect(
        "Görüntülenecek Yıllar (Gelir Tablosu)",
        gelir_years,
        default=gelir_years,
        key="trend_gelir_years"
    )

    if selected_gelir_years:
        base_year_gelir = st.selectbox(
            "Baz Yıl (Gelir Tablosu)",
            selected_gelir_years,
            key="trend_gelir_base"
        )

        df_gelir_selected = df_gelir_pivot[selected_gelir_years].copy()
        df_gelir_trend = df_gelir_selected.copy()

        for idx in df_gelir_trend.index:
            base_val = df_gelir_selected.loc[idx, base_year_gelir]
            if base_val != 0:
                df_gelir_trend.loc[idx] = (df_gelir_selected.loc[idx] / base_val) * 100
            else:
                df_gelir_trend.loc[idx] = 0

        st.dataframe(df_gelir_trend.style.format("{:.2f} %"))



def run_ratio_analysis_dashboard():
    st.subheader("📈 Rasyo Analizi")
    st.write("Rasyo analizlerinin gösterileceği alan.")
    st.markdown("### 🔑 Finansal Rasyolar")

    
    # Read Excel files
    df = pd.read_excel("AKBNK_balance_2.xlsx")
    df2 = pd.read_excel("AKBNK_income_2.xlsx")

    # Clean column names by stripping whitespace
    df.columns = df.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Drop unnecessary column if exists
    if "Unnamed: 1" in df2.columns:
        df2 = df2.drop(columns=["Unnamed: 1"])

    # --- Compute ratios ---
    df["Faktoring/Maddi"] = df["Faktoring Alacakları"] / df["MADDİ DURAN VARLIKLAR (Net)"]
    df["Krediler/Finansal"] = df["KREDİLER (Net)"] / df["Finansal Varlıklar (Net)"]
    df["Nakit/Krediler"] = df["Nakit ve Nakit Benzerleri"] / df["KREDİLER (Net)"]

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    # --- KPI Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Faktoring / Maddi Duran Varlıklar",
        f"{latest['Faktoring/Maddi']:.2f}",
        f"{latest['Faktoring/Maddi'] - previous['Faktoring/Maddi']:+.2f}"
    )
    col2.metric(
        "Krediler / Finansal Varlıklar",
        f"{latest['Krediler/Finansal']:.2f}",
        f"{latest['Krediler/Finansal'] - previous['Krediler/Finansal']:+.2f}"
    )
    col3.metric(
        "Nakit / Krediler",
        f"{latest['Nakit/Krediler']:.2f}",
        f"{latest['Nakit/Krediler'] - previous['Nakit/Krediler']:+.2f}"
    )

    # --- Ratio Charts Side-by-Side ---
    st.markdown("### 📈 Zaman İçindeki Değişim")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(px.line(df, x="Yıllar", y="Faktoring/Maddi", title="Faktoring / Maddi Duran Varlıklar"), use_container_width=True)

    with chart_col2:
        st.plotly_chart(px.line(df, x="Yıllar", y="Krediler/Finansal", title="Krediler / Finansal Varlıklar"), use_container_width=True)

    st.plotly_chart(px.line(df, x="Yıllar", y="Nakit/Krediler", title="Nakit / Krediler"), use_container_width=True)

    # --- Data Table ---
    st.markdown("### 📊 Tüm Rasyo Verileri")
    st.dataframe(df[["Yıllar", "Faktoring/Maddi", "Krediler/Finansal", "Nakit/Krediler"]].style.format({
        "Faktoring/Maddi": "{:.2f}",
        "Krediler/Finansal": "{:.2f}",
        "Nakit/Krediler": "{:.2f}"
    }))

    
# 📝 Report builder module (modularized)
def run_report_builder():

    st.subheader("📝 Raporum")
    st.write("Rapor oluşturma alanı.")


    if "reports" not in st.session_state:
        st.session_state["reports"] = {}

    if "current_report" not in st.session_state:
        st.session_state["current_report"] = None

    # Create new report
    st.markdown("### 📄 Yeni Rapor Oluştur")
    new_report_name = st.text_input("Rapor Adı Girin", "")
    if st.button("Raporu Oluştur") and new_report_name:
        if new_report_name not in st.session_state["reports"]:
            st.session_state["reports"][new_report_name] = {
                "markdown": "",
                "charts": []
            }
            st.session_state["current_report"] = new_report_name

    report_names = list(st.session_state["reports"].keys())

    if report_names:
        selected = st.selectbox(
            "Rapor Seç", 
            report_names, 
            index=report_names.index(st.session_state["current_report"]) 
            if st.session_state["current_report"] in report_names 
            else 0
        )
        st.session_state["current_report"] = selected
        report = st.session_state["reports"][selected]

        st.markdown("### ✍️ Rapor İçeriği")
        report["markdown"] = st.text_area("Markdown İçeriği", value=report["markdown"], height=200)

        st.markdown("### 📊 Eklenmiş Grafikler")
        for i, fig in enumerate(report["charts"]):
            st.plotly_chart(fig, use_container_width=True)

        if st.button("PDF Olarak İndir"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            html = markdown(report["markdown"])
            soup = BeautifulSoup(html, "html.parser")

            for element in soup.find_all():
                if element.name == "h1":
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, element.text, ln=True)
                elif element.name == "h2":
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(0, 10, element.text, ln=True)
                elif element.name == "li":
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, f"- {element.text}", ln=True)
                elif element.name == "p":
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, element.text)
                pdf.ln(2)

            # Save charts as PNG images and insert
            with tempfile.TemporaryDirectory() as tmpdir:
                for i, fig in enumerate(report["charts"]):
                    image_path = os.path.join(tmpdir, f"chart_{i}.png")
                    try:
                        fig.update_layout(
                            template="plotly",
                            paper_bgcolor="white",
                            plot_bgcolor="white"
                        )
                        fig.write_image(image_path, format="png")
                        pdf.image(image_path, w=180)
                        pdf.ln(5)
                    except Exception as e:
                        st.warning(f"Grafik {i+1} PDF'e eklenemedi: {e}")

            pdf_output = pdf.output(dest="S").encode("latin-1")
            buffer = BytesIO(pdf_output)
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{selected}.pdf">📥 PDF\'i İndir</a>'
            st.markdown(href, unsafe_allow_html=True)

    else:
        st.info("Henüz oluşturulmuş bir rapor yok.")


def run_credit_model_training():
    st.subheader("💳 Model Eğitimi")
    st.write("Kredi skorlama model eğitimi alanı.")
    st.markdown("### 💳 Kredi Skorlama Formu")

    with st.form("credit_form"):
        col1, col2 = st.columns(2)
        with col1:
            yas = st.slider("Yaş", 18, 75, 35)
            gelir = st.number_input("Aylık Gelir (₺)", min_value=1000, value=10000, step=500)
            kredi_gecmisi = st.selectbox("Kredi Geçmişi", ["iyi", "orta", "kötü"])
            aktif_kredi_sayisi = st.slider("Aktif Kredi Sayısı", 0, 5, 1)
            kredi_kart_limit_toplam = st.number_input("Toplam Kredi Kartı Limiti (₺)", min_value=1000, value=20000)
        with col2:
            geciken_odeme_sayisi = st.slider("Son 1 Yıldaki Geciken Ödeme Sayısı", 0, 10, 0)
            ev_sahibi_mi = st.selectbox("Ev Sahibi misiniz?", ["Evet", "Hayır"])
            meslek_grubu = st.selectbox("Meslek Grubu", ["memur", "ozel_sektor", "serbest", "emekli"])
            egitim_durumu = st.selectbox("Eğitim Durumu", ["lise", "lisans", "yuksek_lisans", "doktora"])

        submitted = st.form_submit_button("Skorla")

    if submitted:
        try:
            model = joblib.load("kredi_skorlama_model.pkl")
        except Exception as e:
            st.error(f"Model yüklenemedi: {e}")
            return

        # Girdileri uygun formata getir
        input_dict = {
            "yas": yas,
            "gelir": gelir,
            "kredi_gecmisi": LabelEncoder().fit(["iyi", "orta", "kötü"]).transform([kredi_gecmisi])[0],
            "aktif_kredi_sayisi": aktif_kredi_sayisi,
            "kredi_kart_limit_toplam": kredi_kart_limit_toplam,
            "geciken_odeme_sayisi": geciken_odeme_sayisi,
            "ev_sahibi_mi": 1 if ev_sahibi_mi == "Evet" else 0,
            "meslek_grubu": LabelEncoder().fit(["memur", "ozel_sektor", "serbest", "emekli"]).transform([meslek_grubu])[0],
            "egitim_durumu": LabelEncoder().fit(["lise", "lisans", "yuksek_lisans", "doktora"]).transform([egitim_durumu])[0],
        }

        input_df = pd.DataFrame([input_dict])

        try:
            prediction = model.predict(input_df)[0]
            risk_map = {0: "🔴 Yüksek Risk", 1: "🟡 Orta Risk", 2: "🟢 Düşük Risk"}
            st.success(f"Tahmin Edilen Kredi Riski: **{risk_map[prediction]}**")
        except Exception as e:
            st.error(f"Tahmin sırasında hata oluştu: {e}")


def run_fraud_detection():
    st.subheader("🚨 Fraud")
    st.write("Fraud (anomalili işlem) analizlerinin yapılacağı alan.")
    st.markdown("### 🚨 Fraud (Dolandırıcılık) Tespiti")

    with st.form("fraud_form"):
        col1, col2 = st.columns(2)
        with col1:
            islem_tutari = st.number_input("İşlem Tutarı (₺)", min_value=1, value=1000)
            saat = st.slider("İşlem Saati", 0, 23, 14)
            islem_tipi = st.selectbox("İşlem Tipi", ["e_ticaret", "atm", "pos", "eft"])
            bir_gunde_islem_sayisi = st.slider("Aynı Gün İçinde Yapılan İşlem Sayısı", 1, 50, 3)
            aylik_ortalama_tutar = st.number_input("Aylık Ortalama İşlem Tutarı (₺)", min_value=0, value=5000)
        with col2:
            lokasyon_uyusmazligi = st.selectbox("Lokasyon Uyumsuzluğu", ["Hayır", "Evet"])
            cihaz_id_yeni_mi = st.selectbox("Yeni Cihaz mı?", ["Hayır", "Evet"])
            uzak_ulke_mi = st.selectbox("İşlem Yurt Dışından mı?", ["Hayır", "Evet"])
            vpn_kullanimi = st.selectbox("VPN Kullanılmış mı?", ["Hayır", "Evet"])

        submitted = st.form_submit_button("İşlemi Değerlendir")

    if submitted:
        try:
            model = joblib.load("fraud_detection_model.pkl")
        except Exception as e:
            st.error(f"Model yüklenemedi: {e}")
            return

        # Label encode işlemi türü
        islem_tipi_encoded = LabelEncoder().fit(["e_ticaret", "atm", "pos", "eft"]).transform([islem_tipi])[0]

        input_dict = {
            "islem_tutari": islem_tutari,
            "saat": saat,
            "islem_tipi": islem_tipi_encoded,
            "lokasyon_uyusmazligi": 1 if lokasyon_uyusmazligi == "Evet" else 0,
            "cihaz_id_yeni_mi": 1 if cihaz_id_yeni_mi == "Evet" else 0,
            "bir_gunde_islem_sayisi": bir_gunde_islem_sayisi,
            "aylik_ortalama_tutar": aylik_ortalama_tutar,
            "uzak_ulke_mi": 1 if uzak_ulke_mi == "Evet" else 0,
            "vpn_kullanimi": 1 if vpn_kullanimi == "Evet" else 0,
        }

        input_df = pd.DataFrame([input_dict])

        try:
            prediction = model.predict(input_df)[0]
            if prediction == 1:
                st.error("🚨 Bu işlem dolandırıcılık (fraud) olarak değerlendirilmiştir!")
            else:
                st.success("✅ Bu işlem normal görünmektedir.")
        except Exception as e:
            st.error(f"Tahmin sırasında hata oluştu: {e}")


def run_product_matcher():
    st.subheader("🎯 Ürün Bul")
    st.write("Ürün eşleştirme algoritmalarının uygulanacağı alan.")
    st.markdown("### 🎯 Banka Ürünü Önerme")

    with st.form("product_recommender_form"):
        col1, col2 = st.columns(2)
        with col1:
            yas = st.slider("Yaş", 18, 80, 35)
            gelir = st.number_input("Aylık Gelir (₺)", min_value=1000, value=10000, step=500)
            mevcut_urun_sayisi = st.slider("Mevcut Banka Ürün Sayısı", 0, 5, 1)
            yillik_islem_sayisi = st.slider("Yıllık İşlem Sayısı", 0, 100, 20)
        with col2:
            ortalama_bakiye = st.number_input("Ortalama Hesap Bakiyesi (₺)", min_value=0, value=50000)
            yatirim_tecrubesi = st.selectbox("Yatırım Tecrübesi", ["hic", "az", "orta", "ileri"])
            risk_toleransi = st.selectbox("Risk Toleransı", ["dusuk", "orta", "yuksek"])
            digital_kullanim_sikligi = st.slider("Haftalık Mobil Giriş Sayısı", 0, 20, 5)

        submitted = st.form_submit_button("Ürün Öner")

    if submitted:
        try:
            scaler, kmeans = joblib.load("urun_oneri_model.pkl")
        except Exception as e:
            st.error(f"Model yüklenemedi: {e}")
            return

        # Kategorikleri encode et
        yatirim_map = {"hic": 0, "az": 1, "orta": 2, "ileri": 3}
        risk_map = {"dusuk": 0, "orta": 1, "yuksek": 2}

        input_dict = {
            "yas": yas,
            "gelir": gelir,
            "mevcut_urun_sayisi": mevcut_urun_sayisi,
            "yillik_islem_sayisi": yillik_islem_sayisi,
            "ortalama_bakiye": ortalama_bakiye,
            "yatirim_tecrubesi": yatirim_map[yatirim_tecrubesi],
            "risk_toleransi": risk_map[risk_toleransi],
            "digital_kullanim_sikligi": digital_kullanim_sikligi,
        }

        input_df = pd.DataFrame([input_dict])

        try:
            input_scaled = scaler.transform(input_df)
            segment = kmeans.predict(input_scaled)[0]

            # Segmentlere göre önerilen ürünler
            urun_map = {
                0: "💳 Kredi",
                1: "📈 Fon Yatırımı",
                2: "🏦 Vadeli Mevduat"
            }
            st.success(f"Önerilen Banka Ürünü: **{urun_map.get(segment, 'Ürün Yok')}** (Segment {segment})")
        except Exception as e:
            st.error(f"Tahmin sırasında hata oluştu: {e}")


def run_housing_valuation():
    st.subheader("🏘️ Konut Fiyatlama")
    st.write("Konut fiyat tahmin modellerinin gösterileceği alan.")
    st.markdown("### 🏘️ Konut Fiyatlama Formu")

    with st.form("housing_form"):
        col1, col2 = st.columns(2)
        with col1:
            metrekare = st.slider("Metrekare", 30, 300, 90)
            oda_sayisi = st.selectbox("Oda Sayısı", ["1+0", "1+1", "2+1", "3+1", "4+1"])
            bina_yasi = st.slider("Bina Yaşı", 0, 40, 10)
            bulundugu_kat = st.slider("Bulunduğu Kat", 0, 20, 2)
            toplam_kat = st.slider("Toplam Kat Sayısı", 1, 25, 5)
        with col2:
            ilce = st.selectbox("İlçe", ["Beşiktaş", "Kadıköy", "Çankaya", "Atakum"])
            ulasim_yakinligi = st.slider("Ulaşım Yakınlığı (0-1)", 0.0, 1.0, 0.5, step=0.05)
            okul_saglik_skoru = st.slider("Okul ve Sağlık Yakınlığı (0-1)", 0.0, 1.0, 0.5, step=0.05)
            site_icinde_mi = st.selectbox("Site İçinde mi?", ["Evet", "Hayır"])

        submitted = st.form_submit_button("Değerle")

    if submitted:
        try:
            model = joblib.load("konut_fiyatlama_model.pkl")
        except Exception as e:
            st.error(f"Model yüklenemedi: {e}")
            return

        # Encode işlemleri
        oda_sayisi_encoder = LabelEncoder().fit(["1+0", "1+1", "2+1", "3+1", "4+1"])
        ilce_encoder = LabelEncoder().fit(["Beşiktaş", "Kadıköy", "Çankaya", "Atakum"])

        input_dict = {
            "metrekare": metrekare,
            "oda_sayisi": oda_sayisi_encoder.transform([oda_sayisi])[0],
            "bina_yasi": bina_yasi,
            "bulundugu_kat": bulundugu_kat,
            "toplam_kat": toplam_kat,
            "ilce": ilce_encoder.transform([ilce])[0],
            "ulasim_yakinligi": ulasim_yakinligi,
            "okul_saglik_skoru": okul_saglik_skoru,
            "site_icinde_mi": 1 if site_icinde_mi == "Evet" else 0,
        }

        input_df = pd.DataFrame([input_dict])

        try:
            prediction = model.predict(input_df)[0]
            st.success(f"🏷️ Tahmini Konut Değeri: **{int(prediction):,} TL**")
        except Exception as e:
            st.error(f"Tahmin sırasında hata oluştu: {e}")


def run_akbilmis_ai_assistant():
    st.subheader("🤖 AK Bilmiş")
    st.write("Akbank için bilgi veren yapay zeka asistanı.")

def run_macro_dashboard():
    st.subheader("📉 Makro Bankam")
    st.write("Makro ekonomik göstergelerin analiz edileceği alan.")


# And here we are creating the main structure of the application.
# The sidebar is used for navigation and the main area is used for displaying the content.
# We place the functions in the sidebar and call them based on the user's selection.

# 🟥 Sidebar — Full navigation with icons
st.sidebar.title("🔎 Navigasyon")
main_section = st.sidebar.radio("📂 Modül Seçin", [
    "📊 Tablolarım",
    "📈 Analizlerim",
    "📝 Raporum",
    "💳 Kredi Skorlama",
    "🚨 Fraud",
    "🎯 Ürün Bul",
    "🏘️ Konut Fiyatlama",
    "🤖 AK Bilmiş",
    "📉 Makro Bankam"
])

# 🟨 Modular Section Routing
if main_section == "📊 Tablolarım":

    sub_tab = st.sidebar.radio("Alt Sekmeler", ["Bilanço", "Gelir Tablosu"])
    st.markdown(f"#### {sub_tab}")

    if sub_tab == "Bilanço":
        df = pd.read_excel("AKBNK_balance_2.xlsx")
        filtered_chart_section(df, key_prefix="bilanco")

    elif sub_tab == "Gelir Tablosu":
        df = pd.read_excel("AKBNK_income_2.xlsx")
        if "Unnamed: 1" in df.columns:
            df = df.drop(columns=["Unnamed: 1"])
        filtered_chart_section(df, key_prefix="gelir")

elif main_section == "📈 Analizlerim":
    sub_tab = st.sidebar.radio("Alt Bölüm", [
        "Yüzde Analizi",
        "Trend",
        "Rasyo"
    ])
    if sub_tab == "Yüzde Analizi":
        run_common_size_analysis()
    elif sub_tab == "Trend":
        run_trend_analysis()
    elif sub_tab == "Rasyo":
        run_ratio_analysis_dashboard()

elif main_section == "📝 Raporum":
    run_report_builder()

elif main_section == "💳 Kredi Skorlama":
    run_credit_model_training()
    
elif main_section == "🚨 Fraud":
    run_fraud_detection()

elif main_section == "🎯 Ürün Bul":
    run_product_matcher()

elif main_section == "🏘️ Konut Fiyatlama":
    run_housing_valuation()

elif main_section == "🤖 AK Bilmiş":
    run_akbilmis_ai_assistant()

elif main_section == "📉 Makro Bankam":
    run_macro_dashboard()


