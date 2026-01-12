import streamlit as st
import pandas as pd
import io
from fpdf import FPDF

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Takip Paneli", layout="centered")

# --- ATASUN KURUMSAL TASARIM (CSS) ---
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
    h1 { color: #333333; font-family: 'Arial Black', sans-serif; text-align: center; margin-bottom: 0px; }
    .panel-header { text-align: center; color: #666; font-weight: bold; margin-bottom: 30px; }
    .stTextInput>div>div>input { border: 2px solid #FF671B !important; border-radius: 10px; height: 50px; font-size: 20px; }
    .stButton>button { width: 100%; background-color: #333333 !important; color: white !important; border-radius: 10px !important; height: 3.5em; font-weight: bold; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p class='panel-header'>Açık Kapora Takip Paneli</p>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: EXCEL YÜKLEME ---
with st.expander("📁 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        st.info("Sütunları Eşleştirin:")
        c1, c2, c3 = st.columns(3)
        s_no_col = c1.selectbox("Sipariş No", df_temp.columns)
        s_isim_col = c2.selectbox("Müşteri İsim", df_temp.columns)
        s_pers_col = c3.selectbox("Personel No", df_temp.columns)
        
        db_df = df_temp[[s_no_col, s_isim_col, s_pers_col]].copy()
        db_df.columns = ['Sipariş No', 'Müşteri Adı', 'Personel No']
        db_df['Personel No'] = pd.to_numeric(db_df['Personel No'], errors='coerce').fillna(0).astype(int).astype(str)
        db_df['Sipariş No'] = db_df['Sipariş No'].astype(str).str.strip().str.upper()
        
        st.session_state.db = db_df
        st.success(f"✅ {len(st.session_state.db)} Sipariş Yüklendi.")

st.divider()

# --- 2. ADIM: CANLI OKUTMA ---
if not st.session_state.db.empty:
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Sipariş Numarasını Okutun")
        input_kod = st.text_input("", placeholder="Barkodu okutun...").strip().upper()
        submit = st.form_submit_button("SORGULA")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['Sipariş No'] == input_kod]
        if not match.empty:
            isim = match['Müşteri Adı'].iloc[0]
            p_no = match['Personel No'].iloc[0]
            st.success(f"✅ LİSTEDE VAR \n\n **Müşteri:** {isim} | **Personel:** {p_no}")
            st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- PDF OLUŞTURMA FONKSİYONU ---
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    # Standart bir font kullanıyoruz (PDF'de Türkçe karakter için en güvenli yol latin-1 uyumlu karakterlerdir)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt="EKSİK SİPARİŞ LİSTESİ", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    
    # Başlıklar
    pdf.cell(15, 10, "Sıra", 1)
    pdf.cell(45, 10, "Sipariş No", 1)
    pdf.cell(80, 10, "Müşteri Adı", 1)
    pdf.cell(40, 10, "Personel No", 1)
    pdf.ln()
    
    for index, row in df.iterrows():
        pdf.cell(15, 10, str(row['Sıra No']), 1)
        pdf.cell(45, 10, str(row['Sipariş No']), 1)
        # Türkçe karakterleri PDF uyumlu hale getirmek için basit bir temizlik
        isim_temiz = str(row['Müşteri Adı']).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(80, 10, isim_temiz, 1)
        pdf.cell(40, 10, str(row['Personel No']), 1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. ADIM: RAPORLAMA VE İNDİRME ---
st.divider()
if st.button("📊 Eksikleri Listele"):
    eksik_df = st.session_state.db[~st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()
    
    if not eksik_df.empty:
        eksik_df.insert(0, 'Sıra No', range(1, len(eksik_df) + 1))
        st.markdown("## 📋 EKSİK SİPARİŞ LİSTESİ")
        st.dataframe(eksik_df, use_container_width=True, hide_index=True)
        
        st.markdown("### 📥 İndirme Seçenekleri")
        d_col1, d_col2 = st.columns(2)
        
        with d_col1:
            pdf_output = create_pdf(eksik_df)
            st.download_button(
                label="📄 PDF Olarak İndir",
                data=pdf_output,
                file_name="Eksik_Siparis_Listesi.pdf",
                mime="application/pdf"
            )
            
        with d_col2:
            csv_data = eksik_df.to_csv(index=False, encoding='utf-8-sig', sep=';')
            st.download_button(
                label="CVS (.csv) Olarak İndir",
                data=csv_data,
                file_name="Eksik_Siparis_Listesi.csv",
                mime="text/csv"
            )
    else:
        st.success("Tebrikler! Eksik sipariş bulunmuyor.")

if st.button("🔄 Paneli Sıfırla"):
    st.session_state.okutulanlar = set()
    st.rerun()
