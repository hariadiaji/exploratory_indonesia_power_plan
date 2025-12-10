"""
Global constants for generation technology labels and colors.
Color-blind-friendly palette (Okabe–Ito / CUD), harmonized across all plots.
Categorized by conversion technology (turbine / engine type).
"""

# ==============================================================
# 1. LABEL MAPPING — PLN technology code (Indonesia) → English academic name
# ==============================================================

GENERATION_LABELS = {
    "PLTA": "Hydro",
    "PLTAL": "Tidal / Ocean Current",
    "PLTB": "Wind",
    "PLTBg": "Biogas",
    "PLTBm": "Biomass",
    "PLTD": "Diesel Engine",
    "PLTDG": "Diesel-Gas Hybrid",
    "PLTG": "Gas Turbine (OCGT)",
    "PLTG/MG": "Gas Turbine / Engine Hybrid",
    "PLTGU": "Combined Cycle (CCGT)",
    "PLTM": "Mini Hydro",
    "PLTMH": "Micro Hydro",
    "PLTMG": "Gas Engine",
    "PLTP": "Geothermal",
    "PLTS": "Solar PV",
    "PLTSa": "Waste-to-Energy",
    "PLTS-f": "Floating Solar PV",
    "PLTS BESS": "Solar PV + Battery",
    "PLTB BESS": "Wind + Battery",
    "PS": "Pumped Storage (Hydro)",
    "BESS": "BESS",
    "PLTN": "Nuclear",
    "PLTU": "Coal",
    "PLTU MT": "Coal (Mine Mouth)",
    "lain-lain": "Other",
}

# ==============================================================
# 2. COLOR PALETTE — consistent, color-blind-friendly colors
# ==============================================================

GENERATION_COLORS = {
    # --- Solar ---
    "PLTS": "#E1B700",       # warm golden yellow
    "PLTS-f": "#E6C642",     # floating solar (lighter)
    "PLTSa": "#DDBB4B",      # solar w/ agriculture
    "PLTS BESS": "#C9A53C",  # solar + battery

    # --- Wind ---
    "PLTB": "#009ADE",       # sky blue (strong contrast)
    "PLTB BESS": "#3DB7E9",  # lighter blue for hybrid

    # --- Hydro / Ocean ---
    "PLTA": "#4477AA",
    "PLTM": "#66AADD",
    "PLTMH": "#88CCEE",
    "PLTAL": "#336699",      # tidal
    "PS": "#5588BB",         # pumped storage

    # --- Geothermal ---
    "PLTP": "#B35C1E",       # brown-orange

    # --- Bioenergy ---
    "PLTBm": "#7BAF00",      # green (biomass)
    "PLTBg": "#669900",      # biogas

    # === Fossil Families ===

    # --- Coal (steam-based) ---
    "PLTU": "#3C3C3C",       # deep charcoal black
    "PLTU MT": "#5A4638",    # mine-mouth brownish gray

    # --- Gas (turbine-based) ---
    "PLTG": "#E07A1F",       # warm orange (OCGT)
    "PLTGU": "#F29E38",      # amber-golden (CCGT)
    "PLTG/MG": "#E68A00",    # hybrid turbine/engine
    "PLTMG": "#D66B00",      # deeper orange-brown for reciprocating gas engine

    # --- Diesel (engine-based) ---
    "PLTD": "#6E6E6E",       # mid-gray steel
    "PLTDG": "#8C8C8C",      # light metallic gray

    # --- Nuclear ---
    "PLTN": "#7057A3",       # purple-indigo

    # --- Storage ---
    "BESS": "#006400",       # dark green

    # --- Misc ---
    "lain-lain": "#BBBBBB",
}

# ==============================================================
# 3. COMBINED REGISTRY
# ==============================================================

GENERATION_INFO = {
    code: {
        "label": GENERATION_LABELS.get(code, code),
        "color": GENERATION_COLORS.get(code, "#CCCCCC")
    }
    for code in GENERATION_LABELS.keys()
}

