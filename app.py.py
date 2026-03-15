import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Özel Hesaplama", layout="centered")

st.title("🧮 Güncellenmiş Hesaplama Modülü")
st.write("Ana rakamı bulur, ikinci değerden çıkarır ve ikiye böler.")

# Giriş alanları
col1, col2 = st.columns(2)

with col1:
    sayi_1 = st.number_input("5,80'in kaynağı olan sayı:", min_value=0.0, step=0.01, format="%.2f")

with col2:
    sayi_2 = st.number_input("İşlem yapılacak (çıkartılacak) rakam:", min_value=0.0, step=0.01, format="%.2f")

if st.button("Hesapla"):
    if sayi_1 > 0:
        # 1. Aşama: %5,80'den ana rakama ulaş
        ana_rakam = sayi_1 / 0.058
        
        # 2. Aşama: Yeni rakamdan ana rakamı çıkar ve ikiye böl
        nihai_sonuc = (sayi_2 - ana_rakam) / 2
        
        st.markdown("---")
        
        # Görsel Sonuçlar
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric("Bulunan Ana Rakam", f"{ana_rakam:,.2f}")
            st.caption(f"({sayi_1:,.2f} / 0,058)")
            
        with res_col2:
            st.metric("Nihai Sonuç", f"{nihai_sonuc:,.2f}")
            st.caption(f"({sayi_2:,.2f} - {ana_rakam:,.2f}) / 2")
            
        if nihai_sonuc < 0:
            st.warning("Not: Çıkartma işlemi sonucu negatif bir değer çıktı.")
            
    else:
        st.error("Lütfen %5,80 hesabı için geçerli bir sayı giriniz.")

# Alt Bilgi
st.info("Yeni Akış: [Girdi 2 - (Girdi 1 / 0,058)] / 2")
