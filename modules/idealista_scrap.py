import numpy as np

global idealista_links
idealista_links = ["https://www.idealista.com/alquiler-viviendas/santander/los-castros/",
"https://www.idealista.com/alquiler-viviendas/santander/centro-ayuntamiento/",
"https://www.idealista.com/alquiler-viviendas/santander/general-davila/",
"https://www.idealista.com/alquiler-viviendas/santander/puerto-chico/",
"https://www.idealista.com/alquiler-viviendas/santander/el-sardinero/",
"https://www.idealista.com/alquiler-viviendas/santander/numancia-san-fernando/",
"https://www.idealista.com/alquiler-viviendas/santander/cuatro-caminos/",
"https://www.idealista.com/alquiler-viviendas/santander/castilla-hermida/",
"https://www.idealista.com/alquiler-viviendas/santander/alisal-cazona-san-roman/",
"https://www.idealista.com/alquiler-viviendas/santander/valdenoja/"]

def cheap():
    links = np.empty(len(idealista_links), dtype="U999")

    for k, v in enumerate(idealista_links):
        links[k] = v+"?ordenado-por=precios-asc"

    return links
