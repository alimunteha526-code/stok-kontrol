import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Zayi Hedefi Hesaplayıcı", layout="centered", page_icon="🎯")

# Yeni Başlık ve Açıklama
st.title("🎯 Zayi Hedefi Hesap Tablosu")
st.write("Verileri girerek zayi hedefleri ve paylaştırma oranlarını hesaplayabilirsiniz.")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    girdi_1 = st.number_input("%5,80'in kaynağı olan sayı:", min_value=0.0, step=0.01, format="%.2f")

with col2:
    girdi_2 = st.number_input("Çıkarılacak (işlem yapılacak) rakam:", min_value=0.0, step=0.01, format="%.2f")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # 1. Aşama: Ana rakamı hesapla
        ana_rakam = girdi_1 / 0.058
        
        # 2. Aşama: Ana rakamdan girdi_2'yi çıkar ve 2'ye böl (Nihai Sonuç)
        nihai_sonuc = (ana_rakam - girdi_2) / 2
        
        # 3. Aşama: Nihai sonucu 17'ye böl
        on_yediye_bolum = nihai_sonuc / 17
        
        st.divider()
        
        # Özet Tablo Görünümü (Metrics)
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric("Hesaplanan Ana Rakam", f"{ana_rakam:,.2f}")
            
        with res_col2:
            st.metric("Nihai Sonuç", f"{nihai_sonuc:,.2f}")
        
        st.write("##") 
        
        # 17'ye Bölüm - Zayi Payı
        st.subheader("📌 Personel Başına Zayi Hedef Payı (1/17)")
        st.success(f"Hesaplanan Pay: **{on_yediye_bolum:,.2f}**")
        
        # Görsel bir tablo şeklinde özet
        st.info("İşlem Detayları")
        st.table({
            "İşlem Adımı": ["Ana Rakam (%100)", "İşlem Sonucu (Bölüm Öncesi)", "Nihai Sonuç (/2)", "17'ye Bölüm"],
            "Değer": [f"{ana_rakam:,.2f}", f"{ana_rakam - girdi_2:,.2f}", f"{nihai_sonuc:,.2f}", f"{on_yediye_bolum:,.2f}"]
        })
        
    else:
        st.error("Lütfen ilk kutuya geçerli bir sayı giriniz.")

# Alt bilgi
st.markdown("---")
st.caption("Bu tablo zayi hedef hesaplamaları için özel olarak konfigüre edilmiştir.")
