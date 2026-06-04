def get_chemical_database():
    base = {
        "HCl - Asam Klorida": "Corrosive",
        "H2SO4 - Asam Sulfat": "Corrosive",
        "HNO3 - Asam Nitrat": "Oxidizer",
        "NaOH - Natrium Hidroksida": "Corrosive",
        "KOH - Kalium Hidroksida": "Corrosive",
        "KMnO4 - Kalium Permanganat": "Oxidizer",
        "H2O2 - Hidrogen Peroksida": "Oxidizer",
        "Etanol - Alkohol": "Flammable",
        "Benzena - Benzene": "Flammable",
        "Aseton - Acetone": "Flammable",
        "Hg - Merkuri": "Toxic",
        "Pb - Timbal": "Toxic",
        "NaCl - Natrium Klorida": "Safe",
        "KCl - Kalium Klorida": "Safe",
        "CaCl2 - Kalsium Klorida": "Safe",
    }
    chemical_db = {}
    for i in range(5):
        for k, v in base.items():
            if i == 0:
                chemical_db[k] = v
            else:
                chemical_db[f"{k} (Grade {i})"] = v
    return chemical_db

def get_ghs_images():
    return {
        "Flammable": "https://upload.wikimedia.org/wikipedia/commons/6/6c/GHS-pictogram-flamme.svg",
        "Corrosive": "https://upload.wikimedia.org/wikipedia/commons/5/5a/GHS-pictogram-acid.svg",
        "Oxidizer": "https://upload.wikimedia.org/wikipedia/commons/1/1c/GHS-pictogram-rondflam.svg",
        "Toxic": "https://upload.wikimedia.org/wikipedia/commons/3/3b/GHS-pictogram-skull.svg",
        "Safe": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning_sign.svg/320px-Warning_sign.svg.png"
    }
