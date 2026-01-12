import streamlit as st
import pandas as pd
import io

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Açık Kapora", layout="centered")

# --- ATASUN TURUNCU TEMA (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #FF671B; /* Atasun Turuncusu */
    }
    
    /* Beyaz Kart Alanı */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-top: 2rem;
    }

    /* Başlıklar */
    h1, h3 {
        color: #333333 !important;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
    }

    /* Giriş Kutusu ve Butonlar */
    .stTextInput>div>div>input {
        border: 2px solid #FF671B;
        border-radius: 10px;
    }
    
    .stButton>button {
        background-color: #333333 !important; /* Koyu Gri/Siyah Butonlar */
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #555555 !important;
        transform: scale(1.02);
    }

    /* Uyarı Kutuları */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Üst Başlık ve Logo
st.markdown("<h1 style='font-size: 40px;'>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Açık Kapora Takip ve Kontrol Paneli</p>", unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: LİSTE YÜKLEME ---
with st.expander("📁 Excel Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        c1, c2 = st.columns(2)
        s_no_col = c1.selectbox("Sipariş No Sütunu", df_temp.columns)
        s_isim_col = c2.selectbox("İsim Sütunu", df_temp.columns)
        
        st.session_state.db = df_temp[[s_no_col, s_isim_col]].copy()
        st.session_state.db.columns = ['kod', 'isim']
        st.session_state.db['kod'] = st.session_state.db['kod'].astype(str).str.strip().str.upper()
        st.success(f"✅ {len(st.session_state.db)} Kayıt Yüklendi.")

st.divider()

# --- 2. ADIM: OKUTMA FORMU ---
if not st.session_state.db.empty:
    with st.form(key='scan_form', clear_on_submit=True):
        st.markdown("### 📲 Sipariş No Okutun")
        input_kod = st.text_input("", placeholder="Barkodu buraya vurun...").strip().upper()
        submit = st.form_submit_button("SİSTEME SOR")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['kod'] == input_kod]
        if not match.empty:
            isim = match['isim'].iloc[0]
            st.success(f"✅ LİSTEDE VAR: {input_kod} \n\n 👤 Müşteri: {isim}")
            st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- 3. ADIM: RAPORLAMA ---
st.divider()
col_a, col_b = st.columns(2)

with col_a:
    if st.button("📊 Eksikleri Raporla"):
        eksik_df = st.session_state.db[~st.session_state.db['kod'].isin(st.session_state.okutulanlar)]
        if not eksik_df.empty:
            st.warning(f"{len(eksik_df)} adet eksik bulundu.")
            st.dataframe(eksik_df, use_container_width=True)
            
            # Excel İndirme
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                eksik_df.to_excel(writer, index=False, sheet_name='Eksik_Listesi')
            
            st.download_button(
                label="📥 Excel Olarak İndir",
                data=output.getvalue(),
                file_name="Atasun_Eksik_Siparisler.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("Tebrikler, tüm siparişler tamam!")

with col_b:
    if st.button("🔄 Sayımı Sıfırla"):
        st.session_state.okutulanlar = set()
        st.rerun()
