#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.ceniniger.org/presidentielle/"
regions = pd.read_csv("../data/regions.csv", sep = ";")

# %%
def get_lower_geo(url, region_type, region_id):
    page_not_read = True
    url_region = url + "?"+ region_type+ "=" + region_id
    while page_not_read :
        try:
            region_page = requests.get(url_region)
            page_not_read = False
        except :
            time.sleep(30)
            continue
    soup = BeautifulSoup(region_page.content, 'html.parser')
    departements = soup.find_all("option")
    dep_ID = []
    dep_name = []
    for dep in departements:
        if len(dep["value"]) > 0:
            dep_ID.append(dep["value"])
            dep_name.append(dep.text)
    return(dep_ID, dep_name)


# %%
departements = pd.DataFrame()
for reg_id in regions.ID:
    print(reg_id)
    dep_r = pd.DataFrame()
    deps = get_lower_geo(url, "region" , str(reg_id))
    dep_r['dep_ID'] = deps[0]
    dep_r['dep_name'] = deps[1]
    dep_r['reg_ID'] = reg_id
    departements = departements.append(dep_r)

#%%
communes = pd.DataFrame()
for dep_id in departements.dep_ID:
    print(dep_id)
    comm_d = pd.DataFrame()
    comms = get_lower_geo(url, "departement" , str(dep_id))
    comm_d['comm_ID'] = comms[0]
    comm_d['comm_name'] = comms[1]
    comm_d['dep_ID'] = dep_id
    communes = communes.append(comm_d)

# %%
communes.comm_name = communes.comm_name.str.strip().str.replace(";","")

communes = regions.merge(departements, left_on="ID", right_on="reg_ID").merge(communes)
communes.to_csv("../data/communes.csv")