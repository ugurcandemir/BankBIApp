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

def run_common_size_analysis():
    st.subheader("📈 Yüzde Analizi")
    st.write("Yüzde (common-size) analizlerinin gösterileceği alan.")

def run_trend_analysis():
    st.subheader("📈 Trend Analizi")
    st.write("Trend analizlerinin gösterileceği alan.")

def run_ratio_analysis_dashboard():
    st.subheader("📈 Rasyo Analizi")
    st.write("Rasyo analizlerinin gösterileceği alan.")

def run_report_builder():
    st.subheader("📝 Raporum")
    st.write("Rapor oluşturma alanı.")

def run_customer_segmentation():
    st.subheader("💳 Müşteri Segmentasyonu")
    st.write("Segmentasyon analiz alanı.")

def run_credit_model_training():
    st.subheader("💳 Model Eğitimi")
    st.write("Kredi skorlama model eğitimi alanı.")

def run_score_prediction():
    st.subheader("💳 Skor Tahmini")
    st.write("Skor tahminlerinin gösterileceği alan.")

def run_fraud_detection():
    st.subheader("🚨 Fraud")
    st.write("Fraud (anomalili işlem) analizlerinin yapılacağı alan.")

def run_product_matcher():
    st.subheader("🎯 Ürün Bul")
    st.write("Ürün eşleştirme algoritmalarının uygulanacağı alan.")

def run_housing_valuation():
    st.subheader("🏘️ Konut Fiyatlama")
    st.write("Konut fiyat tahmin modellerinin gösterileceği alan.")

def run_akbilmis_ai_assistant():
    st.subheader("🤖 AK Bilmiş")
    st.write("Akbank için bilgi veren yapay zeka asistanı.")

def run_macro_dashboard():
    st.subheader("📉 Makro Bankam")
    st.write("Makro ekonomik göstergelerin analiz edileceği alan.")

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
    sub_tab = st.sidebar.radio("Alt Bölüm", [
        "Finansal Tablolar",
        "Pivot Tablolar",
        "Ham Veri"
    ])
    if sub_tab == "Finansal Tablolar":
        run_financial_tables()
    elif sub_tab == "Pivot Tablolar":
        run_pivot_tables()
    elif sub_tab == "Ham Veri":
        run_raw_data_tables()

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
    sub_tab = st.sidebar.radio("Alt Bölüm", [
        "Müşteri Segmentasyonu",
        "Model Eğitimi",
        "Skor Tahmini"
    ])
    if sub_tab == "Müşteri Segmentasyonu":
        run_customer_segmentation()
    elif sub_tab == "Model Eğitimi":
        run_credit_model_training()
    elif sub_tab == "Skor Tahmini":
        run_score_prediction()

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