# ==============================================================
# 4. CATEGORY MAPPING — grouped by turbine / engine technology
# ==============================================================

GENERATION_CATEGORY = {
    # PV and storage
    "PLTS": "Solar PV",
    "PLTS-f": "Solar PV",
    "PLTSa": "Bioenergy (Steam)",
    "PLTS BESS": "Solar PV",
    "BESS": "BESS",

    # Wind
    "PLTB": "Wind",
    "PLTB BESS": "Wind",

    # Hydro and marine
    "PLTA": "Hydro",
    "PLTM": "Hydro",
    "PLTMH": "Hydro",
    "PLTAL": "Ocean Current",
    "PS": "Hydro",

    # Geothermal
    "PLTP": "Geothermal (Steam)",

    # Bioenergy
    "PLTBm": "Bioenergy (Steam)",
    "PLTBg": "Bioenergy (Engine)",

    # Fossil Gas Turbine
    "PLTG": "Fossil Gas (Turbine)",
    "PLTGU": "Fossil Gas (Combined Cycle)",
    "PLTG/MG": "Fossil Gas (Hybrid)",

    # Fossil Steam
    "PLTU": "Fossil Steam (Coal)",
    "PLTU MT": "Fossil Steam (Coal)",

    # Diesel / Engine-based
    "PLTD": "Diesel (Engine)",
    "PLTDG": "Diesel (Engine Hybrid)",
    "PLTMG": "Diesel (Gas Engine)",

    # Nuclear
    "PLTN": "Nuclear (Steam)",

    # Miscellaneous
    "lain-lain": "Other",
    "Jumlah Total": "Total",
}

# ==============================================================
# 5. Helper functions
# ==============================================================

def get_label(code: str) -> str:
    """Return English label for PLN generation code."""
    return GENERATION_LABELS.get(code, code)

def get_color(code: str) -> str:
    """Return hex color for PLN generation code."""
    return GENERATION_COLORS.get(code, "#CCCCCC")

def get_info(code: str) -> dict:
    """Return both label and color as a dictionary."""
    return GENERATION_INFO.get(code, {"label": code, "color": "#CCCCCC"})

def get_palette(codes: list[str]) -> list[str]:
    """Return color list in the same order as given codes."""
    return [get_color(c) for c in codes]




# ==============================================================
# RUPTL Bucket Categories (Grouping PLN technologies → RUPTL buckets)
# ==============================================================

BUCKET_GENERATION_RUPTL = {
    
    # ---------------- SOLAR PV ----------------
    "SOLAR": {
        "color": GENERATION_COLORS["PLTS"],   # kuning
        "members": [
            "PLTS",       # Solar PV
            "PLTS-f",     # Floating PV
            "PLTS BESS",  # Solar + battery hybrid
            "PLTSa",      # agro-solar (opsional, bisa masuk bio)
        ]
    },

    # ---------------- WIND ----------------
    "WIND": {
        "color": GENERATION_COLORS["PLTB"],   # biru langit
        "members": [
            "PLTB",
            "PLTB BESS",
        ]
    },

    # ---------------- HYDRO & PUMPED STORAGE ----------------
    "HYDRO": {
        "color": GENERATION_COLORS["PLTA"],
        "members": [
            "PLTA",
            "PLTM",
            "PLTMH",
            "PLTA PS",        # pumped storage
            "PLTAL",     # ocean current
        ]
    },

    # ---------------- GEOTHERMAL ----------------
    "GEOTHERMAL": {
        "color": GENERATION_COLORS["PLTP"],
        "members": [
            "PLTP",
        ]
    },

    # ---------------- BIOENERGY ----------------
    "BIOENERGY": {
        "color": GENERATION_COLORS["PLTBm"],   # hijau biomassa
        "members": [
            "PLTBm",
            "PLTBg",
            "PLTSa",   
        ]
    },

    # ---------------- COAL ----------------
    "COAL": {
        "color": GENERATION_COLORS["PLTU"],    # charcoal black
        "members": [
            "PLTU",
            "PLTU MT",
        ]
    },

    # ---------------- GAS ----------------
    "GAS": {
        "color": GENERATION_COLORS["PLTGU"],   # amber/CCGT
        "members": [
            "PLTG",
            "PLTGU",
            "PLTG/MG",
            "PLTMG",
        ]
    },

    # ---------------- DIESEL ----------------
    "DIESEL": {
        "color": GENERATION_COLORS["PLTD"],    # gray steel
        "members": [
            "PLTD",
            "PLTDG",
        ]
    },

    # ---------------- NUCLEAR ----------------
    "NUCLEAR": {
        "color": GENERATION_COLORS["PLTN"],    
        "members": [
            "PLTN",
        ]
    },

    # ---------------- STORAGE ----------------
    "BESS": {
        "label": "BESS (GWh)",
        "color": GENERATION_COLORS["BESS"],
        "members": [
            "BESS",
        ]
    },

    # ---------------- OTHER ----------------
    "OTHER": {
        "color": "#BBBBBB",
        "members": [
            "lain-lain",
        ]
    },
}



