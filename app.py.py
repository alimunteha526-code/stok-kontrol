import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Zayi Hedefi Hesap Tablosu", layout="centered", page_icon="🎯")

# Başlık
st.title("🎯 Zayi Hedefi Hesap Tablosu")

# Giriş Alanları
col1, col2 = st.columns(2)

with col1:
    # Giriş kısmında da ondalık görünmemesi için value ve step tam sayı
    girdi_1 = st.number_input("Zayi Adeti:", min_value=0, step=1, value=0, key="zayi")

with col2:
    girdi_2 = st.number_input("Kesilen Cam Adeti:", min_value=0, step=1, value=0, key="cam")

# Hesaplama Butonu
if st.button("Hesaplamayı Başlat"):
    if girdi_1 > 0:
        # Hesaplamalar
        toplam_cam = int(girdi_1 / 0.058)
        toplam_foy = int((toplam_cam - girdi_2) / 2)
        magaza_foy = int(toplam_foy / 17)
        
        st.divider()
        
        # Sayıları METİN (string) formatına zorlayarak yazdırıyoruz
        # Bu sayede sistem sonuna virgül veya sıfır ekleyemez
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Kesilmesi Gereken Toplam Cam Adeti**")
            st.subheader(str(toplam_cam)) # Sayıyı metne çevirdik: str()
            
        with c2:
            st.write("**Kesilmesi Gereken Toplam Föy Adeti**")
            st.subheader(str(toplam_foy)) # Sayıyı metne çevirdik: str()
        
        st.write("##") 
        
        # Nihai Hedef Bölümü
        st.info("📋 Mağazada Hatasız Kesilmesi Gereken Föy Adeti")
        # En büyük ve net gösterim
        st.title(str(magaza_foy))
        
    else:
        st.error("Lütfen 'Zayi Adeti' kısmına bir değer giriniz.")

# Alt bilgi
st.markdown("---")
st.caption("Veriler operasyonel hedefler doğrultusunda tam sayı olarak sunulmaktadır.")
