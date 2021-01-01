#%%
import geopandas as gpd
import pandas as pd
# %%
dat = gpd.read_file("../data/shapefile/NER_adm03_feb2018.shp")
communes = pd.read_csv("../data/communes.csv")
# %%
dat["NOM_COM"] = dat.NOM_COM.str.replace("ZINDER ", "ZINDER ARRONDISSEMENT ")
dat["NOM_COM"] = dat.NOM_COM.str.replace("NIAMEY ", "NIAMEY ARRONDISSEMENT ")
dat["NOM_COM"] = dat.NOM_COM.str.replace("MARADI ", "MARADI ARRONDISSEMENT ")
dat["NOM_COM"] = dat.NOM_COM.str.replace("TAHOUA", "TAHOUA ARRONDISSEMENT ")

replacement  = {"BIRNI NGAOURE":"BIRNI N'GAOURE",
                "NDOUNGA":"N'DOUNGA",
                "NGONGA":"N'GONGA",
                "NGUELBELY":"N'GUELBELY",
                "NGUIGMI":"N'GUIGMI",
                "NGOURTI":"N'GOURTI",
                "TIBIRI DOUTCHI":"TIBIRI (DOUTCHI)",
                "TIBIRI MARADI":"TIBIRI (MARADI)",
                "TOMBOKOIREY 1":"TOMBOKOIREY I",
                "TOMBOKOIREY 2":"TOMBOKOIREY II",
                "DAN KASSARI":"DAN-KASSARI",
                "DAN GOULBI":"DAN-GOULBI",
                "DAN ISSA":"DAN-ISSA",
                "GANGARA AGUIE":"GANGARA (GAZAOUA)",
                "GANGARA TANOUT":"GANGARA (TANOUT)",
                "KANAN BAKACHE":"KANAN-BAKACHE",
                "MALLAWA":"MALAWA",
                "ROUMBOU 1":"ROUMBOU I",
                "DOGO DOGO":"DOGO-DOGO"}

dat["NOM_COM"] = dat["NOM_COM"].replace(replacement)
#%%
dat.to_file("../data/niger_communes.geojson", driver='GeoJSON')
# %%
