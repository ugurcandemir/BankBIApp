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

def run_common_size_analysis():
    st.subheader("📈 Yüzde Analizi")
    st.write("Yüzde (common-size) analizlerinin gösterileceği alan.")

def run_trend_analysis():
    st.subheader("📈 Trend Analizi")
    st.write("Trend analizlerinin gösterileceği alan.")

def run_ratio_analysis_dashboard():
    st.subheader("📈 Rasyo Analizi")
    st.write("Rasyo analizlerinin gösterileceği alan.")
    
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


