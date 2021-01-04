#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import traceback

url = "https://www.ceniniger.org/presidentielle"
communes = pd.read_csv("../data/communes.csv")

#%%
def parse_results_table(results_page):
    results_table = results_page.find(id="resultat-grid_").find(id="tbody").find_all("tr")
    data = []
    for row in results_table:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols[2:])
    out = pd.DataFrame(data)
    out.columns = ["candidat", "value"]
    out = out.dropna()

    out.candidat = out.candidat.str.title()

    return(out)

def parse_participation_table(results_page, useful_indics):
    participation_tables = results_page.find_all(class_= "col-md-6")
    out = pd.DataFrame()
    for participation_subtable in participation_tables:
        list_subtable = participation_subtable.find_all(text=True)
        lines = []
        line = []
        for x in list_subtable:
            if x == '\n':
                if len(line):
                    lines.append(line[1:])
                    line = []
            elif x == " ":
                pass
            else:
                line.append(x)
        subtable = pd.DataFrame(lines)
        out = out.append(subtable)
    out.columns =["indicateur", "value"]

    out.indicateur = out.indicateur.str.replace(":","").str.strip()

    out = out[out.indicateur.isin(useful_indics)]

    return out


# %%
def get_commune_results(commune_id):
    url_result = "https://www.ceniniger.org/presidentielle/?communee=" + str(commune_id)
    useful_indics = ["Nombre de bureaux de vote parvenus",
                     "Nombre d’inscrits ayant voté",
                     "Nombre total de votants",
                     "Suffrage exprimés valables",
                     "Nombre de bureaux de vote",
                     "Nombre total d'électeurs d'inscrits",
                     "Nombre de votants sur liste additive",
                     "Nombre bulletin nuls"]
    page_not_read= True
    while page_not_read :
        try:
            results_page = requests.get(url_result)
            page_not_read = False
        except :
            time.sleep(30)
            continue
    print("Page read - processing")
    results_page = BeautifulSoup(results_page.content, "html.parser")
    results_table = parse_results_table(results_page)
    participation_table = parse_participation_table(results_page, useful_indics)
    for indic in useful_indics:
        results_table[indic] = participation_table.loc[participation_table.indicateur == indic, "value"].min()
    results_table["commune_id"] = commune_id
    return results_table

def extract_communes_results(communes):
    results = pd.DataFrame()
    obtained = 0
    failed = 0
    for commune_id in communes.comm_ID.unique():
        print(commune_id)
        try :
            results_comm = get_commune_results(commune_id)
            results = results.append(results_comm)
            obtained = obtained + 1
        except :
            print("Failed")
            failed = failed + 1
            pass
        print(str(obtained + failed) + " read - " + str(obtained) + " obtained !")
    return results



# %%
results = extract_communes_results(communes)

# %%
out = results.merge(communes, left_on="commune_id", right_on="comm_ID")
# %%
out.to_csv("../data/niger_2020_results.csv")
# %%
out.value = pd.to_numeric(out.value)
winner = out.groupby(["comm_name"]).apply(lambda x: x[x.value == x.value.max()]).reset_index(drop=True)
# %%
winner.to_csv("../data/winner.csv")
# %%
