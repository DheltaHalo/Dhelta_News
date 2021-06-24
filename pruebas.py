import requests
url = "https://www.idealista.com/alquiler-viviendas/santander/los-castros/?ordenado-por=precios-asc"
page = requests.get(url)
page_content = page.content.decode("latin-1")
print(page_content)