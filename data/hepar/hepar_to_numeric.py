import pandas as pd


filenames = ["hepar_s", "hepar_m", "hepar_l", "hepar_xl", "hepar_train", "hepar_test"]

for filename in filenames:
    df = pd.read_csv(f"data/hepar/{filename}.csv")
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

    colnames = df.columns.tolist()
    for k in ["sex", "age", "triglycerides", "bilirubin", "phosphatase", "proteins", "platelet", "inr", "urea",
              "ESR", "alt", "ast", "amylase", "ggtp", "cholesterol", "albumin",  "ChHepatitis", "Cirrhosis"]:
        colnames.remove(k)

    # loop for all absent/present
    for i in colnames:
        df[i] = df.replace({i: mapping_ap})[i]

    # loop for all hepa
    for j in ["ChHepatitis"]:
        df[j] = df.replace({j: mapping_hepa})[j]

    # loop for all cirr
    for j in ["Cirrhosis"]:
        df[j] = df.replace({j: mapping_cirr})[j]

    # loop for all sex
    for j in ["sex"]:
        df[j] = df.replace({j: mapping_sex})[j]

    # loop for all age
    for k in ["age"]:
        df[k] = df.replace({k: mapping_age})[k]
    
    # loop for all tri
    for k in ["triglycerides"]:
        df[k] = df.replace({k: mapping_tri})[k]
        
    # loop for all bil
    for k in ["bilirubin"]:
        df[k] = df.replace({k: mapping_bil})[k]

    # loop for all pho
    for k in ["phosphatase"]:
        df[k] = df.replace({k: mapping_pho})[k]

    # loop for all pro
    for k in ["proteins"]:
        df[k] = df.replace({k: mapping_pro})[k]
        
    # loop for all platelet
    for k in ["platelet"]:
        df[k] = df.replace({k: mapping_platelet})[k]  
        
    # loop for all inr
    for k in ["inr"]:
        df[k] = df.replace({k: mapping_inr})[k]

    # loop for all urea
    for k in ["urea"]:
        df[k] = df.replace({k: mapping_urea})[k]     
    
    # loop for all ESR
    for k in ["ESR"]:
        df[k] = df.replace({k: mapping_esr})[k]

    # loop for all alt
    for k in ["alt"]:
        df[k] = df.replace({k: mapping_alt})[k]

    # loop for all ast
    for k in ["ast"]:
        df[k] = df.replace({k: mapping_ast})[k]

    # loop for all amy
    for k in ["amylase"]:
        df[k] = df.replace({k: mapping_amy})[k]

    # loop for all ggtp
    for k in ["ggtp"]:
        df[k] = df.replace({k: mapping_ggtp})[k]

    # loop for all chol
    for k in ["cholesterol"]:
        df[k] = df.replace({k: mapping_chol})[k]

    # loop for all alb
    for k in ["albumin"]:
        df[k] = df.replace({k: mapping_alb})[k]

    df.to_csv(f"data/hepar/{filename}.csv", index=False)
