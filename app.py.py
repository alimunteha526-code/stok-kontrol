import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Gelişmiş Hesaplama Sistemi", layout="centered")

st.title("🧮 Özel Hesaplama ve Paylaştırma Paneli")
st.write("Ana rakam üzerinden çıkarma, bölme ve 17'li paylaştırma işlemleri.")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    girdi_1 = st.number_input("%5,80'in kaynağı olan sayı:", min_value=0.0, step=0.01, format="%.2f")

with col2:
    girdi_2 = st.number_input("Çıkarılacak (işlem yapılacak) rakam:", min_value=0.0, step=0.01, format="%.2f")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # 1. Aşama: Ana rakamı hesapla (%5,80'den geri git)
        ana_rakam = girdi_1 / 0.058
        
        # 2. Aşama: Ana rakamdan girdi_2'yi çıkar ve 2'ye böl (Nihai Sonuç)
        nihai_sonuc = (ana_rakam - girdi_2) / 2
        
        # 3. Aşama: Nihai sonucu 17'ye böl
        on_yediye_bolum = nihai_sonuc / 17
        
        st.divider()
        
        # Ana Sonuç Panelleri
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric("Hesaplanan Ana Rakam", f"{ana_rakam:,.2f}")
            st.caption(f"({girdi_1:,.2f} / 0,058)")
            
        with res_col2:
            st.metric("Nihai Sonuç", f"{nihai_sonuc:,.2f}")
            st.caption(f"({ana_rakam:,.2f} - {girdi_2:,.2f}) / 2")
        
        st.write("##") # Biraz boşluk bırakalım
        
        # 17'ye Bölüm Sonucu (Daha belirgin bir vurgu ile)
        st.subheader("📌 17'ye Bölünmüş Sonuç")
        st.info(f"Nihai sonucun 17'ye bölümü: **{on_yediye_bolum:,.2f}**")
        
    else:
        st.error("Lütfen ilk kutuya 0'dan büyük bir sayı giriniz.")

# Alt bilgi ve formül hatırlatıcı
st.markdown("---")
st.caption("İşlem Akışı: [((Girdi 1 / 0,058) - Girdi 2) / 2] / 17")
