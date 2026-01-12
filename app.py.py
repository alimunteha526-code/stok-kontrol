import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Atasun Optik - Açık Kapora", layout="centered")

# Başlık ve Görsel Arayüz
st.title("👓 Atasun Optik")
st.subheader("Açık Kapora / Sipariş Kontrol Sistemi")
st.info("Lütfen önce merkezden gelen 'Açık Kapora' listesini Excel olarak yükleyin.")

# Hafıza Yönetimi (Okutulanları kaybetmemek için)
if 'siparis_havuzu' not in st.session_state:
    st.session_state.siparis_havuzu = set()
    st.session_state.okutulan_siparisler = []

# 1. Adım: Excel Yükleme
yuklenen_dosya = st.file_uploader("Açık Kapora Listesini Seçin", type=['xlsx'])

if yuklenen_dosya:
    try:
        df = pd.read_excel(yuklenen_dosya)
        # Sipariş numaralarının ilk sütunda olduğunu varsayıyoruz
        st.session_state.siparis_havuzu = set(df.iloc[:, 0].astype(str).str.strip().str.upper())
        st.success(f"✅ Liste Yüklendi: {len(st.session_state.siparis_havuzu)} adet bekleyen sipariş bulundu.")
    except Exception as e:
        st.error(f"Excel okunurken hata oluştu: {e}")

# 2. Adım: Canlı Kontrol Alanı
if len(st.session_state.siparis_havuzu) > 0:
    st.divider()
    st.markdown("### 📲 Sipariş Numarasını Okutun")
    
    # Sipariş No Girişi
    siparis_no = st
