import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from database import get_chemical_database, get_ghs_images
from analyzer import analyze_compatibility
import json

st.set_page_config(
    page_title="CHECKCOMCHEMISTRY",
    page_icon="🧪🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    body {
        background-color: #1a1a2e;
        color: #eaeaea;
    }
    
    .main {
        background-color: #16213e;
        color: #eaeaea;
    }
    
    .main-title {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .section-title {
        font-size: 28px;
        font-weight: bold;
        color: #00d4ff;
        border-bottom: 3px solid #00d4ff;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    
    .status-card {
        padding: 30px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 24px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin: 20px 0;
        animation: slideIn 0.6s ease-out;
    }
    
    .safe {
        background: linear-gradient(135deg, #00d97e 0%, #00a85e 100%);
        color: white;
        border: 3px solid #00a85e;
    }
    
    .danger {
        background: linear-gradient(135deg, #ff006e 0%, #c90050 100%);
        color: white;
        border: 3px solid #c90050;
    }
    
    .warning {
        background: linear-gradient(135deg, #ffa500 0%, #cc8400 100%);
        color: white;
        border: 3px solid #cc8400;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes popIn {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .ghs-icon-container {
        text-align: center;
        margin: 20px 0;
    }
    
    .ghs-icon {
        display: inline-block;
        animation: popIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.4));
        transition: transform 0.3s ease;
    }
    
    .ghs-icon:hover {
        transform: scale(1.1) rotateZ(5deg);
    }
    
    .chemical-card {
        background: #0f3460;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
        border: 2px solid #00d4ff;
    }
    
    .chemical-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 25px rgba(0,212,255,0.3);
    }
    
    .chemical-name {
        font-weight: bold;
        color: #00d4ff;
        margin-top: 15px;
        font-size: 14px;
    }
    
    .chemical-category {
        color: #ffa500;
        font-size: 12px;
        margin-top: 8px;
        font-weight: 600;
    }
    
    .danger-badge {
        display: inline-block;
        background: #ff006e;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 8px;
        animation: popIn 0.8s ease-out;
    }
    
    .warning-badge {
        display: inline-block;
        background: #ffa500;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 8px;
        animation: popIn 0.8s ease-out;
    }
    
    .safe-badge {
        display: inline-block;
        background: #00d97e;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 8px;
        animation: popIn 0.8s ease-out;
    }
    
    .info-box {
        background: #0f3460;
        border-left: 5px solid #00d4ff;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #eaeaea;
    }
    
    .metric-card {
        background: #0f3460;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        text-align: center;
        margin: 10px;
        border: 2px solid #00d4ff;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #00d4ff;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #ffa500;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 212, 255, 0.4);
    }
    
    .stSelectbox, .stTextInput {
        color: #eaeaea;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #0f3460;
    }
    
    .favorite-card {
        background: linear-gradient(135deg, #0f3460 0%, #1a4d6d 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid #ff006e;
        box-shadow: 0 4px 15px rgba(255,0,110,0.2);
        animation: slideIn 0.6s ease-out;
    }
    
    .favorite-card:hover {
        box-shadow: 0 8px 25px rgba(255,0,110,0.4);
        transform: translateY(-5px);
    }
    
    .favorite-title {
        color: #ff006e;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    
    .favorite-info {
        color: #eaeaea;
        font-size: 14px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===== INITIALIZE SESSION STATE =====
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.sidebar.markdown("""
<div style='text-align:center; padding:20px 0;'>
    <h1 style='font-size:40px; margin:0;'>🧪</h1>
    <h2 style='font-size:20px; margin:5px 0; color:#00d4ff;'>Checkcomchemistry</h2>
    <p style='font-size:12px; color:#ffa500;'>Politeknik AKA Bogor</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 MENU UTAMA",
    ["🏠 Home", "🔍 Cek Kompatibilitas", "📊 Dashboard", "❤️ Favorit", "📚 Panduan", "🧪 Database", "⚙️ Pengaturan"]
)

if menu == "🏠 Home":
    st.markdown("<div class='main-title'>🧪 CHECKCOMCHEMISTRY</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h3 style='color:#00d4ff;'>🎯 Selamat Datang di Checkcomchemistry</h3>
        <p>Sistem manajemen keamanan bahan kimia dengan visualisasi 3D GHS yang canggih, database 500+ bahan kimia, dan analisis real-time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:40px;'>🔍</div>
            <div class='metric-label'>CEK KOMPATIBILITAS</div>
            <p style='font-size:12px; color:#eaeaea;'>Analisis real-time dengan visualisasi 3D</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:40px;'>📊</div>
            <div class='metric-label'>DASHBOARD ANALYTICS</div>
            <p style='font-size:12px; color:#eaeaea;'>Visualisasi data keamanan lengkap</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:40px;'>📚</div>
            <div class='metric-label'>PANDUAN LENGKAP</div>
            <p style='font-size:12px; color:#eaeaea;'>Edukasi FCOT & GHS interaktif</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🚀 Fitur Utama
        - Cek kompatibilitas 500+ bahan kimia
        - Animasi 3D simbol bahaya GHS
        - Rekomendasi penyimpanan otomatis
        - Dashboard analytics komprehensif
        - Export data mudah
        """)
    
    with col2:
        st.markdown("""
        ### 🛡️ Keamanan
        - Standar GHS terintegrasi penuh
        - Alert sistem real-time
        - Panduan penanganan lengkap
        - Simpan favorit & histori
        - Support 250+ kombinasi
        """)

elif menu == "🔍 Cek Kompatibilitas":
    st.markdown("<h2 class='section-title'>🔍 Cek Kompatibilitas Bahan Kimia</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    ghs_images = get_ghs_images()
    
    import os
    st.write("Path gambar:", ghs_images.get("Corrosive"))
    st.write("File ditemukan:", os.path.exists(ghs_images.get("Corrosive")))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Bahan Kimia 1** 🧪")
        chem1 = st.selectbox("Pilih bahan pertama", list(chemical_db.keys()), key="chem1", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Bahan Kimia 2** 🧪")
        chem2 = st.selectbox("Pilih bahan kedua", list(chemical_db.keys()), key="chem2", label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        check_btn = st.button("✅ Cek Sekarang", use_container_width=True, key="check_btn")
    with col2:
        clear_all = st.button("🧹 Hapus Semua", use_container_width=True, key="clear_all_btn")
    
    # ---- CLEAR ALL HISTORY ----
    if clear_all:
        st.session_state.history = []
        st.success("✅ Semua data riwayat dihapus!")
        st.rerun()
    
    # ---- CHECK/ANALISIS ----
    if check_btn:
        with st.spinner("🔬 Menganalisis kombinasi bahan kimia..."):
            import time
            time.sleep(1.2)
        
        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]
        status, penjelasan, penyimpanan = analyze_compatibility(t1, t2)
        
        status_class = "safe" if "AMAN" in status else ("danger" if "BERBAHAYA" in status else "warning")
        
        st.markdown(f"<div class='status-card {status_class}'>{status}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chemical-card'>", unsafe_allow_html=True)
                       
        import os
        
        image_path = ghs_images.get(t1)
        
        st.write("Path:", image_path)
        st.write("Ada file:", os.path.exists(image_path))
        
        if os.path.exists(image_path):
            st.image(image_path, width=120)
        else:
            st.error(f"File tidak ditemukan: {image_path}")
            st.markdown(f"""
            <div class='chemical-name'>{chem1}</div>
            <div class='chemical-category'>{t1}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='chemical-card'>", unsafe_allow_html=True)
            st.image(
                ghs_images.get(t2),
                width=120
            )
            st.markdown(f"""
            <div class='chemical-name'>{chem2}</div>
            <div class='chemical-category'>{t2}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 3D GHS Symbol Animation
        st.markdown("<h3 class='section-title'>🎯 Visualisasi Simbol Bahaya (3D)</h3>", unsafe_allow_html=True)
        
        col_ghs1, col_ghs2, col_ghs3 = st.columns(3)
        
        with col_ghs1:
            st.markdown("<div class='ghs-icon-container'>", unsafe_allow_html=True)
            st.markdown(f"<div class='ghs-icon'><img src='{ghs_images.get(t1, '')}' width='120' style='filter: drop-shadow(0 8px 16px rgba(0,212,255,0.5));'></div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:bold; margin-top:10px; color:#00d4ff;'>{t1}</p></div>", unsafe_allow_html=True)
        
        with col_ghs2:
            st.markdown("<div style='text-align:center; display:flex; align-items:center; justify-content:center; height:150px;'><h2 style='font-size:48px; color:#00d4ff;'>+</h2></div>", unsafe_allow_html=True)
        
        with col_ghs3:
            st.markdown("<div class='ghs-icon-container'>", unsafe_allow_html=True)
            st.markdown(f"<div class='ghs-icon'><img src='{ghs_images.get(t2, '')}' width='120' style='filter: drop-shadow(0 8px 16px rgba(0,212,255,0.5));'></div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:bold; margin-top:10px; color:#00d4ff;'>{t2}</p></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧠 Penjelasan Hasil")
            st.info(penjelasan)
        
        with col2:
            st.markdown("### 📦 Rekomendasi Penyimpanan")
            st.warning(penyimpanan)
        
        record = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Bahan 1": chem1,
            "Bahan 2": chem2,
            "Kategori 1": t1,
            "Kategori 2": t2,
            "Hasil": status.replace("❌ ", "").replace("⚠️ ", "").replace("✅ ", ""),
        }
        st.session_state.history.append(record)
        
        # Create favorite data structure
        favorite_data = {
            "id": len(st.session_state.favorites) + 1,
            "chem1": chem1,
            "chem2": chem2,
            "cat1": t1,
            "cat2": t2,
            "status": status.replace("❌ ", "").replace("⚠️ ", "").replace("✅ ", ""),
            "penjelasan": penjelasan,
            "penyimpanan": penyimpanan,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❤️ Tambah ke Favorit"):
                # Cek duplikasi
                is_duplicate = any(
                    fav["chem1"] == chem1 and fav["chem2"] == chem2 
                    for fav in st.session_state.favorites
                )
                if not is_duplicate:
                    st.session_state.favorites.append(favorite_data)
                    st.success("✅ Ditambahkan ke favorit!")
                    st.rerun()
                else:
                    st.warning("⚠️ Kombinasi ini sudah ada di favorit!")
        
        with col2:
            if st.button("📋 Copy Hasil"):
                st.info(f"**Bahan 1:** {chem1} ({t1})\n\n**Bahan 2:** {chem2} ({t2})\n\n**Status:** {status}")

elif menu == "📊 Dashboard":
    st.markdown("<h2 class='section-title'>📊 Dashboard Analytics</h2>", unsafe_allow_html=True)
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Analisis", len(df), delta=None)
        
        bahaya = len(df[df["Hasil"].str.contains("BERBAHAYA", na=False)])
        with col2:
            st.metric("🔴 Berbahaya", bahaya)
        
        aman = len(df[df["Hasil"].str.contains("AMAN", na=False)])
        with col3:
            st.metric("🟢 Aman", aman)
        
        perhatian = len(df[df["Hasil"].str.contains("PERHATIAN", na=False)])
        with col4:
            st.metric("🟡 Perlu Perhatian", perhatian)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 class='section-title'>📈 Distribusi Hasil Analisis</h3>", unsafe_allow_html=True)
            result_counts = df["Hasil"].value_counts()
            fig = px.pie(values=result_counts.values, names=result_counts.index, color_discrete_map={"BERBAHAYA": "#ff006e", "AMAN": "#00d97e", "PERLU PERHATIAN": "#ffa500"})
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<h3 class='section-title'>🧪 Kategori Bahan Terpopuler</h3>", unsafe_allow_html=True)
            all_cats = pd.concat([df["Kategori 1"], df["Kategori 2"]])
            cat_counts = all_cats.value_counts().head(8)
            fig = px.bar(x=cat_counts.index, y=cat_counts.values, labels={"x": "Kategori", "y": "Frekuensi"}, color_discrete_sequence=["#00d4ff"])
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📋 Riwayat Analisis</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, f"fcot_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        with col2:
            json_str = df.to_json(orient="records")
            st.download_button("📥 Download JSON", json_str, f"fcot_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        with col3:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.history = []
                st.rerun()
    else:
        st.info("📭 Belum ada data analisis. Mulai dengan melakukan pengecekan kompatibilitas!")

elif menu == "❤️ Favorit":
    st.markdown("<h2 class='section-title'>❤️ Favorit Analisis</h2>", unsafe_allow_html=True)
    
    if st.session_state.favorites:
        st.success(f"✅ Total {len(st.session_state.favorites)} favorit tersimpan")
        
        # VIEW MODE / EDIT MODE
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_fav = st.selectbox("📊 Urutkan", ["Terbaru", "Terlama", "Nama A-Z"])
        with col2:
            filter_status = st.multiselect("🔍 Filter Status", ["AMAN", "BERBAHAYA", "PERLU PERHATIAN"], default=["AMAN", "BERBAHAYA", "PERLU PERHATIAN"])
        with col3:
            if st.button("📥 Export Favorit"):
                fav_json = json.dumps(st.session_state.favorites, indent=2, ensure_ascii=False)
                st.download_button("Download JSON", fav_json, f"favorit_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        
        # SORT & FILTER
        favorites_sorted = st.session_state.favorites.copy()
        
        if sort_fav == "Terbaru":
            favorites_sorted = sorted(favorites_sorted, key=lambda x: x["timestamp"], reverse=True)
        elif sort_fav == "Terlama":
            favorites_sorted = sorted(favorites_sorted, key=lambda x: x["timestamp"])
        else:
            favorites_sorted = sorted(favorites_sorted, key=lambda x: x["chem1"])
        
        # Filter by status
        favorites_sorted = [fav for fav in favorites_sorted if fav["status"] in filter_status]
        
        st.markdown("---")
        
        if favorites_sorted:
            for idx, fav in enumerate(favorites_sorted):
                st.markdown("""
                <div class='favorite-card'>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    # Status badge
                    status_color = "🟢" if "AMAN" in fav["status"] else ("🔴" if "BERBAHAYA" in fav["status"] else "🟡")
                    st.markdown(f"""
                    <div class='favorite-title'>{status_color} {fav['chem1']} + {fav['chem2']}</div>
                    <div class='favorite-info'><strong>Status:</strong> {fav['status']}</div>
                    <div class='favorite-info'><strong>Kategori:</strong> {fav['cat1']} + {fav['cat2']}</div>
                    <div class='favorite-info'><strong>Disimpan:</strong> {fav['timestamp']}</div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("👁️", key=f"view_{idx}", help="Lihat Detail"):
                        st.session_state[f"show_detail_{idx}"] = not st.session_state.get(f"show_detail_{idx}", False)
                
                with col3:
                    if st.button("❌", key=f"del_{idx}", help="Hapus"):
                        st.session_state.favorites.pop(idx)
                        st.success("✅ Favorit dihapus!")
                        st.rerun()
                
                # DETAIL VIEW
                if st.session_state.get(f"show_detail_{idx}", False):
                    st.markdown("---")
                    st.markdown(f"""
                    <div class='info-box'>
                    <h4 style='color:#00d4ff;'>📝 Penjelasan</h4>
                    <p>{fav['penjelasan']}</p>
                    </div>
                    
                    <div class='info-box'>
                    <h4 style='color:#ffa500;'>📦 Rekomendasi Penyimpanan</h4>
                    <p>{fav['penyimpanan']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Load Ulang Analisis", key=f"reload_{idx}"):
                            st.info(f"Silakan pilih kembali di menu 'Cek Kompatibilitas':\n\n- **Bahan 1:** {fav['chem1']}\n- **Bahan 2:** {fav['chem2']}")
                    with col2:
                        copy_text = f"**Bahan 1:** {fav['chem1']} ({fav['cat1']})\n**Bahan 2:** {fav['chem2']} ({fav['cat2']})\n**Status:** {fav['status']}\n\n**Penjelasan:**\n{fav['penjelasan']}\n\n**Penyimpanan:**\n{fav['penyimpanan']}"
                        if st.button("📋 Copy Semua", key=f"copy_{idx}"):
                            st.info(copy_text)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("")
        else:
            st.info("📭 Tidak ada favorit yang sesuai dengan filter.")
        
        st.markdown("---")
        if st.button("🗑️ Hapus Semua Favorit", use_container_width=True):
            st.session_state.favorites = []
            st.success("✅ Semua favorit dihapus!")
            st.rerun()
    else:
        st.info("📭 Tidak ada favorit. Tambahkan saat melakukan pengecekan kompatibilitas!")

elif menu == "📚 Panduan":
    st.markdown("<h2 class='section-title'>📚 Panduan FCOT & GHS</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["FCOT", "GHS", "Penyimpanan", "FAQ"])
    
    with tab1:
        st.markdown("""
        ## 🔥 FCOT (Chemical Hazard Categories)
        
        ### **F - Flammable (Mudah Terbakar)**
        - Zat yang mudah terbakar pada suhu ruangan
        - Contoh: Etanol, Benzena, Aseton, Petroleum ether
        - Tanda bahaya: 🔥
        
        ### **C - Corrosive (Korosif)**
        - Zat yang merusak atau membakar jaringan hidup
        - Contoh: HCl, H2SO4, NaOH, KOH, HF
        - Tanda bahaya: 🧪
        
        ### **O - Oxidizer (Pengoksidasi)**
        - Zat yang mempercepat pembakaran zat lain
        - Contoh: KMnO4, H2O2, HNO3, Cl2, F2
        - Tanda bahaya: ⚡
        
        ### **T - Toxic (Beracun)**
        - Zat yang berbahaya bagi kesehatan manusia
        - Contoh: Hg, Pb, Sianida, Arsenikum
        - Tanda bahaya: ☠️
        """)
    
    with tab2:
        st.markdown("""
        ## 🌍 GHS (Globally Harmonized System)
        
        Standar internasional untuk klasifikasi dan pelabelan bahan kimia berbahaya.
        
        ### **GHS02 - Flammable** 🔥
        - Bahan yang mudah terbakar
        - Precautionary: Jauhkan dari panas, percikan, nyala api
        
        ### **GHS05 - Corrosive** 🧪
        - Bahan yang korosif untuk kulit/mata
        - Precautionary: Gunakan sarung tangan & kacamata
        
        ### **GHS03 - Oxidizing** ⚡
        - Bahan pengoksidasi
        - Precautionary: Terpisah dari bahan mudah terbakar
        
        ### **GHS06 - Acute Toxicity** ☠️
        - Bahan beracun akut
        - Precautionary: Hindari kontak langsung
        """)
    
    with tab3:
        st.markdown("""
        ## 📦 Panduan Penyimpanan Bahan Kimia
        
        ### Prinsip Umum:
        1. **Pisahkan Kategori** - Flammable, Oxidizer, Corrosive, Toxic
        2. **Ventilasi Baik** - Hindari penumpukan uap berbahaya
        3. **Suhu Terkontrol** - Jauh dari sumber panas >25°C
        4. **Wadah Tepat** - Sesuai jenis bahan kimia
        5. **Labeling Jelas** - Identifikasi mudah dan aman
        """)
    
    with tab4:
        st.markdown("""
        ## ❓ Pertanyaan Umum
        
        **Q: Apakah bahan kategori sama selalu aman?**
        A: Tidak selalu. Kompatibilitas tergantung sifat kimia spesifik setiap bahan.
        """)

elif menu == "🧪 Database":
    st.markdown("<h2 class='section-title'>🧪 Database Bahan Kimia (500+ Items)</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Cari bahan kimia", placeholder="Cth: HCl, Etanol...")
    with col2:
        db_list = [{"Nama": name, "Kategori": cat} for name, cat in chemical_db.items()]
        df_temp = pd.DataFrame(db_list)
        categories = st.multiselect("📂 Filter kategori", df_temp["Kategori"].unique(), default=df_temp["Kategori"].unique())
    with col3:
        sort_by = st.selectbox("📊 Urutkan", ["Nama A-Z", "Kategori"])
    
    filtered_df = pd.DataFrame([{"Nama": name, "Kategori": cat} for name, cat in chemical_db.items()])
    filtered_df = filtered_df[filtered_df["Kategori"].isin(categories)]
    
    if search:
        filtered_df = filtered_df[filtered_df["Nama"].str.contains(search, case=False, na=False)]
    
    if sort_by == "Nama A-Z":
        filtered_df = filtered_df.sort_values("Nama")
    else:
        filtered_df = filtered_df.sort_values("Kategori")
    
    st.info(f"📊 Menampilkan {len(filtered_df)} dari {len(chemical_db)} bahan kimia")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

elif menu == "⚙️ Pengaturan":
    st.markdown("<h2 class='section-title'>⚙️ Pengaturan Aplikasi</h2>", unsafe_allow_html=True)
    
    with st.expander("📊 Data & Privasi"):
        st.write("Data disimpan dalam session state lokal browser Anda (tidak dikirim ke server).")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Semua Data"):
                export_data = {
                    "history": st.session_state.history,
                    "favorites": st.session_state.favorites
                }
                export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
                st.download_button("Download JSON", export_json, f"backup_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        with col2:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.history = []
                st.session_state.favorites = []
                st.success("✅ Data dihapus!")
    
    with st.expander("ℹ️ Tentang Aplikasi"):
        st.markdown("""
        **FCOT Chemical System PRO v3.1**
        
        Aplikasi manajemen keamanan bahan kimia dengan fitur-fitur canggih:
        
        - Analisis kompatibilitas 500+ bahan kimia
        - Visualisasi 3D simbol bahaya GHS
        - Dashboard analytics komprehensif
        - **Sistem Favorit Lengkap** ⭐ (NEW!)
        - Export/Import data lengkap
        - Panduan interaktif FCOT & GHS
        
        **Fitur Favorit Baru:**
        - Simpan hasil analisis dengan detail lengkap
        - Filter & sort favorit
        - View detail hasil analisis
        - Export favorit ke JSON
        - Cegah duplikasi
        
        **Teknologi:**
        - Python 3.8+
        - Streamlit
        - Plotly
        - Pandas
        
        **Disclaimer:** Untuk operasi industri, konsultasi dengan ahli keselamatan profesional.
        """)
