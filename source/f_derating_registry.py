
# f_derating_registry.py
# this is the place of every derating registries defined
# will be called by f2 functions for assigning parameters to gen/trans assets.
# will also be called by f3 functions for executing derating calculation.

import numpy as np

# === GLOBAL DEFAULTS ===

# Gas derating with 1.15 equation
GLOBAL_ALPHA = 0.0083 #Bartos and Chester, 2015

# Open Cycle Gas derating
GLOBAL_ALPHA_OCGT = 0.006 #Handayani, 2019 0.6% Muarakarang
GLOBAL_TREF_OCGT = 16.0 #Celsius

# Combined Cycle Gas derating
GLOBAL_ALPHA_CCGT = 0.0045 #Handayani, 2019 0.34% Muarakarang
GLOBAL_TREF_CCGT = 16.0 #Celsius

# PV derating
GLOBAL_EPSILON = 0.004  # PV temp coefficient, mono-Si P type (Junko Database)
GLOBAL_IRRADIANCE = 1000  # W/m2 , Bartos and Chester, 2015, also apply to Indonesia
GLOBAL_TREF = 25 #test condition

#coal derating (Petrakopolou, 2020)
# pertrakopolou alpha = 0.006, T_ref = 25 Celsius
GLOBAL_ALPHA_COAL = 0.0034  # Derating factor per degree Celsius above T_ref
GLOBAL_TREF_COAL = 25  # Reference temperature for coal derating in Celsius

# Nuclear derating
GLOBAL_ALPHA_NUCLEAR = 0.0044 #Attia, 2015, with T_ref = 25 Celsius
GLOBAL_TREF_NUCLEAR = 25  # 

# Diesel derating # based on Cummins 1200 kW diesel generator specification, small diesel.
GLOBAL_TREF_DIESEL_CUMMINS = 35.0  # Celsius
GLOBAL_TMAX_DIESEL_CUMMINS = 45.0  # Celsius
GLOBAL_MMIN_DIESEL_CUMMINS = 0.69  # Minimum multiplier at TMAX

# Diesel derating from Wartsila specification, for larger diesel genset 
GLOBAL_ALPHA_DIESEL_AMB = 0.005     # 0.5% per °C
GLOBAL_TREF_DIESEL      = 25.0      # °C

GLOBAL_ALPHA_ALT_PER_M  = 0.0001    # 1% per 100 m
GLOBAL_ALT_REF_DIESEL   = 0.0       # m

GLOBAL_ALPHA_DIESEL_CAC = 0.004     # 0.4% per °C (optional)
GLOBAL_TREF_CAC         = 25.0      # °C


# Transmission derating
GLOBAL_EMISSIVITY = 0.9 #
GLOBAL_ABSORPTIVITY = 0.5 #
GLOBAL_SOLAR_RAD = 500  # W/m2
GLOBAL_T_CONDUCTOR = 90  # Celsius
GLOBAL_SIGMA = 5.67e-8  # Stefan–Boltzmann constant

# === DERATING FUNCTIONS ===

def gas_derating(tasmax_values, daya_mw, alpha, **kwargs):
    if alpha == "glob":
        alpha = GLOBAL_ALPHA
    return [daya_mw * (-alpha * t + 1.15) for t in tasmax_values]

def oc_gas_derating(tasmax_values, daya_mw, alpha_ocgt="glob", T_ref_ocgt="glob", **kwargs):
    """
    Derating function for gas turbine (OCGT).
    Power decreases linearly with temperature above reference temperature.
    Source: Handayani 2019, Bartos, and Chester (2017)
    """
    if alpha_ocgt == "glob":
        alpha_ocgt = GLOBAL_ALPHA_OCGT
    if T_ref_ocgt == "glob":
        T_ref_ocgt = GLOBAL_TREF_OCGT

    return [daya_mw * (1 - alpha_ocgt * max(0, T - T_ref_ocgt)) for T in tasmax_values]

def cc_gas_derating(tasmax_values, daya_mw, alpha_ccgt="glob", T_ref_ccgt="glob", **kwargs):
    """
    Derating function for gas turbine (OCGT).
    Power decreases linearly with temperature above reference temperature.
    Source: Handayani 2019, Bartos, and Chester (2017)
    """
    if alpha_ccgt == "glob":
        alpha_ccgt = GLOBAL_ALPHA_CCGT
    if T_ref_ccgt == "glob":
        T_ref_ccgt = GLOBAL_TREF_CCGT

    return [daya_mw * (1 - alpha_ccgt * max(0, T - T_ref_ccgt)) for T in tasmax_values]

