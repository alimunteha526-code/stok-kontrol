import streamlit as st
import pandas as pd
import io
from fpdf import FPDF

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Takip Paneli", layout="wide")

# --- ATASUN KURUMSAL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FF671B; }
    .block-container {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 1rem;
    }
    h1, h2, h3 { color: #333333; font-family: 'Arial Black', sans-serif; text-align: center; }
    .stButton>button { width: 100%; background-color: #333333 !important; color: white !important; font-weight: bold; border-radius: 10px !important; }
    .stDownloadButton>button { background-color: #007bff !important; color: white !important; border-radius: 10px !important; }
    .status-box { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: EXCEL YÜKLEME ---
with st.expander("📁 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        sabit_isim = "Müşteri Adı"
        sabit_pers = "Personel No"
        s_no_col = st.selectbox("Sipariş No Sütununu Seçin:", df_temp.columns)
        
        if sabit_isim in df_temp.columns and sabit_pers in df_temp.columns:
            db_df = df_temp[[s_no_col, sabit_isim, sabit_pers]].copy()
            db_df.columns = ['Sipariş No', 'Müşteri Adı', 'Personel No']
            db_df['Personel No'] = pd.to_numeric(db_df['Personel No'], errors='coerce').fillna(0).astype(int).astype(str)
            db_df['Sipariş No'] = db_df['Sipariş No'].astype(str).str.strip().str.upper()
            st.session_state.db = db_df
            st.success(f"✅ {len(st.session_state.db)} Kayıt Yüklendi.")

st.divider()

# --- 2. ADIM: BARKOD OKUTMA ---
if not st.session_state.db.empty:
    col_input, col_stats = st.columns([2, 1])
    
    with col_input:
        with st.form(key='barkod_form', clear_on_submit=True):
            input_kod = st.text_input("Sipariş No Okutun:", placeholder="Barkodu vurduğunuzda listeden düşer...").strip().upper()
            submit = st.form_submit_button("OKUT")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['Sipariş No'] == input_kod]
        if not match.empty:
            if input_kod in st.session_state.okutulanlar:
                st.warning(f"⚠️ Zaten okutuldu: {input_kod}")
            else:
                st.session_state.okutulanlar.add(input_kod)
                st.toast(f"✅ {input_kod} Listeden düştü!", icon='👓')
                st.rerun()
        else:
            st.error(f"❌ Listede yok: {input_kod}")

    # --- 3. ADIM: CANLI LİSTELER ---
    kalan_df = st.session_state.db[~st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()
    tamamlanan_df = st.session_state.db[st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()

    with col_stats:
        st.markdown(f"<div class='status-box' style='background-color:#dc3545;'>KALAN: {len(kalan_df)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='status-box' style='background-color:#28a745;'>TAMAM: {len(tamamlanan_df)}</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 KALAN SİPARİŞLER (EKSİKLER)", "✅ TAMAMLANANLAR"])

    with tab1:
        if not kalan_df.empty:
            st.dataframe(kalan_df, use_container_width=True, hide_index=True)
            # İndirme Butonları
            c1, c2 = st.columns(2)
            csv_data = kalan_df.to_csv(index=False, encoding='utf-8-sig', sep=';')
            c1.download_button("📂 Eksikleri CVS İndir", data=csv_data, file_name="Eksik_Siparisler.csv")
            
            # PDF Hazırlama
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14); pdf.cell(190, 10, "EKSIK SIPARISLER", ln=True, align='C'); pdf.set_font("Arial", size=10); pdf.ln(5)
            for i, r in kalan_df.iterrows():
                isim = str(r['Müşteri Adı']).replace('İ','I').replace('ğ','g').replace('ü','u').replace('ş','s').replace('ö','o').replace('ç','c')
                pdf.cell(45, 8, str(r['Sipariş No']), 1); pdf.cell(90, 8, isim[:40], 1); pdf.cell(40, 8, str(r['Personel No']), 1); pdf.ln()
            c2.download_button("📄 Eksikleri PDF İndir", data=pdf.output(dest='S').encode('latin-1'), file_name="Eksik_Siparisler.pdf")
        else:
            st.success("🎉 Harika! Tüm liste tamamlandı.")

    with tab2:
        if not tamamlanan_df.empty:
            st.dataframe(tamamlanan_df, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz okutulan sipariş yok.")

if st.button("🔄 Paneli Sıfırla"):
    st.session_state.okutulanlar = set()
    st.session_state.db = pd.DataFrame()
    st.rerun()
