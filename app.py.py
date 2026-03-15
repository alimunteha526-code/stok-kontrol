import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Zayi Hedefi Hesap Tablosu", layout="centered", page_icon="🎯")

# Başlık
st.title("🎯 Zayi Hedefi Hesap Tablosu")
st.write("Operasyonel verileri girerek hedeflerinizi hesaplayabilirsiniz.")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    # Sayı girişlerini tam sayı (step=1) olarak ayarladık
    girdi_1 = st.number_input("Zayi Adeti:", min_value=0, step=1, key="zayi")

with col2:
    girdi_2 = st.number_input("Kesilen Cam Adeti:", min_value=0, step=1, key="cam")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # 1. Aşama: Toplam cam adetine ulaş (%5,80 üzerinden)
        toplam_cam_hedefi = girdi_1 / 0.058
        
        # 2. Aşama: Toplam föy adeti (Farkın ikiye bölünmüş hali)
        toplam_foy_adeti = (toplam_cam_hedefi - girdi_2) / 2
        
        # 3. Aşama: Mağazada Hatasız Kesilmesi Gereken Föy Adeti (17'ye bölüm)
        magaza_foy_hedefi = toplam_foy_adeti / 17
        
        st.divider()
        
        # Sonuç Kartları - Sıfırları kaldırmak için int() veya :.0f kullanıyoruz
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            # Yuvarlayarak tam sayı gösteriyoruz
            st.metric("Kesilmesi Gereken Toplam Cam Adeti", f"{toplam_cam_hedefi:,.0f}")
            
        with res_col2:
            st.metric("Kesilmesi Gereken Toplam Föy Adeti", f"{toplam_foy_adeti:,.0f}")
        
        st.write("##") 
        
        # Nihai Hedef
        st.subheader("📋 Mağazada Hatasız Kesilmesi Gereken Föy Adeti")
        # Sonucu en yakın tam sayıya yuvarladık
        st.success(f"Gerekli Föy Adeti (Birim Başına): **{magaza_foy_hedefi:,.0f}**")
        
    else:
        st.error("Lütfen 'Zayi Adeti' kısmına geçerli bir sayı giriniz.")

# Alt bilgi
st.markdown("---")
st.caption("Bu araç operasyonel verimlilik ve zayi yönetimi için optimize edilmiştir.")
