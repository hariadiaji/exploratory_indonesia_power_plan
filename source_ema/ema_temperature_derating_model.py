from ema_workbench import Model, RealParameter, ScalarOutcome
from ema_workbench import perform_experiments
from source_ema.ema_derating_calculator import DeratingEngine

# === 1. INIT ENGINE ===
eng = DeratingEngine("rukn_2060_Indonesia_capacity.csv")

# === 2. DEFINE EMA MODEL FUNCTION ===
def model_function(experiment):
    Tnat = experiment["T_nat_2060"]   # uncertainty dari EMA

    # apply derating
    eng.apply_derating(Tnat)
    summary = eng.summarize()

    return {
        "loss_percent": summary["loss_percent"],
        "loss_mw": summary["total_loss_mw"],
    }

# === 3. CREATE MODEL WRAPPER ===
ema_model = Model("Temperature_Derating_Test", function=model_function)

# === 4. UNCERTAINTY SPACE ===
ema_model.uncertainties = [
    RealParameter("T_nat_2060", 22.93, 38.91)  # range dari Option2
]

# === 5. OUTCOMES ===
ema_model.outcomes = [
    ScalarOutcome("loss_percent"),
    ScalarOutcome("loss_mw")
]

