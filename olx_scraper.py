from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import quote_plus

def obter_links_olx(preco_fipe, marca, modelo, estado, ano):
    busca = f"{modelo}"
    estado_path = f"estado-{estado.lower()}"
    # URL com o ano filtrado
    url = f"https://www.olx.com.br/autos-e-pecas/motos/{ano}/{estado_path}?q={quote_plus(busca)}"

    print(f"URL gerada: {url}")  # Para verificar a URL no console

    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)

    try:
        driver.get(url)

        # Fechar a mensagem de política de cookies, se aparecer
        try:
            fechar_botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fechar')]"))
            )
            fechar_botao.click()
            print("Botão 'Fechar' clicado com sucesso.")
        except Exception as e:
            print("Botão 'Fechar' não encontrado ou já fechado:", e)

        # Aceitar os cookies, se necessário
        try:
            aceitar_botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar')]"))
            )
            aceitar_botao.click()
            print("Botão 'Aceitar' clicado com sucesso.")
        except Exception as e:
            print("Botão 'Aceitar' não encontrado ou já aceito:", e)

        # Esperar a página carregar completamente
        time.sleep(5)

        # Esperar até que os anúncios estejam carregados
        try:
            anuncios_elementos = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'sc-16a6z39-3')]"))
            )
        except Exception as e:
            print("Erro ao localizar anúncios:", e)
            return []

        # Coletar os links dos anúncios e filtrar pelo preço
        links = []
        print(f"Número de anúncios encontrados: {len(anuncios_elementos)}")

        for anuncio in anuncios_elementos:
            try:
                # Obter o preço do anúncio
                preco_element = anuncio.find_element(By.XPATH, ".//span[contains(@class, 'sc-16a6z39-5')]")
                preco_text = preco_element.text.replace("R$ ", "").replace(".", "").replace(",", ".")
                preco_anuncio = float(preco_text.strip())

                # Verificar se o preço está abaixo ou igual ao preço FIPE
                if preco_anuncio <= preco_fipe:
                    link_element = anuncio.find_element(By.XPATH, ".//a[@data-lurker-detail='list_id']")
                    link = link_element.get_attribute("href")
                    links.append(link)
            except Exception as e:
                print("Erro ao processar anúncio:", e)

        print(f"Número de links coletados: {len(links)}")
        return links
    finally:
        driver.quit()