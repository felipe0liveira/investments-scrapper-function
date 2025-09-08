from src.scrapper import scrap
from src.analizer import analize

def main():
    filename, length = scrap()

    if length == 0:
        print("Nenhum registro encontrado.")
        return
    
    print(f"Arquivo salvo: {filename}")
    print(f"Número de registros: {length}")
    db_records = analize(filename)

if __name__ == "__main__":
    main()
    # db_records = analize("./data/data-20250908_115214.json")