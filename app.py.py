import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Atasun Optik - Açık Kapora", layout="centered")

# Başlıklar
st.title("👓 Atasun Optik")
st.subheader("Açık Kapora / Sipariş Kontrol Sistemi")

# Hafıza Yönetimi
if 'siparis_havuzu' not in st.session_state:
    st.session_state.siparis_havuzu = set()
    st.session_state.okutulan_siparisler = []

# 1. Adım: Liste Yükleme
yuklenen_dosya = st.file_uploader("Açık Kapora Listesini Seçin (Excel)", type=['xlsx'])

if yuklenen_dosya:
    try:
        df = pd.read_excel(yuklenen_dosya)
        # Sipariş numaralarının ilk sütunda olduğunu varsayıyoruz
        st.session_state.siparis_havuzu = set(df.iloc[:, 0].astype(str).str.strip().str.upper())
        st.success(f"✅ Liste Yüklendi: {len(st.session_state.siparis_havuzu)} adet bekleyen sipariş bulundu.")
    except Exception as e:
        st.error(f"Excel okunurken hata oluştu: {e}")

st.divider()

# 2. Adım: Okutma Formu (Balon efekti kaldırıldı)
with st.form(key='barkod_form', clear_on_submit=True):
    st.markdown("### 📲 Sipariş Numarasını Okutun")
    siparis_no = st.text_input("Giriş Yapın", placeholder="Barkodu buraya okutun...").strip().upper()
    submit_button = st.form_submit_button(label='Kontrol Et')

# Form gönderildiğinde (Enter veya Buton)
if submit_button and siparis_no:
    if siparis_no in st.session_state.siparis_havuzu:
        st.success(f"✅ DOĞRU: {siparis_no} numaralı sipariş listede var.")
        if siparis_no not in st.session_state.okutulan_siparisler:
            st.session_state.okutulan_siparisler.append(siparis_no)
    else:
        st.error(f"❌ HATA: {siparis_no} LİSTEDE BULUNAMADI!")

# 3. Adım: Raporlama ve Özet
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("Sayımı Bitir ve Eksikleri Göster"):
        okutulan_set = set(st.session_state.okutulan_siparisler)
        eksikler = list(st.session_state.siparis_havuzu - okutulan_set)
        
        if eksikler:
            st.warning(f"Sayılamayan / Eksik Sipariş: {len(eksikler)}")
            st.dataframe(pd.DataFrame(eksikler, columns=["Eksik Sipariş No"]), use_container_width=True)
        else:
            st.success("Tüm siparişler tamamlandı!")

with col2:
    if st.button("Sistemi Sıfırla"):
        st.session_state.okutulan_siparisler = []
        st.rerun()
