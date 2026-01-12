import streamlit as st
import pandas as pd
import io

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Takip Paneli", layout="centered")

# --- ATASUN KURUMSAL TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan Turuncu */
    .stApp {
        background-color: #FF671B;
    }
    
    /* Beyaz Orta Panel */
    .block-container {
        background-color: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 2rem;
    }

    /* Başlık Stilleri */
    h1 {
        color: #333333;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        margin-bottom: 0px;
    }
    .panel-header {
        text-align: center;
        color: #666;
        font-weight: bold;
        margin-bottom: 30px;
    }

    /* Giriş Kutusu */
    .stTextInput>div>div>input {
        border: 2px solid #FF671B !important;
        border-radius: 10px;
        height: 50px;
        font-size: 20px;
    }

    /* Butonlar (Siyah/Koyu Gri) */
    .stButton>button {
        width: 100%;
        background-color: #333333 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5em;
        font-weight: bold;
        border: none !important;
    }
    
    .stButton>button:hover {
        background-color: #555555 !important;
        transform: scale(1.01);
    }

    /* Tablo ve Uyarılar */
    .stDataFrame { border: 1px solid #eee; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Üst Bilgi
st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p class='panel-header'>Açık Kapora Takip Paneli</p>", unsafe_allow_html=True)

# --- VERİ HAFIZASI ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: EXCEL YÜKLEME ---
with st.expander("📂 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        c1, c2 = st.columns(2)
        s_no_col = c1.selectbox("Sipariş No Sütunu", df_temp.columns)
        s_isim_col = c2.selectbox("Müşteri İsim Sütunu", df_temp.columns)
        
        st.session_state.db = df_temp[[s_no_col, s_isim_col]].copy()
        st.session_state.db.columns = ['kod', 'isim']
        st.session_state.db['kod'] = st.session_state.db['kod'].astype(str).str.strip().str.upper()
        st.success(f"✅ {len(st.session_state.db)} Sipariş Yüklendi.")

st.divider()

# --- 2. ADIM: CANLI BARKOD OKUTMA ---
if not st.session_state.db.empty:
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Sipariş Numarasını Okutun")
        input_kod = st.text_input("", placeholder="Barkodu okutun ve bekleyin...").strip().upper()
        submit = st.form_submit_button("SORGULA")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['kod'] == input_kod]
        if not match.empty:
            isim = match['isim'].iloc[0]
            st.success(f"✅ LİSTEDE VAR \n\n **Sipariş No:** {input_kod} \n\n **Müşteri:** {isim}")
            st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- 3. ADIM: RAPOR VE DIŞA AKTAR ---
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    if st.button("📊 Eksikleri Listele"):
        eksik_df = st.session_state.db[~st.session_state.db['kod'].isin(st.session_state.okutulanlar)]
        if not eksik_df.empty:
            st.warning(f"{len(eksik_df)} Eksik Sipariş Bulundu")
            st.dataframe(eksik_df, use_container_width=True)
            
            # Excel İndirme Butonu
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                eksik_df.to_excel(writer, index=False, sheet_name='Eksik_Listesi')
            
            st.download_button(
                label="📥 Eksik Listesini Excel İndir",
                data=output.getvalue(),
                file_name="Atasun_Eksik_Siparisler.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("Tüm siparişler tamamlandı!")

with col_right:
    if st.button("🔄 Paneli Sıfırla"):
        st.session_state.okutulanlar = set()
        st.rerun()
