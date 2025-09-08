import re
import unicodedata
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def normalize_column_name(name):
    """Normaliza o nome da coluna: remove acentos, converte para minúsculo e substitui espaços por _"""
    # Remove acentos
    name = unicodedata.normalize('NFD', name)
    name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
    
    # Converte para minúsculo
    name = name.lower()
    
    # Remove caracteres especiais e substitui espaços por _
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '_', name.strip())
    
    return name

def extract_table_data(html):
    """Extrai dados da tabela #rentabilidadeTable e retorna lista de dicionários"""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'rentabilidadeTable'})
    
    if not table:
        print("Tabela #rentabilidadeTable não encontrada")
        return []
    
    # Define os cabeçalhos manualmente baseado na estrutura real da tabela
    # Coluna 1: Título (ignoramos o cabeçalho, mas o título real está na coluna 2)
    # Coluna 2: Título real do produto
    # Coluna 3: Ignorar
    # Coluna 4: Investimento mínimo
    # Coluna 5: Rendimento anual
    # Coluna 6: Vencimento
    headers = ['titulo_cabecalho', 'titulo', 'coluna_ignorar', 'investimento_minimo', 'rendimento_anual', 'vencimento']
    
    # Extrai APENAS os dados (ignora o cabeçalho)
    data_rows = []
    tbody = table.find('tbody')
    
    if tbody:
        # Se houver tbody, pega todas as linhas do tbody
        rows = tbody.find_all('tr')
    else:
        # Se não houver tbody, pega todas as linhas exceto a primeira (cabeçalho)
        all_rows = table.find_all('tr')
        rows = all_rows[1:] if len(all_rows) > 1 else []
    
    for row in rows:
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 4:  # Precisa ter pelo menos 4 colunas
            row_data = {}
            
            # Pega o título da segunda coluna (índice 1)
            titulo = cells[1].get_text().strip() if len(cells) > 1 else ""
            
            # Pega investimento mínimo da posição correta
            if len(cells) >= 4:
                investimento_minimo = cells[3].get_text().strip() if len(cells) > 3 else ""
            else:
                investimento_minimo = cells[2].get_text().strip() if len(cells) > 2 else ""
            
            # Pega rendimento anual
            rendimento_anual = cells[4].get_text().strip() if len(cells) > 4 else ""
            
            # Pega vencimento
            vencimento = cells[5].get_text().strip() if len(cells) > 5 else ""
            
            # Monta o dicionário apenas com os campos que queremos
            row_data = {
                'titulo': titulo,
                'investimento_minimo': investimento_minimo,
                'rendimento_anual': rendimento_anual,
                'vencimento': vencimento,
                'data_extracao': datetime.now().isoformat(),
            }           
            # Só adiciona se tiver pelo menos o investimento mínimo
            if investimento_minimo:
                data_rows.append(row_data)
    
    return data_rows


def scrap():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.tesourodireto.com.br/produtos/dados-sobre-titulos/rendimento-dos-titulos")
            page.wait_for_selector("#rentabilidadeTable")  # espera a tabela aparecer
            html = page.content()
            
            # Extrai os dados da tabela
            table_data = extract_table_data(html)
            
            # Exibe os resultados
            print(f"Encontrados {len(table_data)} registros na tabela:")
            print("\nPrimeiros registros:")
            for i, row in enumerate(table_data[:3]):  # Mostra apenas os primeiros 3 registros
                print(f"Registro {i+1}: {row}")
            
            if len(table_data) > 3:
                print(f"\n... e mais {len(table_data) - 3} registros")
            
            # Cria a pasta data se não existir
            data_dir = "./data"
            os.makedirs(data_dir, exist_ok=True)
            
            # Gera timestamp para o nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(data_dir, f"data-{timestamp}.json")
            
            # Salva os dados em arquivo JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(table_data, f, ensure_ascii=False, indent=2)
            
            browser.close()
    except Exception as e:
        print(f"Erro durante o scraping: {e}")
        filename = None
        table_data = []

    return filename, len(table_data)
