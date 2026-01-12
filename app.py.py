import streamlit as st
import pandas as pd
import base64 # Logoyu base64'e çevirmek için

# --- SABİT DEĞİŞKENLER ---
# Atasun Optik logosunun web adresi (Örnek URL, kendi logonuzla değiştirin)
# Bu URL'yi kendi logonuzun internetteki bir linki ile değiştirmeniz gerekebilir
ATASUN_LOGO_URL = "https://www.atasunoptik.com.tr/Assets/img/atasun-optik-logo.svg" 

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Açık Kapora", layout="centered")

# --- ARKA PLAN LOGOSU İÇİN CSS ---
# Streamlit'e özel CSS enjeksiyonu
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url({ATASUN_LOGO_URL}) no-repeat top left;
        background-size: 150px; /* Logo boyutu */
        background-position: 10px 10px; /* Logo konumu */
        padding-top: 5rem; /* İçeriğin logonun altına inmesini sağlar */
    }}
    .sidebar .sidebar-content {{
        background: url({ATASUN_LOGO_URL}) no-repeat;
        background-size: 100px;
        background-position: 10px 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("👓 Atasun Optik")
st.subheader("Açık Kapora / Sipariş Kontrol Sistemi")

# --- HAFIZA YÖNETİMİ ---
# siparis_havuzu: Ana liste (kod ve diğer bilgilerle)
# okutulan_siparis_kodlari: Sadece okutulan kodlar
if 'siparis_havuzu' not in st.session_state:
    st.session_state.siparis_havuzu = pd.DataFrame() # DataFrame olarak saklayacağız
    st.session_state.okutulan_siparis_kodlari = set()

# --- 1. ADIM: LİSTE YÜKLEME ---
yuklenen_dosya = st.file_uploader("Açık Kapora Listesini Yükleyin (Excel)", type=['xlsx'])

if yuklenen_dosya:
    try:
        df_ana = pd.read_excel(yuklenen_dosya)
        
        # Excel'deki ilk iki sütunu kullanacağımızı varsayalım: 
        # İlk sütun: Sipariş Kodu, İkinci Sütun: Müşteri Adı/Diğer Bilgi
        if len(df_ana.columns) < 2:
            st.error("Excel dosyanızda en az iki sütun olmalı: (1) Sipariş Kodu, (2) İsim/Açıklama.")
        else:
            # Sütun isimlerini kullanıcıya seçtirelim (daha esnek olur)
            st.info("Lütfen Sipariş Numarası ve İsim sütunlarını seçin.")
            col_siparis, col_isim = st.columns(2)
            secilen_siparis_sutun = col_siparis.selectbox("Sipariş Numarası Sütunu", df_ana.columns)
            secilen_isim_sutun = col_isim.selectbox("Müşteri/İsim Sütunu", df_ana.columns)

            st.session_state.siparis_havuzu = df_ana[[secilen_siparis_sutun, secilen_isim_sutun]].copy()
            st.session_state.siparis_havuzu.columns = ['SiparisKodu', 'Isim'] # Sütun isimlerini standartlaştır
            st.session_state.siparis_havuzu['SiparisKodu'] = st.session_state.siparis_havuzu['SiparisKodu'].astype(str).str.strip().str.upper()
            
            st.success(f"✅ Liste Yüklendi: {len(st.session_state.siparis_havuzu)} adet bekleyen sipariş bulundu.")
            
    except Exception as e:
        st.error(f"Excel okunurken hata oluştu: {e}. Lütfen dosya formatını kontrol edin.")

st.divider()

# --- 2. ADIM: OKUTMA FORMU ---
if not st.session_state.siparis_havuzu.empty: # Eğer liste yüklendiyse okutma formunu göster
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Sipariş Numarasını Okutun")
        siparis_no_giris = st.text_input("Giriş Yapın", placeholder="Barkodu buraya okutun...").strip().upper()
        submit_button = st.form_submit_button(label='Kontrol Et')

    if submit_button and siparis_no_giris:
        if siparis_no_giris in st.session_state.siparis_havuzu['SiparisKodu'].values:
            ilgili_isim = st.session_state.siparis_havuzu[st.session_state.siparis_havuzu['SiparisKodu'] == siparis_no_giris]['Isim'].iloc[0]
            st.success(f"✅ DOĞRU: {siparis_no_giris} - Müşteri: **{ilgili_isim}** - Listede var.")
            if siparis_no_giris not in st.session_state.okutulan_siparis_kodlari:
                st.session_state.okutulan_siparis_kodlari.add(siparis_no_giris) # Set'e ekle
        else:
            st.error(f"❌ HATA: {siparis_no_giris} LİSTEDE BULUNAMADI!")
else:
    st.warning("Lütfen başlamadan önce 'Açık Kapora Listesi' Excel dosyasını yükleyin.")

# --- 3. ADIM: RAPORLAMA VE İNDİRME ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("Sayımı Bitir ve Eksikleri Göster"):
        okutulan_kodlar_set = st.session_state.okutulan_siparis_kodlari
        
        # Ana listedeki kodları okutulanlarla karşılaştır
        eksik_df = st.session_state.siparis_havuzu[
            ~st.session_state.siparis_havuzu['SiparisKodu'].isin(okutulan_kodlar_set)
        ]
        
        if not eksik_df.empty:
            st.warning(f"Sayılamayan / Eksik Sipariş: {len(eksik_df)} adet.")
            st.dataframe(eksik_df, use_container_width=True)

            # Eksik listesini Excel olarak indirilebilir hale getir
            @st.cache_data # Veriyi önbelleğe al
            def convert_df_to_excel(df_to_convert):
                output = df_to_convert.to_excel(index=False, header=True, engine='xlsxwriter')
                return output

            excel_data = convert_df_to_excel(eksik_df)
            st.download_button(
                label="Eksik Listesini Excel İndir",
                data=excel_data,
                file_name="Eksik_Siparis_Listesi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("Tüm siparişler tamamlandı!")

with col2:
    if st.button("Sistemi Sıfırla / Yeni Listeyi Yükle"):
        st.session_state.clear() # Tüm session state'i temizle
        st.rerun() # Sayfayı yeniden yükle