def pv_derating(tasmax_values, daya_mw, epsilon="glob", T_ref="glob", irradiance="glob", **kwargs):
    if epsilon == "glob":
        epsilon = GLOBAL_EPSILON
    if T_ref == "glob":
        T_ref = GLOBAL_TREF
    if irradiance == "glob":
        irradiance = [GLOBAL_IRRADIANCE] * len(tasmax_values)
    return [daya_mw * (irr / 1000) * (1 - epsilon * (T - T_ref)) for T, irr in zip(tasmax_values, irradiance)]

def coal_derating(tasmax_values, daya_mw, alpha_coal="glob", T_ref_coal="glob", **kwargs):
    """
    Derating function for coal power plants using recirculating cooling systems.
    Based on linear efficiency loss due to ambient air temperature above reference temperature.

    Parameters:
    - tasmax_values: list of air temperature values (°C)
    - daya_mw: installed capacity (MW)
    - alpha_coal: derating coefficient per °C (default = GLOBAL_ALPHA_COAL)
    - T_ref_coal: reference temperature (°C) above which derating starts (default = GLOBAL_TREF_COAL)
    
    Returns:
    - List of derated capacity values (MW)
    """
    if alpha_coal == "glob":
        alpha_coal = GLOBAL_ALPHA_COAL
    if T_ref_coal == "glob":
        T_ref_coal = GLOBAL_TREF_COAL

    return [daya_mw * (1 - alpha_coal * max(0, T - T_ref_coal)) for T in tasmax_values]

def nuclear_derating(tasmax_values, daya_mw, alpha_nuclear="glob", T_ref_nuclear="glob", **kwargs):
    """
    Derating function for nuclear power plants using Rankine-type cooling systems.
    Based on linear efficiency loss due to ambient or cooling-water temperature above reference temperature.

    Parameters:
    - tasmax_values: list of temperature values (°C)
    - daya_mw: installed capacity (MW)
    - alpha_nuclear: derating coefficient per °C (default = GLOBAL_ALPHA_NUCLEAR)
    - T_ref_nuclear: reference temperature (°C) above which derating starts (default = GLOBAL_TREF_NUCLEAR)
    
    Returns:
    - List of derated capacity values (MW)
    """
    if alpha_nuclear == "glob":
        alpha_nuclear = GLOBAL_ALPHA_NUCLEAR
    if T_ref_nuclear == "glob":
        T_ref_nuclear = GLOBAL_TREF_NUCLEAR

    return [daya_mw * (1 - alpha_nuclear * max(0, T - T_ref_nuclear)) for T in tasmax_values]

def diesel_derating_cummins(tasmax_values, daya_mw,
                    T_ref_diesel_cummins="glob",
                    T_max_diesel_cummins="glob",
                    m_min_diesel_cummins="glob",
                    **kwargs):
    """
    Derating function for diesel power plants (Cummins-style, altitude = 0 m).
    Uses a linear derating between T_ref_diesel and T_max_diesel, clamped at m_min_diesel.

    Parameters:
    - tasmax_values: list of air/filter inlet temperature values (°C)
    - daya_mw: installed capacity (MW)
    - T_ref_diesel: temperature where derating starts (°C)
        default = GLOBAL_TREF_DIESEL (recommended 35°C)
    - T_max_diesel: temperature where minimum multiplier is reached (°C)
        default = GLOBAL_TMAX_DIESEL (recommended 45°C)
    - m_min_diesel: minimum power multiplier at T_max_diesel
        default = GLOBAL_MMIN_DIESEL (recommended 0.69)

    Returns:
    - List of derated capacity values (MW)
    """
    # --- Load global defaults if still set to "glob" ---
    if T_ref_diesel_cummins == "glob":
        T_ref_diesel_cummins = GLOBAL_TREF_DIESEL_CUMMINS
    if T_max_diesel_cummins == "glob":
        T_max_diesel_cummins = GLOBAL_TMAX_DIESEL_CUMMINS
    if m_min_diesel_cummins == "glob":
        m_min_diesel_cummins = GLOBAL_MMIN_DIESEL_CUMMINS

    # --- Compute slope for linear derating ---
    slope = (1.0 - m_min_diesel_cummins) / (T_max_diesel_cummins - T_ref_diesel_cummins)
    derated_values = []

    # --- Apply linear derating with clamping ---
    for T in tasmax_values:
        if T <= T_ref_diesel_cummins:
            multiplier = 1.0
        elif T >= T_max_diesel_cummins:
            multiplier = m_min_diesel_cummins
        else:
            multiplier = 1.0 - slope * (T - T_ref_diesel_cummins)
        derated_values.append(daya_mw * multiplier)

    return derated_values



