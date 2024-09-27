#%%
import requests

#%%
from bs4 import  BeautifulSoup

#%%
from tqdm import tqdm

#%%
import pandas as pd

#%%
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.118873644.1726845672; _ga_DJLCSW50SC=GS1.1.1726855667.2.1.1726855672.55.0.0; _ga_D6NF5QC4QT=GS1.1.1726855667.2.1.1726855673.54.0.0; _ga=GA1.2.1351818916.1726845671; FCNEC=%5B%5B%22AKsRol-MW6IlFiSiKmfaTcyzGnAH6yrqeVY5ijdJkAKihFMnvE7g1X0z_G35XUDeIM1v6lCky44ZX0MyAlDnRJ6k5yBaBtds2VqtHxzMNFXHwWXbq3GxkFtRCg7T3SG4_HhkY1yYVBM_RK9NAVyV2M3AXBbSRuJ5_A%3D%3D%22%5D%5D',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Opera";v="112"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    }

#%%
url = "https://www.residentevildatabase.com/personagens"

#%%
def get_content(url):
    response = requests.get(url, headers=headers)
    return response

#%%
def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    paragrafo

    ems = paragrafo.find_all("em")
    ems

    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

#%%
def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
                .find("h4")
                .find_next()
                .find_all("li"))

    aparicoes = [i.text for i in  lis]
    return aparicoes

#%%
def get_personagens_info(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Feito!")
    else:
        soup = BeautifulSoup(resp.text, features="html.parser")
        data = get_basic_infos(soup)
        data['Aparições'] = get_aparicoes(soup)
        return data

#%%    
def get_links():    
    url = "https://www.residentevildatabase.com/personagens"

    resp = requests.get(url, headers=headers)

    soup_personagens = BeautifulSoup(resp.text, features="html.parser")

    ancoras = (soup_personagens.find("div", class_="td-page-content")
                        .find_all("a"))

    links = [i["href"] for i in ancoras]
    
    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_info(i)
    if d is not None:
        d["link"] = i
        nome = i.strip("/").split("/")[-1].replace("-", " ").title()
        d["nome"] = nome
        data.append(d)
data

#%%
df = pd.DataFrame(data)
df

#%%

df.to_parquet("dados_re.parquet", index=False)

#%%
df_new= pd.read_parquet("dados_re.parquet")
df_new