import requests

def obter_preco_fipe(marca, modelo, ano):
    # Passo 1: Obter o código da marca
    url_marcas = f"https://parallelum.com.br/fipe/api/v1/motos/marcas"
    response = requests.get(url_marcas)
    marcas = response.json()
    
    codigo_marca = None
    for m in marcas:
        if m['nome'].lower() == marca.lower():
            codigo_marca = m['codigo']
            break
    
    if not codigo_marca:
        print(f"Marca {marca} não encontrada.")
        return None

    # Passo 2: Obter os modelos da marca
    url_modelos = f"https://parallelum.com.br/fipe/api/v1/motos/marcas/{codigo_marca}/modelos"
    response = requests.get(url_modelos)
    modelos = response.json()
    
    codigo_modelo = None
    for m in modelos['modelos']:
        if m['nome'].lower() == modelo.lower():
            codigo_modelo = m['codigo']
            break
    
    if not codigo_modelo:
        print(f"Modelo {modelo} não encontrado.")
        return None
    
    # Passo 3: Obter os anos do modelo
    url_anos = f"https://parallelum.com.br/fipe/api/v1/motos/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    response = requests.get(url_anos)
    anos = response.json()
    
    codigo_ano = None
    for a in anos:
        if a['nome'][:4] == ano[:4]:  # Considerando apenas o ano, ignorando o combustível
            codigo_ano = a['codigo']
            break
    
    if not codigo_ano:
        print(f"Ano {ano} não encontrado.")
        return None
    
    # Passo 4: Obter o preço FIPE
    url_preco = f"https://parallelum.com.br/fipe/api/v1/motos/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    response = requests.get(url_preco)
    preco_info = response.json()
    
    if 'Valor' in preco_info:
        return preco_info['Valor']
    else:
        print("Erro ao obter o preço FIPE.")
        return None