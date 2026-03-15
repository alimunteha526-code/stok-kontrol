import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Zayi Hedefi Hesap Tablosu", layout="centered", page_icon="🎯")

# Başlık
st.title("🎯 Zayi Hedefi Hesap Tablosu")
st.write("Operasyonel verileri girerek hedeflerinizi hesaplayabilirsiniz.")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    girdi_1 = st.number_input("Zayi Adeti:", min_value=0, step=1, key="zayi")

with col2:
    girdi_2 = st.number_input("Kesilen Cam Adeti:", min_value=0, step=1, key="cam")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # Hesaplamalar ve Tam Sayıya Çevirme (int)
        toplam_cam_hedefi = int(girdi_1 / 0.058)
        toplam_foy_adeti = int((toplam_cam_hedefi - girdi_2) / 2)
        magaza_foy_hedefi = int(toplam_foy_adeti / 17)
        
        st.divider()
        
        # Sonuçları Metric yerine "st.write" veya "st.markdown" ile yazdırıyoruz
        # Bu sayede Streamlit sayıya dokunamaz, sadece bizim yazdığımızı basar.
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Kesilmesi Gereken Toplam Cam Adeti**")
            st.title(f"{toplam_cam_hedefi}") # Büyük ve temiz rakam
            
        with c2:
            st.markdown(f"**Kesilmesi Gereken Toplam Föy Adeti**")
            st.title(f"{toplam_foy_adeti}") # Büyük ve temiz rakam
        
        st.write("##") 
        
        # Nihai Hedef Bölümü
        st.success("📋 Mağazada Hatasız Kesilmesi Gereken Föy Adeti")
        st.header(f"Gerekli Föy Adeti: {magaza_foy_hedefi}")
        
    else:
        st.error("Lütfen 'Zayi Adeti' kısmına geçerli bir sayı giriniz.")

# Alt bilgi
st.markdown("---")
st.caption("Veriler operasyonel zayi hedefleri doğrultusunda hesaplanmaktadır.")
