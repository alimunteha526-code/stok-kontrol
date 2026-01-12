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
    h1 { color: #333333; font-family: 'Arial Black', sans-serif; text-align: center; }
    .stButton>button { width: 100%; background-color: #333333 !important; color: white !important; font-weight: bold; border-radius: 10px !important; height: 3.5em; }
    .stDownloadButton>button { background-color: #007bff !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:bold; color:#666;'>Açık Kapora Takip Paneli</p>", unsafe_allow_html=True)

# Oturum durumunu (session state) başlat
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: EXCEL YÜKLEME ---
with st.expander("📁 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        
        # Sabit sütun isimleri
        sabit_isim = "Müşteri Adı"
        sabit_pers = "Personel No"
        
        # Sipariş No sütununu seçtir
        s_no_col = st.selectbox("Lütfen 'Sipariş No' sütununu seçin:", df_temp.columns)
        
        if sabit_isim in df_temp.columns and sabit_pers in df_temp.columns:
            db_df = df_temp[[s_no_col, sabit_isim, sabit_pers]].copy()
            db_df.columns = ['Sipariş No', 'Müşteri Adı', 'Personel No']
            
            # Veri temizleme
            db_df['Personel No'] = pd.to_numeric(db_df['Personel No'], errors='coerce').fillna(0).astype(int).astype(str)
            db_df['Sipariş No'] = db_df['Sipariş No'].astype(str).str.strip().str.upper()
            
            st.session_state.db = db_df
            st.success(f"✅ {len(st.session_state.db)} Kayıt Yüklendi.")
        else:
            st.error(f"⚠️ Hata: Excel'de '{sabit_isim}' ve '{sabit_pers}' bulunamadı.")

st.divider()

# --- 2. ADIM: BARKOD OKUTMA VE LİSTEDEN DÜŞME ---
if not st.session_state.db.empty:
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Barkodu Okutun")
        input_kod = st.text_input("", placeholder="Okutulan barkod listeden düşer...").strip().upper()
        submit = st.form_submit_button("KONTROL ET")

    if submit and input_kod:
        # Siparişin listede olup olmadığını kontrol et
        match = st.session_state.db[st.session_state.db['Sipariş No'] == input_kod]
        
        if not match.empty:
            if input_kod in st.session_state.okutulanlar:
                st.warning(f"⚠️ Bu sipariş zaten okutuldu: {input_kod}")
            else:
                isim = match['Müşteri Adı'].iloc[0]
                st.success(f"✅ BULUNDU: {isim} (Listeden düşüldü)")
                # Okutulanı küme içine ekle
                st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- 3. ADIM: KALAN (EKSİK) LİSTEYİ GÖSTER ---
st.divider()
# Kalan siparişleri hesapla (Okutulanları ana listeden çıkar)
kalan_df = st.session_state.db[~st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()

if not st.session_state.db.empty:
    st.markdown(f"### 📊 Kalan Sipariş Sayısı: {len(kalan_df)}")
    
    if st.button("📋 Kalan Listeyi Detaylı Gör"):
        if not kalan_df.empty:
            kalan_df.insert(0, 'Sıra No', range(1, len(kalan_df) + 1))
            st.dataframe(kalan_df, use_container_width=True, hide_index=True)
            
            # İndirme seçenekleri
            col_pdf, col_csv = st.columns(2)
            
            with col_pdf:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(190, 10, "KALAN SIPARIS LISTESI", ln=True, align='C')
                pdf.ln(5)
                pdf.set_font("Arial", size=10)
                pdf.cell(15, 8, "Sira", 1); pdf.cell(45, 8, "Siparis No", 1); pdf.cell(90, 8, "Musteri Adi", 1); pdf.cell(30, 8, "Pers. No", 1); pdf.ln()
                
                for i, r in kalan_df.iterrows():
                    isim_pdf = str(r['Müşteri Adı']).replace('İ','I').replace('ğ','g').replace('ü','u').replace('ş','s').replace('ö','o').replace('ç','c').replace('Ğ','G').replace('Ü','U').replace('Ş','S').replace('Ö','O').replace('Ç','C')
                    pdf.cell(15, 8, str(r['Sıra No']), 1)
                    pdf.cell(45, 8, str(r['Sipariş No']), 1)
                    pdf.cell(90, 8, isim_pdf[:40], 1)
                    pdf.cell(30, 8, str(r['Personel No']), 1)
                    pdf.ln()
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button("📄 PDF İndir", data=pdf_bytes, file_name="Kalan_Siparisler.pdf", mime="application/pdf")

            with col_csv:
                csv_data = kalan_df.to_csv(index=False, encoding='utf-8-sig', sep=';')
                st.download_button("📂 CVS İndir", data=csv_data, file_name="Kalan_Siparisler.csv", mime="text/csv")
        else:
            st.success("🎉 Tebrikler! Listedeki tüm siparişler okutuldu.")

if st.button("🔄 Tüm İşlemi Sıfırla"):
    st.session_state.okutulanlar = set()
    st.rerun()
