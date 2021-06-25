# -*- coding: utf-8 -*-
"""
@author: DheltaHalo
"""
import requests
import pandas as pd
import numpy as np
import os
from requests.sessions import default_headers

main_path = "files/anuncios.csv"

def main(file_path: str = main_path):
    url = "https://www.milanuncios.com/ofertas-de-empleo-en-guadalajara/?fromSearch=1&demanda=n"
    page = requests.get(url)
    page_content = page.content.decode("latin-1")

    name_list = page_content.split("\"name\"")
    url_list = page_content.split("\"url\"")

    titulares = np.empty(len(name_list), dtype = "U999")
    urls = np.empty(len(url_list), dtype = "U999")

    for k, v in enumerate(name_list):
        titulares[k] = v.split("\n")[0]
    
    for k, v in enumerate(url_list):
        urls[k] = v.split("\n")[0]

    titulares = titulares[3:]
    urls = urls[2:]

    for k, v in enumerate(titulares):
        ind_1 = v.find("\"") + 1
        ind_2 = v[ind_1:].find("\"")
        titulares[k] = v[ind_1: ind_2 + 3]

    for k, v in enumerate(urls):
        ind_1 = v.find("\"") + 1
        ind_2 = v[ind_1:].find("\"")
        urls[k] = v[ind_1: ind_2 + 3]

    frame = {"titulares": titulares, "urls": urls}
    df = pd.DataFrame(frame)

    global main_path

    if file_path != main_path:
        main_path = file_path
        
    df.to_csv(file_path, index = False)

def decode():
    df = pd.read_csv(main_path)

    return df
