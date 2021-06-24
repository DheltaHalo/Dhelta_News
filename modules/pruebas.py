
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

main_path = "./files/anuncios.csv"

folder = os.path.dirname(main_path)
print(folder)
os.mkdir(folder)