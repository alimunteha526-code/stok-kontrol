import streamlit as st
import pandas as pd

st.set_page_config(page_title="Atasun Optik - Açık Kapora", layout="centered")

st.title("👓 Atasun Optik")
st.subheader("Açık Kapora / Sipariş Kontrol Sistemi")

if 'siparis_havuzu' not in st.session_state:
    st.session_state.siparis_havuzu = set()
    st.session_state.okutulan_siparisler = []

yuklenen_dosya = st.file_uploader("Açık Kapora Listesini Seçin", type=['xlsx'])

if yuklenen_dosya:
    df = pd.read_excel(yuklenen_dosya)
    # İlk sütunu sipariş numarası al ve temizle
    st.session_state.siparis_havuzu = set(df.iloc[:, 0].astype(str).str.strip().str.upper())
    st.success(f"✅ {len(st.session_state.siparis_havuzu)} adet sipariş yüklendi.")

st.divider()

# OKUTMA FORMU: Bu kısım okutma yapınca kutuyu otomatik temizler
with st.form(key='barkod_form', clear_on_submit=True):
    siparis_no = st.text_input("Sipariş Numarasını Okutun", placeholder="Barkodu buraya okutun...").strip().upper()
    submit_button = st.form_submit_button(label='Kontrol Et')

# Form gönderildiğinde veya Enter'a basıldığında çalışır
if submit_button and siparis_no:
    if siparis_no in st.session_state.siparis_havuzu:
        st.balloons() # Görsel bir başarı efekti
        st.success(f"✅ DOĞRU: {siparis_no} listede var.")
        if siparis_no not in st.session_state.okutulan_siparisler:
            st.session_state.okutulan_siparisler.append(siparis_no)
    else:
        st.error(f"❌ UYARI: {siparis_no} LİSTEDE YOK!")

# RAPORLAMA
st.divider()
if st.button("Sayımı Bitir ve Eksikleri Göster"):
    okutulan_set = set(st.session_state.okutulan_siparisler)
    eksikler = list(st.session_state.siparis_havuzu - okutulan_set)
    
    st.warning(f"Eksik Sipariş Sayısı: {len(eksikler)}")
    st.dataframe(pd.DataFrame(eksikler, columns=["Eksik Sipariş No"]), use_container_width=True)

if st.button("Sıfırla"):
    st.session_state.okutulan_siparisler = []
    st.rerun()