# ==============================================================
# RUKN 2060 — Color Map for Future Technology Types
# ==============================================================

RUKN_GENERATION_COLORS = {

    # ---------------- Variable Renewable Energy ----------------
    "PLTS": GENERATION_COLORS["PLTS"],              # Solar PV (yellow)
    "PLTB": GENERATION_COLORS["PLTB"],              # Wind (sky blue)
    "PLTAL": GENERATION_COLORS["PLTAL"],            # Ocean current (blue)
    
    # ---------------- Hydro ----------------
    "PLTA": GENERATION_COLORS["PLTA"],              # Dispatchable hydro

    # ---------------- Coal Variants ----------------
    # Base coal: #3C3C3C → derivative colors:
    "PLTU NH3": "#505070",                          # Coal + Ammonia (coal + blue tint)
    "PLTU cofiring biomassa dan CCS": "#546B4F",    # Coal + Biomass + CCS (coal + green tint)

    # ---------------- Geothermal ----------------
    "PLTP": GENERATION_COLORS["PLTP"],              # Geothermal (brown-orange)

    # ---------------- Gas Family Variants ----------------
    # Base gas colors: OCGT (#E07A1F) / CCGT (#F29E38)
    "PLTG/PLTGU/PLTMG/PLTMGU H2": "#D9A066",        # Hydrogen gas turbine (hydrogen blue)
    "PLTG/PLTGU/PLTMG/PLTMGU + CCS": "#D4841A",     # Gas + CCS (deeper amber)
    "PLTG/PLTGU/PLTMG/PLTMGU (konvensional)": GENERATION_COLORS["PLTGU"],   # Conventional CCGT

    # ---------------- Bioenergy ----------------
    "PLTBio": "#4F7A00",                            # Bioenergy gas engine (dark biomass green)

    # ---------------- Nuclear ----------------
    "PLTN": GENERATION_COLORS["PLTN"],              # Nuclear purple

    # ---------------- Waste Heat ----------------
    "Waste heat": "#A89F8C",                        # Warm grey / industrial surplus heat
}


# ==============================================================
# RUKN 2060 — English Labels for Legend
# ==============================================================

RUKN_LABELS = {
    "PLTS": "Solar PV",
    "PLTB": "Wind",
    "PLTAL": "Ocean",
    "PLTA": "Hydro",

    "PLTU NH3": "Coal + Ammonia Blending",
    "PLTU cofiring biomassa dan CCS": "Coal + Biomass Cofiring + CCS",

    "PLTP": "Geothermal",

    "PLTG/PLTGU/PLTMG/PLTMGU (konvensional)": "Gas Turbine (Conventional)",
    "PLTG/PLTGU/PLTMG/PLTMGU + CCS": "Gas Turbine + CCS",
    "PLTG/PLTGU/PLTMG/PLTMGU H2": "Gas Turbine - Hydrogen",

    "PLTBio": "Bioenergy",

    "PLTN": "Nuclear",

    "Waste heat": "Waste Heat Recovery",
}