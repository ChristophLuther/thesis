import pandas as pd
# TODO fix column names
filenames = ["alarm_s", "alarm_m", "alarm_l", "alarm_xl", "alarm_train", "alarm_test"]

for filename in filenames:
    df = pd.read_csv(f"data/alarm/{filename}.csv")
    mapping_lnh = {"LOW": 0, "NORMAL": 1, "HIGH": 2}
    mapping_tf = {False: 0, True: 1}
    mapping_zlnh = {"ZERO": 0, "LOW": 1, "NORMAL": 2, "HIGH": 3}
    mapping_int = {"NORMAL": 0, "ESOPHAGEAL": 1, "ONESIDED": 2}
    # loop for all LOW, NORMAL (and HIGH)
    for i in ["CVP", "PCWP", "TPR", "BP", "CO", "HRBP", "HREKG", "HRSAT",
              "PAP", "SAO2", "FIO2", "MINVOLSET", "LVEDVOLUME", "STROKEVOLUME", "CATECHOL", "HR",
              "SHUNT", "PVSAT", "ARTCO2"]:
        df[i] = df.replace({i: mapping_lnh})[i]

    # loop for all TRUE, FALSE
    for j in ["HISTORY", "HYPOVOLEMIA", "LVFAILURE", "ANAPHYLAXIS", "INSUFFANESTH", "PULMEMBOLUS", "KINKEDTUBE",
              "DISCONNECT", "ERRLOWOUTPUT", "ERRCAUTER"]:
        df[j] = df.replace({j: mapping_tf})[j]

    # loop for all ZERO, LOW, NORMAL, HIGH
    for k in ["PRESS", "EXPCO2", "MINVOL", "VENTALV", "VENTLUNG", "VENTTUBE", "VENTMACH"]:
        df[k] = df.replace({k: mapping_zlnh})[k]

    df["INTUBATION"] = df.replace({"INTUBATION": mapping_int})["INTUBATION"]

    df.to_csv(f"data/alarm/{filename}.csv", index=False)
