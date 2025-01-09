from olx_scraper import obter_links_olx
from fipe_api import obter_preco_fipe

def main():
    marca = "YAMAHA"
    modelo = "XTZ 250 LANDER 249cc/LANDER BLUEFLEX/ABS"
    ano = "2023"
    estado = "MG"

    preco_fipe = obter_preco_fipe(marca, modelo, ano)
    if preco_fipe:
        print(f"Preço FIPE para {marca} {modelo} {ano}: {preco_fipe}")
        preco_fipe_numero = float(preco_fipe.replace("R$ ", "").replace(".", "").replace(",", ".").strip())
        links = obter_links_olx(preco_fipe_numero, marca, modelo, estado, ano)
        print("Links encontrados:")
        for link in links:
            print(link)
    else:
        print("Não foi possível obter o preço da FIPE.")

if __name__ == "__main__":
    main()