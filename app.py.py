import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Canlı Barkod Kontrol", layout="centered")
st.title("🔍 Canlı Ürün Kontrol Sistemi")

# 1. Aşama: Ana Listeyi Yükleme
if 'ana_liste' not in st.session_state:
    st.session_state.ana_liste = set()
    st.session_state.okutulanlar = []

uploaded_file = st.file_uploader("Önce Ana Listeyi (Excel) Yükleyin", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # İlk sütunu ürün kodu kabul ediyoruz
    st.session_state.ana_liste = set(df.iloc[:, 0].astype(str).str.strip().str.upper())
    st.success(f"Sistem hazır! {len(st.session_state.ana_liste)} ürün yüklendi.")

# 2. Aşama: Canlı Okutma Alanı
if len(st.session_state.ana_liste) > 0:
    st.divider()
    
    # Kullanıcıdan giriş alma
    yeni_kod = st.text_input("Ürün Kodunu Okutun ve Enter'a Basın", key="barkod_giris").strip().upper()

    if yeni_kod:
        if yeni_kod in st.session_state.ana_liste:
            st.success(f"✅ {yeni_kod} - STOKTA VAR")
            if yeni_kod not in st.session_state.okutulanlar:
                st.session_state.okutulanlar.append(yeni_kod)
        else:
            st.error(f"⚠️ UYARI: {yeni_kod} - LİSTEDE YOK (FAZLA ÜRÜN!)")
            if yeni_kod not in st.session_state.okutulanlar:
                st.session_state.okutulanlar.append(yeni_kod)

    # 3. Aşama: Sonuçları Raporlama
    st.divider()
    if st.button("Sayımı Bitir ve Eksikleri Listele"):
        okutulan_set = set(st.session_state.okutulanlar)
        eksikler = list(st.session_state.ana_liste - okutulan_set)
        
        st.subheader("📊 Sayım Özeti")
        st.write(f"Toplam Olması Gereken: {len(st.session_state.ana_liste)}")
        st.write(f"Okutulan Doğru Ürün: {len(okutulan_set & st.session_state.ana_liste)}")
        
        if eksikler:
            st.error(f"Eksik Ürün Sayısı: {len(eksikler)}")
            st.dataframe(pd.DataFrame(eksikler, columns=["Eksik Ürün Kodları"]))
        else:
            st.balloons()
            st.success("Tebrikler! Hiç eksik ürün yok.")