from datetime import datetime
import json
import re
import unicodedata


def analize(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

            db_records = []

            for record in data:
                record = record or {}
                title = record.get('titulo', None)
                slug = re.sub(r'[^a-zA-Z0-9]+', '-', unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8').lower()).strip('-') if title else None
                minimum_investment = record.get('investimento_minimo', None)
                annual_yield = record.get('rendimento_anual', None)
                due_date = record.get('vencimento', None)
                due_iso_format = datetime.strptime(due_date, "%d/%m/%Y").date().isoformat() if due_date else None
                extraction_date = record.get('data_extracao', None)

                db_records.append({
                    'title': title,
                    'slug': slug,
                    'minimum_investment': minimum_investment,
                    'annual_yield': annual_yield,
                    'due_date': due_iso_format,
                    'extraction_date': extraction_date
                })

            return db_records
    except Exception as e:
        print(f"Erro ao ler o arquivo {filename}: {e}")
        return []