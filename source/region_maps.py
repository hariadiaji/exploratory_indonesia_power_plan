# source/region_maps.py
# All comments in English.

# === Paste your current mappings here UNCHANGED ===

ISLAND_MAP = {
    "Sumatera": ["ACEH", "SUMATERA UTARA", "SUMATERA BARAT", "RIAU", "KEPULAUAN RIAU", "JAMBI", "BENGKULU", "BANGKA BELITUNG","SUMATERA SELATAN", "LAMPUNG"],
    "Kalimantan": ["KALIMANTAN BARAT", "KALIMANTAN TENGAH", "KALIMANTAN SELATAN", "KALIMANTAN TIMUR", "KALIMANTAN UTARA"],
    "Jawa": ["BANTEN", "DKI JAKARTA", "JAWA BARAT", "JAWA TENGAH", "DAERAH ISTIMEWA YOGYAKARTA", "JAWA TIMUR"],
    "Bali-Nusa": ["BALI", "NUSA TENGGARA BARAT", "NUSA TENGGARA TIMUR"],
    "Sulawesi": ["SULAWESI UTARA", "SULAWESI TENGAH", "SULAWESI BARAT", "SULAWESI SELATAN", "SULAWESI TENGGARA", "GORONTALO"],
    "Maluku-Papua": ["MALUKU", "MALUKU UTARA", "PAPUA", "PAPUA BARAT", "PAPUA TENGAH", "PAPUA PEGUNUNGAN", "PAPUA SELATAN", "PAPUA BARAT DAYA"]
}

# Keys = system name; Values = list of regionals (exact strings from 'system_measure_regional')
ISLAND_MEASURE_SYSTEM_MAP = {
    "JAWA BALI": [
        "JAKARTA BANTEN", "JAWA BARAT", "JAWA TENGAH YOGYAKARTA", "JAWA TIMUR", "BALI"
    ],
    "SUMATERA": ["ACEH","SUMATERA UTARA","SUMATERA BARAT", "RIAU" ,"SUMATERA SELATAN","JAMBI", "BANGKA", "BENGKULU","LAMPUNG" 
    ],
    "KALIMANTAN": [
        "KALIMANTAN BARAT KHATULISTIWA", "KALIMANTAN BARAT KETAPANG", "KALIMANTAN SELATAN TENGAH", "KALIMANTAN TIMUR"
    ],
    "SULAWESI": [
        "SUL - MAKASSAR", "SULAWESI - UTARA"
    ],
    "NUSA TENGGARA": [
        "NTB - LOMBOK", "NTB - TAMBORA", "NTT - FLORES", "NTT - TIMOR"
    ]

    # add more systems...
}

# We use Parent_ORDER to order the systems in visualizations and Demand grouping
PARENT_ORDER = ["JAWA BALI", "SUMATERA", "KALIMANTAN", "SULAWESI", "NUSA TENGGARA"]


# For Future Demand Projection. Relate Real province to system_measure_regional
# PROVINCE : SYSTEM_MEASURE_REGIONAL
PROVINCE_TO_SYSTEM_MEASURE = {
    "ACEH" : "ACEH", 
    "SUMATERA UTARA": "SUMATERA UTARA",
    "SUMATERA BARAT": "SUMATERA BARAT", 
    "KEPULAUAN RIAU": "RIAU", 
    "JAMBI": "JAMBI", 
    "BENGKULU": "BENGKULU", 
    "BANGKA BELITUNG": "BANGKA",
    "SUMATERA SELATAN": "SUMATERA SELATAN", 
    "LAMPUNG": "LAMPUNG",

    "BANTEN": "JAKARTA BANTEN", 
    "DKI JAKARTA": "JAKARTA BANTEN",
    "JAWA BARAT": "JAWA BARAT", 
    "JAWA TENGAH": "JAWA TENGAH YOGYAKARTA", 
    "DAERAH ISTIMEWA YOGYAKARTA": "JAWA TENGAH YOGYAKARTA", 
    "JAWA TIMUR": "JAWA TIMUR",

    "KALIMANTAN BARAT": "KALIMANTAN BARAT KHATULISTIWA", 
    "KALIMANTAN TENGAH": "KALIMANTAN SELATAN TENGAH", 
    "KALIMANTAN SELATAN": "KALIMANTAN SELATAN TENGAH", 
    "KALIMANTAN TIMUR" : "KALIMANTAN TIMUR", 
    "KALIMANTAN UTARA": "KALIMANTAN TIMUR",

    "SULAWESI UTARA" : "SULAWESI - UTARA", 
    "SULAWESI TENGAH": "SUL - MAKASSAR", 
    "SULAWESI BARAT": "SUL - MAKASSAR", 
    "SULAWESI SELATAN": "SUL - MAKASSAR", 
    "SULAWESI TENGGARA":  "SUL - MAKASSAR", 
    "GORONTALO": "SULAWESI - UTARA",

    "BALI": "BALI", 
    "NUSA TENGGARA BARAT": "NTB - LOMBOK", 
    "NUSA TENGGARA TIMUR": "NTT - FLORES"


}

SYSTEM_MAP = {
    # === JAMALI (Jawa + Bali) ===
    "Jamali": [
        "BANTEN", "DKI JAKARTA", "JAWA BARAT",
        "JAWA TENGAH", "DI YOGYAKARTA", "DAERAH ISTIMEWA YOGYAKARTA",
        "JAWA TIMUR", "BALI"
    ],

    # === SUMATERA ===
    "Sumatera": [
        "ACEH", "SUMATERA UTARA", "SUMATERA BARAT",
        "RIAU", "KEPULAUAN RIAU", "JAMBI", "BENGKULU",
        "BANGKA BELITUNG", "SUMATERA SELATAN", "LAMPUNG"
    ],

    # === KHATULISTIWA (KALBAR only) ===
    "Khatulistiwa": ["KALIMANTAN BARAT"],

    # === SISTEM KALIMANTAN (All except Kalbar) ===
    "Sistem Kalimantan": [
        "KALIMANTAN TENGAH", "KALIMANTAN SELATAN",
        "KALIMANTAN TIMUR", "KALIMANTAN UTARA"
    ],

    # === SULUTGO (Utara + Tengah) ===
    "Sulbagut": [
        "SULAWESI UTARA", "SULAWESI TENGAH", "GORONTALO"
    ],

    # === SULSEL RABAR (Barat + Selatan + Tenggara) ===
    "Sulbagsel": [
        "SULAWESI BARAT", "SULAWESI SELATAN", "SULAWESI TENGGARA"
    ],

    # === INDIVIDUAL SYSTEMS (others) ===
    # These are isolated systems per province
    "NTB": ["NUSA TENGGARA BARAT"],
    "NTT": ["NUSA TENGGARA TIMUR"],
    "MA": ["MALUKU"],
    "MALUT": ["MALUKU UTARA"],
    "PP": ["PAPUA"],
    "PPBRT": ["PAPUA BARAT"],
    "Papua Tengah": ["PAPUA TENGAH"],
    "Papua Pegunungan": ["PAPUA PEGUNUNGAN"],
    "Papua Selatan": ["PAPUA SELATAN"],
    "Papua Barat Daya": ["PAPUA BARAT DAYA"]
}

def get_ordered_provinces():
    """Return a flat list of provinces ordered by SYSTEM_MAP keys."""
    ordered = []
    for system, prov_list in SYSTEM_MAP.items():
        ordered.extend(prov_list)
    return ordered