import os
from datetime import datetime

from settings import *
from modules import milanuncios_scrap

def main():
    folder = os.path.dirname(files_path)

    if not(os.path.isdir(folder)):
        os.mkdir(folder)

    if not(os.path.isfile(files_path + "anuncios.csv")):
      milanuncios_scrap.main()

    f = open(files_path + log_name, "a+")
    f.write(f"Session started at: {str(datetime.now())}\n")
    f.close()
