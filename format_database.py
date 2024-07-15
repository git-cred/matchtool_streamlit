import pandas as pd

GLIDE = pd.read_csv("GLIDE.csv")
dropList = ["time", "id", "duration", "status", "latitude", "longitude"]
GLIDE = GLIDE.drop(dropList, axis=1)
GLIDE["GLIDE_ID"] = GLIDE["event"] + "-" + GLIDE["number"]
GLIDE.to_csv("GLIDE_formatted.csv")

EMDAT = pd.read_excel("public_emdat_2004.xlsx")
dropList = ["Historic", "Disaster Group", "End Day", "End Month", "End Year", "Disaster Subgroup",
                    "Origin", "Associated Types", "OFDA/BHA Response", "Appeal", "Declaration",
                    "AID Contribution ('000 US$)", "River Basin",
                    "Reconstruction Costs ('000 US$)", "Reconstruction Costs, Adjusted ('000 US$)",
                    "Insured Damage ('000 US$)", "Insured Damage, Adjusted ('000 US$)", "Total Damage ('000 US$)",
                    "Total Damage, Adjusted ('000 US$)", "CPI", "Admin Units", "Entry Date", "Last Update"]
EMDAT = EMDAT.drop(dropList, axis=1)
EMDAT["EMDAT_ID"] = EMDAT["EMDAT_ID"] = EMDAT["DisNo."].apply(lambda x: x.replace(x[9:], ""))
EMDAT.to_csv("public_emdat_2004_formatted.csv")
