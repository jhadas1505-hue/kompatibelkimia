import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from database import get_chemical_database, get_ghs_images
from analyzer import analyze_compatibility
from pdf_export import generate_compatibility_pdf, generate_history_pdf
from data_manager import DataManager
import io

# Initialize data manager
dm = DataManager()

st.set_page_config(
    page_title="CHECKCOMCHEMISTRY PRO",
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
    
    .info-box {
        background: #0f3460;
        border-left: 5px solid #00d4ff;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #eaeaea;
    }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

st.sidebar.markdown("""
<div style='text-align:center; padding:20px 0;'>
    <h1 style='font-size:40px; margin:0;'>🧪</h1>
    <h2 style='font-size:20px; margin:5px 0; color:#00d4ff;'>CheckcomChemistry PRO</h2>
    <p style='font-size:12px; color:#ffa500;'>v2.0 - Advanced Edition</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 MENU UTAMA",
    ["🏠 Home", "🔍 Cek Kompatibilitas", "📊 Dashboard", "❤️ Favorit", "📝 Catatan", "📚 Panduan", "🧪 Database", "⚙️ Pengaturan"]
)

if menu == "🏠 Home":
    st.markdown("<div class='main-title'>🧪 CHECKCOMCHEMISTRY PRO</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h3 style='color:#00d4ff;'>🎯 Selamat Datang di Checkcomchemistry PRO</h3>
        <p>Versi Enhanced dengan fitur PDF Export, Data Persistence, dan Advanced Analytics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get statistics
    stats = dm.get_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Total Analisis", stats['total_analysis'])
    with col2:
        st.metric("🔴 Berbahaya", stats['dangerous'])
    with col3:
        st.metric("🟢 Aman", stats['safe'])
    with col4:
        st.metric("🟡 Perlu Perhatian", stats['warning'])
    with col5:
        st.metric("❤️ Favorit", stats['favorites'])
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🚀 Fitur Utama
        - Cek kompatibilitas 500+ bahan kimia
        - 📄 **NEW:** Export hasil sebagai PDF
        - 💾 **NEW:** Simpan history ke database
        - 📊 Advanced analytics komprehensif
        - 📝 **NEW:** Buat catatan analisis
        - Export data mudah (CSV/JSON)
        """)
    
    with col2:
        st.markdown("""
        ### 🛡️ Keamanan
        - Standar GHS terintegrasi penuh
        - Alert sistem real-time
        - Panduan penanganan lengkap
        - Simpan favorit & histori
        - 💾 **NEW:** Data persisten
        - Support 500+ kombinasi
        """)

elif menu == "🔍 Cek Kompatibilitas":
    st.markdown("<h2 class='section-title'>🔍 Cek Kompatibilitas Bahan Kimia</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    ghs_images = get_ghs_images()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Bahan Kimia 1** 🧪")
        chem1 = st.selectbox("Pilih bahan pertama", list(chemical_db.keys()), key="chem1", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Bahan Kimia 2** 🧪")
        chem2 = st.selectbox("Pilih bahan kedua", list(chemical_db.keys()), key="chem2", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        check_btn = st.button("✅ Cek Sekarang", use_container_width=True, key="check_btn")
    with col2:
        clear_all = st.button("🧹 Hapus Semua", use_container_width=True, key="clear_all_btn")
    with col3:
        add_note_btn = st.button("📝 Tambah Catatan", use_container_width=True, key="add_note_btn")
    
    if clear_all:
        st.session_state.history = []
        st.success("✅ Semua data riwayat dihapus!")
        st.rerun()
    
    if check_btn:
        with st.spinner("🔬 Menganalisis kombinasi bahan kimia..."):
            import time
            time.sleep(1.2)
        
        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]
        status, penjelasan, penyimpanan = analyze_compatibility(t1, t2)
        
        # Save to database
        dm.save_analysis(chem1, chem2, t1, t2, status, status.replace("❌ ", "").replace("⚠️ ", "").replace("✅ ", ""))
        
        st.session_state.last_analysis = {
            'chem1': chem1,
            'chem2': chem2,
            'cat1': t1,
            'cat2': t2,
            'status': status,
            'penjelasan': penjelasan,
            'penyimpanan': penyimpanan
        }
        
        status_class = "safe" if "AMAN" in status else ("danger" if "BERBAHAYA" in status else "warning")
        
        st.markdown(f"<div class='status-card {status_class}'>{status}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chemical-card'>", unsafe_allow_html=True)
            st.image(ghs_images.get(t1, ""), width=100, use_column_width=True)
            st.markdown(f"""
            <div style='color:#00d4ff; font-weight:bold; margin-top:15px;'>{chem1}</div>
            <div style='color:#ffa500; font-size:12px; margin-top:8px;'>{t1}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chemical-card'>", unsafe_allow_html=True)
            st.image(ghs_images.get(t2, ""), width=100, use_column_width=True)
            st.markdown(f"""
            <div style='color:#00d4ff; font-weight:bold; margin-top:15px;'>{chem2}</div>
            <div style='color:#ffa500; font-size:12px; margin-top:8px;'>{t2}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧠 Penjelasan Hasil")
            st.info(penjelasan)
        
        with col2:
            st.markdown("### 📦 Rekomendasi Penyimpanan")
            st.warning(penyimpanan)
        
        st.markdown("---")
        
        record = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Bahan 1": chem1,
            "Bahan 2": chem2,
            "Kategori 1": t1,
            "Kategori 2": t2,
            "Hasil": status.replace("❌ ", "").replace("⚠️ ", "").replace("✅ ", ""),
        }
        st.session_state.history.append(record)
        
        # Download buttons
        st.markdown("### 📥 Download Hasil")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pdf_buffer = generate_compatibility_pdf(chem1, chem2, t1, t2, status, penjelasan, penyimpanan)
            st.download_button(
                "📄 Download PDF",
                pdf_buffer,
                file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        
        with col2:
            if st.button("❤️ Tambah ke Favorit"):
                fav = f"{chem1} + {chem2}"
                dm.save_favorite(fav)
                st.success("✅ Ditambahkan ke favorit!")
        
        with col3:
            if st.button("📋 Copy Hasil"):
                st.info(f"**Bahan 1:** {chem1} ({t1})\n\n**Bahan 2:** {chem2} ({t2})\n\n**Status:** {status}")

elif menu == "📊 Dashboard":
    st.markdown("<h2 class='section-title'>📊 Dashboard Analytics</h2>", unsafe_allow_html=True)
    
    df = dm.get_all_analysis()
    
    if len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Analisis", len(df))
        
        bahaya = len(df[df["status"].str.contains("BERBAHAYA", na=False)])
        with col2:
            st.metric("🔴 Berbahaya", bahaya)
        
        aman = len(df[df["status"].str.contains("AMAN", na=False)])
        with col3:
            st.metric("🟢 Aman", aman)
        
        perhatian = len(df[df["status"].str.contains("PERHATIAN", na=False)])
        with col4:
            st.metric("🟡 Perlu Perhatian", perhatian)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 class='section-title'>📈 Distribusi Hasil Analisis</h3>", unsafe_allow_html=True)
            result_counts = df["status"].value_counts()
            fig = px.pie(values=result_counts.values, names=result_counts.index, color_discrete_map={"BERBAHAYA": "#ff006e", "AMAN": "#00d97e", "PERLU PERHATIAN": "#ffa500"})
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<h3 class='section-title'>🧪 Kategori Bahan Terpopuler</h3>", unsafe_allow_html=True)
            all_cats = pd.concat([df["category_1"], df["category_2"]])
            cat_counts = all_cats.value_counts().head(8)
            fig = px.bar(x=cat_counts.index, y=cat_counts.values, labels={"x": "Kategori", "y": "Frekuensi"}, color_discrete_sequence=["#00d4ff"])
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📋 Riwayat Analisis</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, f"fcot_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        with col2:
            json_str = df.to_json(orient="records")
            st.download_button("📥 Download JSON", json_str, f"fcot_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        with col3:
            pdf_buffer = generate_history_pdf(df)
            st.download_button("📄 Download PDF Report", pdf_buffer, f"fcot_report_{datetime.now().strftime('%Y%m%d')}.pdf", "application/pdf")
        with col4:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.history = []
                st.rerun()
    else:
        st.info("📭 Belum ada data analisis. Mulai dengan melakukan pengecekan kompatibilitas!")

elif menu == "❤️ Favorit":
    st.markdown("<h2 class='section-title'>❤️ Favorit Analisis</h2>", unsafe_allow_html=True)
    
    favorites = dm.get_favorites()
    
    if favorites:
        st.success(f"✅ Total {len(favorites)} favorit tersimpan")
        for i, fav in enumerate(favorites):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{i+1}. {fav}**")
            with col2:
                if st.button("❌", key=f"del_{i}"):
                    dm.delete_favorite(fav)
                    st.rerun()
    else:
        st.info("📭 Tidak ada favorit. Tambahkan saat melakukan pengecekan kompatibilitas!")

elif menu == "📝 Catatan":
    st.markdown("<h2 class='section-title'>📝 Catatan Analisis</h2>", unsafe_allow_html=True)
    
    with st.form("note_form"):
        st.markdown("### Buat Catatan Baru")
        title = st.text_input("Judul Catatan")
        content = st.text_area("Isi Catatan", height=150)
        submit = st.form_submit_button("💾 Simpan Catatan")
        
        if submit and title and content:
            dm.save_note(title, content)
            st.success("✅ Catatan berhasil disimpan!")
    
    st.markdown("---")
    st.markdown("### Catatan Tersimpan")
    
    notes_df = dm.get_notes()
    
    if len(notes_df) > 0:
        for idx, row in notes_df.iterrows():
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{row['title']}**")
                    st.write(row['content'])
                    st.caption(f"📅 {row['timestamp']}")
                with col2:
                    if st.button("🗑️", key=f"note_{idx}"):
                        # Delete note functionality
                        st.info("Fitur delete akan ditambahkan")
                st.markdown("---")
    else:
        st.info("📝 Belum ada catatan. Mulai buat catatan baru!")

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
        
        **Q: Bagaimana cara menggunakan PDF export?**
        A: Setelah analisis, klik tombol "Download PDF" untuk mendapatkan laporan profesional.
        
        **Q: Apakah data saya tersimpan?**
        A: Ya! Semua data disimpan di database lokal dan tidak hilang meski aplikasi ditutup.
        
        **Q: Bagaimana backup data?**
        A: Buka Settings > Backup & Restore > Export JSON untuk backup lengkap.
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
        st.write("Data disimpan dalam SQLite database lokal (tidak dikirim ke server).")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Semua Data (JSON)"):
                filename = dm.export_to_json()
                st.success(f"✅ Data berhasil di-export ke: {filename}")
        with col2:
            if st.button("🗑️ Hapus Semua Data"):
                st.warning("⚠️ Aksi ini akan menghapus semua data secara permanen!")
                if st.button("Konfirmasi Hapus"):
                    st.session_state.history = []
                    st.success("✅ Data dihapus!")
    
    with st.expander("📄 Tentang Versi"):
        st.markdown("""
        **FCOT Chemical System PRO v2.0**
        
        ### New Features:
        - ✅ PDF Export untuk hasil analisis
        - ✅ SQLite Database untuk data persistence
        - ✅ Fitur catatan (notes)
        - ✅ Advanced PDF Report untuk history
        - ✅ Statistics tracking
        - ✅ Import/Export JSON
        
        ### Technology Stack:
        - Python 3.8+
        - Streamlit
        - Plotly
        - Pandas
        - ReportLab (PDF)
        - SQLite3
        
        ### Disclaimer:
        Untuk operasi industri, konsultasi dengan ahli keselamatan profesional.
        """)
    
    with st.expander("ℹ️ Informasi Sistem"):
        stats = dm.get_statistics()
        st.json(stats)