def diesel_derating(
    tasmax_values, 
    daya_mw, 
    altitude_m=1.0,                 # from height_gedtm (meters), but default 1.0 m if no height data 
    alpha_amb="glob",               # 0.5% per °C
    T_ref_diesel="glob",            # 25°C
    alpha_alt_per_m="glob",         # 1% per 100 m  => 0.0001 per m
    alt_ref_m="glob",               # 0 m
    alpha_cac="glob",               # 0.4% per °C (optional)
    T_ref_cac="glob",               # 25°C
    cac_temp_values=None,           # optional list; if None, c-term ignored
    use_cac_equals_ambient=False,   # True => CAC temp = ambient
    **kwargs
):
    """
    Derating for medium-speed diesel (Wärtsilä/Vasa ISO 3046 guideline).
    Reduction factor (%) = a + b + c,
      a = alpha_amb * max(0, T_amb - T_ref_diesel)
      b = alpha_alt_per_m * max(0, altitude_m - alt_ref_m) * 100% (already fractional here)
      c = alpha_cac * max(0, T_cac - T_ref_cac)   [optional]

    Returns: list of derated capacities (MW), same length as tasmax_values.
    """
    # ---- load globals ----
    if alpha_amb == "glob":
        alpha_amb = GLOBAL_ALPHA_DIESEL_AMB      # e.g., 0.005  (0.5%/°C)
    if T_ref_diesel == "glob":
        T_ref_diesel = GLOBAL_TREF_DIESEL        # e.g., 25.0 °C

    if alpha_alt_per_m == "glob":
        alpha_alt_per_m = GLOBAL_ALPHA_ALT_PER_M # e.g., 0.0001 per m (1%/100 m)
    if alt_ref_m == "glob":
        alt_ref_m = GLOBAL_ALT_REF_DIESEL        # e.g., 0.0 m

    if alpha_cac == "glob":
        alpha_cac = GLOBAL_ALPHA_DIESEL_CAC      # e.g., 0.004 (0.4%/°C)
    if T_ref_cac == "glob":
        T_ref_cac = GLOBAL_TREF_CAC              # e.g., 25.0 °C

    # altitude term (scalar)
    b = max(0.0, altitude_m - alt_ref_m) * alpha_alt_per_m  # fractional (e.g., 0.001 = 0.1%)

    derated = []
    for i, T in enumerate(tasmax_values):
        # ambient term
        a = alpha_amb * max(0.0, T - T_ref_diesel)

        # CAC term (optional)
        if cac_temp_values is not None:
            T_cac = cac_temp_values[i]
        elif use_cac_equals_ambient:
            T_cac = T
        else:
            T_cac = None

        c = alpha_cac * max(0.0, T_cac - T_ref_cac) if T_cac is not None else 0.0

        reduction = a + b + c                 # total fractional reduction
        multiplier = max(0.0, min(1.0, 1.0 - reduction))  # clamp 0..1

        derated.append(daya_mw * multiplier)

    return derated



def transmission_derating(
    wind_speed_list,
    T_air_list,
    diameter_mm,
    emissivity="glob",
    absorptivity="glob",
    T_conductor="glob",
    solar_rad="glob",
    **kwargs
):
    if emissivity == "glob":
        emissivity = GLOBAL_EMISSIVITY
    if absorptivity == "glob":
        absorptivity = GLOBAL_ABSORPTIVITY
    if T_conductor == "glob":
        T_conductor = GLOBAL_T_CONDUCTOR
    if solar_rad == "glob":
        solar_rad = GLOBAL_SOLAR_RAD

    diameter_m = diameter_mm / 1000
    sigma = GLOBAL_SIGMA
    results = []

    for v, T_a in zip(wind_speed_list, T_air_list):
        T_k = T_a + 273.15
        T_c = T_conductor + 273.15

        Q_r = np.pi * diameter_m * emissivity * sigma * ((T_c**4) - (T_k**4))
        Q_s = absorptivity * solar_rad * np.pi * diameter_m
        Q_c = np.pi * diameter_m * 10.45 * (1 + 10 * np.sqrt(v)) * (T_conductor - T_a)

        net_heat = Q_c + Q_r - Q_s
        results.append(net_heat)

    return results

# === FUNCTION LOOKUP ===

DERATING_FUNCTIONS = {
    "gas_derating": gas_derating,
    "pv_derating": pv_derating,
    "coal_derating": coal_derating,
    "transmission_derating": transmission_derating,
    "nuclear_derating": nuclear_derating,
    "diesel_derating_cummins": diesel_derating_cummins,
    "diesel_derating": diesel_derating,
    "oc_gas_derating": oc_gas_derating,
    "cc_gas_derating": cc_gas_derating,
}
