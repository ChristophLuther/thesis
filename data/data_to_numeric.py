# convert all data sampled from the graphs Alarm, Asia, Hepar II and Sachs to numeric values
# manually in order to maintain as much information as possible (e.g. for ordinal variables)
import pandas as pd

# alarm data
alarm = pd.read_csv(f"data/alarm.csv")
mapping_lnh = {"LOW": 0, "NORMAL": 1, "HIGH": 2}
mapping_tf = {False: 0, True: 1}
mapping_zlnh = {"ZERO": 0, "LOW": 1, "NORMAL": 2, "HIGH": 3}
mapping_int = {"NORMAL": 0, "ESOPHAGEAL": 1, "ONESIDED": 2}
# loop for all LOW, NORMAL (and HIGH)
for i in ["CVP", "PCWP", "TPR", "BP", "CO", "HRBP", "HREKG", "HRSAT",
          "PAP", "SAO2", "FIO2", "MINVOLSET", "LVEDVOLUME", "STROKEVOLUME", "CATECHOL", "HR",
          "SHUNT", "PVSAT", "ARTCO2"]:
    alarm[i] = alarm.replace({i: mapping_lnh})[i]
# loop for all TRUE, FALSE
for j in ["HISTORY", "HYPOVOLEMIA", "LVFAILURE", "ANAPHYLAXIS", "INSUFFANESTH", "PULMEMBOLUS", "KINKEDTUBE",
          "DISCONNECT", "ERRLOWOUTPUT", "ERRCAUTER"]:
    alarm[j] = alarm.replace({j: mapping_tf})[j]
# loop for all ZERO, LOW, NORMAL, HIGH
for k in ["PRESS", "EXPCO2", "MINVOL", "VENTALV", "VENTLUNG", "VENTTUBE", "VENTMACH"]:
    alarm[k] = alarm.replace({k: mapping_zlnh})[k]
alarm["INTUBATION"] = alarm.replace({"INTUBATION": mapping_int})["INTUBATION"]
alarm.to_csv(f"data/alarm.csv", index=False)


# asia data
asia = pd.read_csv(f"data/asia.csv")
mapping_rf = {"no": 0, "yes": 1}
col_names = asia.columns.tolist()
for i in col_names:
    asia[i] = asia.replace({i: mapping_rf})[i]
asia.to_csv(f"data/asia.csv", index=False)


# hepar data
hepar = pd.read_csv(f"data/hepar.csv")
mapping_ap = {"absent": 0, "present": 1}
mapping_hepa = {"absent": 0, "present": 1, "active": 2, "persistent": 3}
mapping_cirr = {"absent": 0, "present": 1, "compensate": 2, "decompensate": 3}
mapping_sex = {"female": 0, "male": 1}
mapping_age = {"age0_30": 0, "age31_50": 1, "age51_65": 2, "age65_100": 3}
mapping_tri = {"a1_0": 0, "a17_4": 1, "a3_2": 2}
mapping_bil = {"a1_0": 0, "a19_7": 1, "a6_2": 2, "a88_20": 3}
mapping_pho = {"a239_0": 0, "a4000_700": 1, "a699_240": 2}
mapping_pro = {"a10_6": 0, "a5_2": 1}
mapping_platelet = {"a299_150": 0, "a99_0": 1, "a149_100": 2, "a597_300": 3}
mapping_inr = {"a109_70": 0, "a69_0": 1, "a200_110": 2}
mapping_urea = {"a165_50": 0, "a49_40": 1, "a39_0": 2}
mapping_esr = {"a14_0": 0, "a200_50": 1, "a49_15": 2}
mapping_alt = {"a199_100": 0, "a99_35": 1, "a34_0": 2, "a850_200": 3}
mapping_ast = {"a149_40": 0, "a39_0": 1, "a399_150": 2, "a700_400": 3}
mapping_amy = {"a299_0": 0, "a1400_500": 1, "a499_300": 2}
mapping_ggtp = {"a9_0": 0, "a640_70": 1, "a29_10": 2, "a69_30": 3}
mapping_chol = {"a239_0": 0, "a349_240": 1, "a999_350": 2}
mapping_alb = {"a70_50": 0, "a29_0": 1, "a49_30": 2}

colnames = hepar.columns.tolist()
for k in ["sex", "age", "triglycerides", "bilirubin", "phosphatase", "proteins", "platelet", "inr", "urea",
          "ESR", "alt", "ast", "amylase", "ggtp", "cholesterol", "albumin",  "ChHepatitis", "Cirrhosis"]:
    colnames.remove(k)
# loop for all absent/present
for i in colnames:
    hepar[i] = hepar.replace({i: mapping_ap})[i]
# loop for all hepa
for j in ["ChHepatitis"]:
    hepar[j] = hepar.replace({j: mapping_hepa})[j]
# loop for all cirr
for j in ["Cirrhosis"]:
    hepar[j] = hepar.replace({j: mapping_cirr})[j]
# loop for all sex
for j in ["sex"]:
    hepar[j] = hepar.replace({j: mapping_sex})[j]
# loop for all age
for k in ["age"]:
    hepar[k] = hepar.replace({k: mapping_age})[k]

# loop for all tri
for k in ["triglycerides"]:
    hepar[k] = hepar.replace({k: mapping_tri})[k]

# loop for all bil
for k in ["bilirubin"]:
    hepar[k] = hepar.replace({k: mapping_bil})[k]
# loop for all pho
for k in ["phosphatase"]:
    hepar[k] = hepar.replace({k: mapping_pho})[k]
# loop for all pro
for k in ["proteins"]:
    hepar[k] = hepar.replace({k: mapping_pro})[k]

# loop for all platelet
for k in ["platelet"]:
    hepar[k] = hepar.replace({k: mapping_platelet})[k]

# loop for all inr
for k in ["inr"]:
    hepar[k] = hepar.replace({k: mapping_inr})[k]
# loop for all urea
for k in ["urea"]:
    hepar[k] = hepar.replace({k: mapping_urea})[k]

# loop for all ESR
for k in ["ESR"]:
    hepar[k] = hepar.replace({k: mapping_esr})[k]
# loop for all alt
for k in ["alt"]:
    hepar[k] = hepar.replace({k: mapping_alt})[k]
# loop for all ast
for k in ["ast"]:
    hepar[k] = hepar.replace({k: mapping_ast})[k]
# loop for all amy
for k in ["amylase"]:
    hepar[k] = hepar.replace({k: mapping_amy})[k]
# loop for all ggtp
for k in ["ggtp"]:
    hepar[k] = hepar.replace({k: mapping_ggtp})[k]
# loop for all chol
for k in ["cholesterol"]:
    hepar[k] = hepar.replace({k: mapping_chol})[k]
# loop for all alb
for k in ["albumin"]:
    hepar[k] = hepar.replace({k: mapping_alb})[k]
hepar.to_csv(f"data/hepar.csv", index=False)


# sachs data
sachs = pd.read_csv(f"data/sachs.csv")
mapping_rf = {"LOW": 0, "AVG": 1,  "HIGH": 2}
col_names = sachs.columns.tolist()
for i in col_names:
    sachs[i] = sachs.replace({i: mapping_rf})[i]
sachs.to_csv(f"data/sachs.csv", index=False)
