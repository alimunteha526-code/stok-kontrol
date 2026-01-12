import streamlit as st
import pandas as pd

# Sayfa Ayarları (Sekme başlığı)
st.set_page_config(page_title="Atasun Açık Kapora", layout="centered")

# Başlık Özelleştirme
st.title("🔍 Atasun Açık Kapora Programı")
st.write("Ana sipariş listenizi yükleyin ve gelen sipariş numaralarını anlık kontrol edin.")

# 1. Aşama: Hafıza Yönetimi
if 'ana_liste' not in st.session_state:
    st.session_state.ana_liste = set()
    st.session_state.okutulanlar = []

# Dosya Yükleme Alanı
uploaded_file = st.file_uploader("Önce Ana Sipariş Listesini (Excel) Yükleyin", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # İlk sütunu sipariş numarası kabul ediyoruz
    st.session_state.ana_liste = set(df.iloc[:, 0].astype(str).str.strip().str.upper())
    st.success(f"Sistem hazır! {len(st.session_state.ana_liste)} adet sipariş numarası yüklendi.")

# 2. Aşama: Canlı Sipariş Numarası Girişi
if len(st.session_state.ana_liste) > 0:
    st.divider()
    
    # Kullanıcıdan sipariş numarası alma
    yeni_no = st.text_input("Sipariş Numarasını Okutun ve Enter'a Basın", key="siparis_giris").strip().upper()

    if yeni_no:
        if yeni_no in st.session_state.ana_liste:
            st.success(f"✅ {yeni_no} - SİPARİŞ LİSTEDE MEVCUT")
            if yeni_no not in st.session_state.okutulanlar:
                st.session_state.okutulanlar.append(yeni_no)
        else:
            st.error(f"⚠️ UYARI: {yeni_no} - BU NUMARA LİSTEDE YOK!")
            # İstersen listede olmayanları da takibe alabilirsin:
            if yeni_no not in st.session_state.okutulanlar:
                st.session_state.okutulanlar.append(yeni_no)

    # 3. Aşama: Raporlama
    st.divider()
    if st.button("Kontrolü Bitir ve Eksik Siparişleri Listele"):
        okutulan_set = set(st.session_state.okutulanlar)
        eksikler = list(st.session_state.ana_liste - okutulan_set)
        
        st.subheader("📊 Kontrol Özeti")
        st.write(f"Toplam Beklenen Sipariş: {len(st.session_state.ana_liste)}")
        st.write(f"Okutulan Doğru Sipariş: {len(okutulan_set & st.session_state.ana_liste)}")
        
        if eksikler:
            st.error(f"Henüz Gelmeyen (Eksik) Sipariş Sayısı: {len(eksikler)}")
            st.dataframe(pd.DataFrame(eksikler, columns=["Eksik Sipariş Numaraları"]))
        else:
            st.balloons()
            st.success("Harika! Tüm siparişler tamamlandı.")
