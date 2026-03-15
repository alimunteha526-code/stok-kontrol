import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Ters Yüzde Hesaplayıcı", layout="centered")

# Başlık ve Açıklama
st.title("📊 %5,80 Hesaplama Aracı")
st.write("Girdiğiniz sayının, hangi rakamın %5,80'i olduğunu anında hesaplar.")

# Kullanıcı Girişi
number_input = st.number_input("Lütfen elinizdeki sayıyı giriniz:", min_value=0.0, step=0.01, format="%.2f")

# Hesaplama Butonu
if st.button("Hesapla"):
    if number_input > 0:
        # %5,80 olduğu için 0.058'e bölüyoruz
        result = number_input / 0.058
        
        # Sonuç Ekranı
        st.success(f"Girdiğiniz {number_input:.2f} sayısı, aşağıdaki rakamın %5,80'idir:")
        st.metric(label="Bulunan Ana Rakam", value=f"{result:,.2f}")
        
        # Detaylı Bilgi
        st.info(f"Doğrulama: {result:,.2f} x 0,058 = {number_input:.2f}")
    else:
        st.warning("Lütfen 0'dan büyük bir sayı giriniz.")

# Alt Bilgi
st.markdown("---")
st.caption("Streamlit ile hızlı hesaplama modülü.")
