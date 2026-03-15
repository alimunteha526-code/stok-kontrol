import streamlit as st

# Sayfa tasarımı
st.set_page_config(page_title="Ters Yüzde ve Fark Hesaplayıcı", layout="centered")

# Başlık ve açıklama
st.title("🧮 Gelişmiş %5,80 Hesaplama")
st.write("Verilen sayının %5,80 olduğu ana rakamı bulur ve aradaki farkı hesaplar.")

# Kullanıcı Girişi
input_val = st.number_input("Elinizdeki sayıyı giriniz:", min_value=0.0, step=0.01, format="%.2f")

if st.button("Hesaplamayı Başlat"):
    if input_val > 0:
        # 1. Adım: Ana rakamı bul (%5,80'den geri git)
        ana_rakam = input_val / 0.058
        
        # 2. Adım: Ana rakamdan girdi değerini çıkar
        fark = ana_rakam - input_val
        
        # Sonuçları yan yana sütunlarda gösterelim
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Girdiğiniz Sayı", f"{input_val:,.2f}")
        
        with col2:
            st.metric("Bulunan Ana Rakam", f"{ana_rakam:,.2f}")
            
        with col3:
            st.metric("Aradaki Fark", f"{fark:,.2f}", delta_color="normal")

        # Detaylı özet alanı
        st.markdown("---")
        st.info(f"**İşlem Özeti:**")
        st.write(f"- {ana_rakam:,.2f} sayısının %5,80'i: **{input_val:,.2f}**")
        st.write(f"- Ana rakamdan girdi çıkarıldığında kalan: **{fark:,.2f}**")
        
    else:
        st.warning("Lütfen 0'dan büyük bir değer girerek işleme devam edin.")

# Alt bilgi
st.caption("Veri doğrulama: (Girdi / 0.058) - Girdi")
