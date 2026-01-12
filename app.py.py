import streamlit as st
import pandas as pd
import io
from fpdf import FPDF

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Atasun Optik - Takip Paneli", layout="centered")

# --- ATASUN TURUNCU TEMA (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FF671B; }
    .block-container {
        background-color: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 2rem;
    }
    h1 { color: #333333; font-family: 'Arial Black', sans-serif; text-align: center; }
    .stButton>button { width: 100%; background-color: #333333 !important; color: white !important; font-weight: bold; border-radius: 10px !important; height: 3.5em; }
    /* İndirme butonlarını belirginleştir */
    .stDownloadButton>button { background-color: #007bff !important; color: white !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:bold; color:#666;'>Açık Kapora Takip Paneli</p>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: LİSTE YÜKLEME ---
with st.expander("📁 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        c1, c2, c3 = st.columns(3)
        s_no_col = c1.selectbox("Sipariş No", df_temp.columns)
        s_isim_col = c2.selectbox("Müşteri İsim", df_temp.columns)
        s_pers_col = c3.selectbox("Personel No", df_temp.columns)
        
        db_df = df_temp[[s_no_col, s_isim_col, s_pers_col]].copy()
        db_df.columns = ['Sipariş No', 'Müşteri Adı', 'Personel No']
        db_df['Personel No'] = pd.to_numeric(db_df['Personel No'], errors='coerce').fillna(0).astype(int).astype(str)
        db_df['Sipariş No'] = db_df['Sipariş No'].astype(str).str.strip().str.upper()
        st.session_state.db = db_df
        st.success(f"✅ {len(st.session_state.db)} Kayıt Yüklendi.")

st.divider()

# --- 2. ADIM: BARKOD OKUTMA ---
if not st.session_state.db.empty:
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Barkodu Okutun")
        input_kod = st.text_input("", placeholder="Barkodu buraya vurun...").strip().upper()
        submit = st.form_submit_button("SORGULA")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['Sipariş No'] == input_kod]
        if not match.empty:
            isim = match['Müşteri Adı'].iloc[0]
            st.success(f"✅ DOĞRU: {isim}")
            st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- 3. ADIM: RAPORLAMA VE İNDİRME SEÇENEKLERİ ---
st.divider()

# Bu buton eksikleri hesaplar ve indirme butonlarını tetikler
if st.button("📊 Eksikleri Listele ve İndirme Butonlarını Aç"):
    eksik_df = st.session_state.db[~st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()
    
    if not eksik_df.empty:
        eksik_df.insert(0, 'Sıra No', range(1, len(eksik_df) + 1))
        st.markdown("### 📋 EKSİK SİPARİŞ LİSTESİ")
        st.dataframe(eksik_df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.markdown("#### ⬇️ Dosyayı Aşağıdan İndirin")
        
        col_pdf, col_csv = st.columns(2)
        
        # --- PDF OLUŞTURMA ---
        with col_pdf:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(190, 10, "EKSİK SİPARİŞ LİSTESİ", ln=True, align='C')
                pdf.ln(5)
                pdf.set_font("Arial", size=10)
                # Tablo Başlıkları
                pdf.cell(15, 8, "Sira", 1)
                pdf.cell(45, 8, "Siparis No", 1)
                pdf.cell(90, 8, "Musteri Adi", 1)
                pdf.cell(40, 8, "Pers. No", 1)
                pdf.ln()
                # Veriler
                for i, r in eksik_df.iterrows():
                    pdf.cell(15, 8, str(r['Sıra No']), 1)
                    pdf.cell(45, 8, str(r['Sipariş No']), 1)
                    pdf.cell(90, 8, str(r['Müşteri Adı'])[:40], 1)
                    pdf.cell(40, 8, str(r['Personel No']), 1)
                    pdf.ln()
                
                pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
                st.download_button("📄 PDF İndir", data=pdf_output, file_name="Eksik_Siparisler.pdf", mime="application/pdf")
            except:
                st.error("PDF oluşturulurken bir hata oluştu.")

        # --- CSV OLUŞTURMA ---
        with col_csv:
            csv_data = eksik_df.to_csv(index=False, encoding='utf-8-sig', sep=';')
            st.download_button("📂 CVS İndir", data=csv_data, file_name="Eksik_Siparisler.csv", mime="text/csv")
            
    else:
        st.success("Tüm siparişler tamamlanmış!")

if st.button("🔄 Sıfırla"):
    st.session_state.okutulanlar = set()
    st.rerun()
