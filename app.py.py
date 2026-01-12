import streamlit as st
import pandas as pd
import io

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Atasun Optik - Takip Paneli", layout="centered")

# --- ATASUN KURUMSAL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FF671B; }
    .block-container {
        background-color: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 2rem;
    }
    h1 { color: #333333; font-family: 'Arial Black', sans-serif; text-align: center; margin-bottom: 0px; }
    .panel-header { text-align: center; color: #666; font-weight: bold; margin-bottom: 30px; }
    .stTextInput>div>div>input { border: 2px solid #FF671B !important; border-radius: 10px; height: 50px; font-size: 20px; }
    .stButton>button { width: 100%; background-color: #333333 !important; color: white !important; border-radius: 10px !important; height: 3.5em; font-weight: bold; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👓 ATASUN OPTİK</h1>", unsafe_allow_html=True)
st.markdown("<p class='panel-header'>Açık Kapora Takip Paneli</p>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()
    st.session_state.okutulanlar = set()

# --- 1. ADIM: EXCEL YÜKLEME ---
with st.expander("📁 Ana Sipariş Listesini Yükle", expanded=True):
    yuklenen_dosya = st.file_uploader("", type=['xlsx'])
    if yuklenen_dosya:
        df_temp = pd.read_excel(yuklenen_dosya)
        st.info("Sütunları Eşleştirin:")
        c1, c2, c3 = st.columns(3)
        s_no_col = c1.selectbox("Sipariş No", df_temp.columns)
        s_isim_col = c2.selectbox("Müşteri İsim", df_temp.columns)
        s_pers_col = c3.selectbox("Personel No", df_temp.columns)
        
        st.session_state.db = df_temp[[s_no_col, s_isim_col, s_pers_col]].copy()
        st.session_state.db.columns = ['Sipariş No', 'Müşteri Adı', 'Personel No']
        st.session_state.db['Sipariş No'] = st.session_state.db['Sipariş No'].astype(str).str.strip().str.upper()
        st.success(f"✅ {len(st.session_state.db)} Sipariş Yüklendi.")

st.divider()

# --- 2. ADIM: CANLI OKUTMA ---
if not st.session_state.db.empty:
    with st.form(key='barkod_form', clear_on_submit=True):
        st.markdown("### 📲 Sipariş Numarasını Okutun")
        input_kod = st.text_input("", placeholder="Barkodu okutun...").strip().upper()
        submit = st.form_submit_button("SORGULA")

    if submit and input_kod:
        match = st.session_state.db[st.session_state.db['Sipariş No'] == input_kod]
        if not match.empty:
            isim = match['Müşteri Adı'].iloc[0]
            p_no = match['Personel No'].iloc[0]
            st.success(f"✅ LİSTEDE VAR \n\n **Müşteri:** {isim} | **Personel:** {p_no}")
            st.session_state.okutulanlar.add(input_kod)
        else:
            st.error(f"❌ LİSTEDE YOK: {input_kod}")

# --- 3. ADIM: RAPORLAMA VE EXCEL ---
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    if st.button("📊 Eksikleri Listele"):
        eksik_df = st.session_state.db[~st.session_state.db['Sipariş No'].isin(st.session_state.okutulanlar)].copy()
        
        if not eksik_df.empty:
            # 1'den başlayan sıra numarası sütunu ekleme
            eksik_df.insert(0, 'Sıra No', range(1, len(eksik_df) + 1))
            
            st.warning(f"{len(eksik_df)} Eksik Sipariş Bulundu")
            st.dataframe(eksik_df, use_container_width=True, hide_index=True)
            
            # Excel İndirme
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                eksik_df.to_excel(writer, index=False, sheet_name='Eksik_Siparis_Listesi')
            
            st.download_button(
                label="📥 Eksik Listesini Excel İndir",
                data=output.getvalue(),
                file_name="Atasun_Eksik_Listesi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("Tüm siparişler tamamlandı!")

with col_right:
    if st.button("🔄 Paneli Sıfırla"):
        st.session_state.okutulanlar = set()
        st.rerun()
