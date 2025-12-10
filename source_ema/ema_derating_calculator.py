import pandas as pd
import numpy as np

from source_ema.f_derating_registry import DERATING_FUNCTIONS  # lookup ke semua fungsi derating   :contentReference[oaicite:1]{index=1}


class DeratingEngine:

    def __init__(self, rukn_csv):
        """
        rukn_csv = file berisi kapasitas pembangkit RUKN 2060
                    kolom wajib:
                    - jenis (kode PLN: PLTU, PLTG, PLTGU, PLTS, dst.)
                    - daya_mw
        """
        self.df = pd.read_csv(rukn_csv)
        self._assign_derating_function()


    # ==========================================================
    # MAPPING: kontrak kamu → fungsi derating
    # ==========================================================

    def _map_function(self, jenis):
        jenis = str(jenis)

        if "PLTGU" in jenis:
            return "cc_gas_derating"
        elif "PLTG" in jenis:
            return "oc_gas_derating"
        elif "PLTMG" in jenis:
            return "diesel_derating"
        elif "PLTDG" in jenis:
            return "diesel_derating"
        elif "PLTD" in jenis:
            return "diesel_derating"
        elif "PLTBm" in jenis:
            return "coal_derating"
        elif "PLTSa" in jenis:
            return "coal_derating"
        elif "PLTU MT" in jenis:
            return "coal_derating"
        elif "PLTU" in jenis:
            return "coal_derating"
        elif "PLTBg" in jenis:
            return "oc_gas_derating"
        elif "PLTS-f" in jenis or "PLTS+BESS" in jenis:
            return "pv_derating"
        elif "PLTS" in jenis:
            return "pv_derating"
        elif "PLTN" in jenis:
            return "nuclear_derating"
        else:
            return None


    def _assign_derating_function(self):
        """Tambahkan kolom derating_function ke dataframe RUKN."""
        self.df["derating_function"] = self.df["jenis"].apply(self._map_function)


    # ==========================================================
    # CORE: APPLY DERATING TO NATIONAL CAPACITY
    # ==========================================================

    def apply_derating(self, T_nat):
        """
        T_nat = temperatur nasional satu angka (°C).
                di-extend menjadi list karena semua fungsi derating menerima list tasmax_values.
        Return:
          - dataframe dengan derated MW per pembangkit
          - total_derated_capacity
        """

        T_list = [T_nat]     # semua pembangkit pakai temperatur nasional sama
        derated_values = []

        for _, row in self.df.iterrows():

            func_name = row["derating_function"]
            P = row["daya_mw"]

            if func_name is None or func_name not in DERATING_FUNCTIONS:
                derated = P  # tidak terdampak derating
            else:
                func = DERATING_FUNCTIONS[func_name]
                derated = func(tasmax_values=T_list, daya_mw=P)[0]

            derated_values.append(derated)

        self.df["derated_mw"] = derated_values
        self.df["loss_mw"] = self.df["daya_mw"] - self.df["derated_mw"]

        return self.df


    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summarize(self):
        """
        Summary nasional:
           - before derating
           - after derating
           - loss total
        """
        total_before = self.df["daya_mw"].sum()
        total_after = self.df["derated_mw"].sum()
        loss = total_before - total_after

        return {
            "total_before_mw": round(total_before, 2),
            "total_after_mw": round(total_after, 2),
            "total_loss_mw": round(loss, 2),
            "loss_percent": round(100 * loss / total_before, 2)
        }
