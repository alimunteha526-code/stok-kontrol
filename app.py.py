import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Zayi Hedefi Hesap Tablosu", layout="centered", page_icon="🎯")

# Başlık
st.title("🎯 Zayi Hedefi Hesap Tablosu")
st.write("Hesaplama yapmak için gerekli verileri giriniz.")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    girdi_1 = st.number_input("%5,80'in kaynağı olan sayı:", min_value=0.0, step=0.01, format="%.2f", key="g1")

with col2:
    girdi_2 = st.number_input("Çıkarılacak (işlem yapılacak) rakam:", min_value=0.0, step=0.01, format="%.2f", key="g2")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # 1. Aşama: Ana rakamı hesapla
        ana_rakam = girdi_1 / 0.058
        
        # 2. Aşama: Ana rakamdan girdi_2'yi çıkar ve 2'ye böl (Nihai Sonuç)
        nihai_sonuc = (ana_rakam - girdi_2) / 2
        
        # 3. Aşama: Föy Adeti (17'ye bölüm)
        foy_adeti = nihai_sonuc / 17
        
        st.divider()
        
        # Üst Özet Kartları
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric("Hesaplanan Ana Rakam", f"{ana_rakam:,.2f}")
            
        with res_col2:
            st.metric("Nihai Sonuç (Bölüm Öncesi)", f"{nihai_sonuc:,.2f}")
        
        st.write("##") 
        
        # Mağazada Hatasız Kesilmesi Gereken Föy Adeti
        st.subheader("📋 Mağazada Hatasız Kesilmesi Gereken Föy Adeti")
        st.success(f"Gerekli Föy Adeti: **{foy_adeti:,.2f}**")
        
    else:
        st.error("Lütfen ilk kutuya geçerli bir sayı giriniz.")

# Alt bilgi
st.markdown("---")
st.caption("Veriler operasyonel hedefler doğrultusunda hesaplanmaktadır.")
