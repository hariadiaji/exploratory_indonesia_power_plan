# =======================================================
# climate_extractor.py
# CLASS-BASED Climate State Extractor (Assets Only)
# Produces:
#   - MIN/MAX tasmax per provinsi
#   - NATIONAL MIN/MAX (capacity-weighted)
# =======================================================

import pandas as pd
import numpy as np
import ast


# -------------------------------------
# UTILITIES (standalone helpers)
# -------------------------------------

def parse_list(cell):
    """Convert string/list to Python list of floats."""
    if isinstance(cell, str):
        try:
            v = ast.literal_eval(cell)
        except:
            return []
    elif isinstance(cell, (list, tuple, np.ndarray)):
        v = cell
    else:
        return []
    return [x for x in v if isinstance(x, (int, float))]


def extract_minmax(series_of_lists):
    """Flatten lists → return (min, max)."""
    arr = []
    for cell in series_of_lists:
        arr.extend(parse_list(cell))
    if len(arr) == 0:
        return np.nan, np.nan
    arr = np.array(arr, dtype=float)
    return float(arr.min()), float(arr.max())


def capacity_weighted(series, weights):
    """Simple weighted average function."""
    return float(np.average(series, weights=weights))


# -------------------------------------
# CLASS: ClimateExtractor
# -------------------------------------

class ClimateExtractor:
    """
    Extractor for asset-based tasmax lists:
    - MIN/MAX per provinsi
    - NATIONAL MIN/MAX (capacity-weighted)
    """

    ERA5_YEARS = [2024, 2023, 2022, 2021, 2020, 2010, 2000]

    def __init__(self, assets_csv):
        """Load asset CSV once."""
        self.assets = pd.read_csv(assets_csv)
        self.provs = sorted(self.assets["provinsi"].unique())
        self.out = pd.DataFrame({"provinsi": self.provs})
        self.all_cols = list(self.assets.columns)

    # ---------------------------
    # INTERNAL HELPERS
    # ---------------------------

    def _find_columns(self):
        """Identify tasmax columns by scenario pattern."""

        cols = {}

        cols["45_2031"] = [c for c in self.all_cols if "rcp45" in c and "203101" in c]
        cols["85_2031"] = [c for c in self.all_cols if "rcp85" in c and "203101" in c]

        cols["45_2051"] = [c for c in self.all_cols if "rcp45" in c and "205101" in c]
        cols["85_2051"] = [c for c in self.all_cols if "rcp85" in c and "205101" in c]

        cols["45_2024"] = [c for c in self.all_cols if "rcp45" in c and "202401-202412" in c]
        cols["85_2024"] = [c for c in self.all_cols if "rcp85" in c and "202401-202412" in c]

        # ERA5
        for yr in self.ERA5_YEARS:
            cols[f"ERA5_{yr}"] = [c for c in self.all_cols if c.startswith(f"tmax_ERA5_{yr}")]

        return cols

    def _minmax_per_province(self, colset):
        """Return dict { 'min': {prov}, 'max': {prov} }."""
        result_min = {}
        result_max = {}

        for prov, rows in self.assets.groupby("provinsi")[colset]:
            mn, mx = extract_minmax(rows.values.flatten())
            result_min[prov] = mn
            result_max[prov] = mx

        return {"min": result_min, "max": result_max}

    # ---------------------------
    # PUBLIC API
    # ---------------------------

    def compute_minmax(self):
        """Compute MIN/MAX tasmax per provinsi for all scenario windows."""

        cols = self._find_columns()

        def add(colset, label):
            mm = self._minmax_per_province(colset)
            self.out[f"min_{label}"] = self.out["provinsi"].map(mm["min"])
            self.out[f"max_{label}"] = self.out["provinsi"].map(mm["max"])

        # Add RCP windows
        add(cols["45_2031"], "assets_45_2031_2040")
        add(cols["85_2031"], "assets_85_2031_2040")

        add(cols["45_2051"], "assets_45_2051_2060")
        add(cols["85_2051"], "assets_85_2051_2060")

        # Add 12-month 2024 window
        add(cols["45_2024"], "assets_45_2024")
        add(cols["85_2024"], "assets_85_2024")

        # ERA5
        for yr in self.ERA5_YEARS:
            label = f"ERA5_{yr}"
            colset = cols[f"ERA5_{yr}"]

            if len(colset) > 0:
                mm = self._minmax_per_province(colset)
                self.out[f"min_{label}"] = self.out["provinsi"].map(mm["min"])
                self.out[f"max_{label}"] = self.out["provinsi"].map(mm["max"])
            else:
                self.out[f"min_{label}"] = np.nan
                self.out[f"max_{label}"] = np.nan

        # Round all numeric columns to 2 decimals
        numeric_cols = self.out.select_dtypes(include=[np.number]).columns
        self.out[numeric_cols] = self.out[numeric_cols].round(3)

        return self.out

    def compute_national_temperature(self, scenario="85_2051_2060"):
        """
        Compute capacity-weighted MIN/MAX national temperature for a given scenario.
        scenario key examples:
            "45_2051_2060"
            "85_2051_2060"
        """

        min_col = f"min_assets_{scenario}"
        max_col = f"max_assets_{scenario}"

        if min_col not in self.out.columns:
            raise ValueError(f"Scenario columns not found: {min_col}")

        # Compute total capacity per provinsi
        cap = self.assets.groupby("provinsi")["daya_mw"].sum().reset_index()
        cap.columns = ["provinsi", "capacity_mw"]

        df = self.out.merge(cap, on="provinsi", how="left")

        Tnat_min = capacity_weighted(df[min_col], df["capacity_mw"])
        Tnat_max = capacity_weighted(df[max_col], df["capacity_mw"])

        return {
            "scenario": scenario,
            "national_min": round(Tnat_min, 3),
            "national_max": round(Tnat_max, 3)
        }

    def save(self, output_csv):
        self.out.to_csv(output_csv, index=False)
        print(f"[OK] Saved climate min–max table to: {output_csv}")
