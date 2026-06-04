def analyze_compatibility(t1, t2):
    categories = [t1, t2]
    
    if "Flammable" in categories and "Oxidizer" in categories:
        return ("❌ BERBAHAYA", "Kombinasi Flammable + Oxidizer sangat berbahaya! Flammable akan mempercepat pembakaran, Oxidizer akan meningkatkan intensitas api → ledakan atau kebakaran besar.", "🚨 PISAHKAN KETAT! Jangan simpan di area yang sama. Gunakan cabinet terpisah dan jauh dari sumber panas/api.")
    elif "Corrosive" in categories and "Toxic" in categories:
        return ("❌ BERBAHAYA", "Corrosive dapat merusak wadah → Toxic bocor. Kombinasi ini sangat bahaya untuk lingkungan kerja.", "🚨 Gunakan SECONDARY CONTAINMENT (wadah berlapis). Simpan di ventilasi khusus dengan monitoring ketat.")
    elif "Oxidizer" in categories and "Toxic" in categories:
        return ("❌ BERBAHAYA", "Oxidizer mempercepat reaksi → gas beracun meningkat drastis. Inhalasi dapat fatal.", "🚨 PISAHKAN KETAT! Gunakan fume hood khusus dan ventilasi eksternal ke luar gedung.")
    elif "Flammable" in categories and "Toxic" in categories:
        return ("⚠️ PERLU PERHATIAN", "Kombinasi ini memiliki risiko ganda: kebakaran + gas beracun. Jika terbakar, asap akan sangat beracun.", "⚠️ Ventilasi SANGAT BAIK diperlukan. Simpan dalam wadah tertutup rapat. Jauh dari sumber panas. Siapkan alat pemadam api khusus.")
    elif "Corrosive" in categories and "Flammable" in categories:
        return ("⚠️ PERLU PERHATIAN", "Corrosive dapat merusak/bocor dari wadah → Flammable tumpah → api. Risiko sedang-tinggi.", "⚠️ Gunakan WADAH TAHAN KOROSI. Simpan terpisah. Area dengan ventilasi baik dan jauh dari api.")
    elif "Corrosive" in categories and "Oxidizer" in categories:
        return ("⚠️ PERLU PERHATIAN", "Kedua zat reaktif. Oxidizer + asam dapat menciptakan reaksi eksplosif.", "⚠️ Simpan TERPISAH dengan minimal 2 meter jarak. Gunakan wadah tahan korosi/asam.")
    elif t1 == t2 and t1 != "Safe":
        return ("✅ RELATIF AMAN", f"Kedua bahan termasuk kategori {t1} yang sama. Sifat kimia serupa sehingga kompatibel.", f"📦 Dapat disimpan bersama dalam area penyimpanan {t1}. Tetap perhatikan ventilasi dan suhu ruang.")
    elif t1 == "Safe" or t2 == "Safe":
        return ("✅ AMAN", "Salah satu atau kedua bahan adalah kategori Safe (tidak berbahaya). Kombinasi aman.", "📦 Dapat disimpan bersama di lokasi penyimpanan normal. Perhatikan regulasi penyimpanan umum.")
    else:
        return ("⚠️ PERLU PERHATIAN", f"Kombinasi {t1} dan {t2}. Meski tidak seserius kombinasi lain, tetap ada potensi interaksi. Perlu monitoring.", "⚠️ Simpan TERPISAH (minimal 1 meter). Gunakan SECONDARY CONTAINMENT untuk precaution. Pastikan label jelas.")
