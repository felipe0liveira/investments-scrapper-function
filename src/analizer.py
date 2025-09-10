from datetime import datetime
import json
import re
import unicodedata

from src.models import InvestmentRecord


def analize(investments_list: list[dict]) -> list[InvestmentRecord]:
    try:
        db_records: list[InvestmentRecord] = []

        for record in investments_list:
            record = record or {}
            title = record.get("titulo", None)
            slug = (
                re.sub(
                    r"[^a-zA-Z0-9]+",
                    "-",
                    unicodedata.normalize("NFKD", title)
                    .encode("ascii", "ignore")
                    .decode("utf-8")
                    .lower(),
                ).strip("-")
                if title
                else None
            )
            minimum_investment = record.get("investimento_minimo", None)
            annual_yield = record.get("rendimento_anual", None)
            due_date = record.get("vencimento", None)
            due_iso_format = (
                datetime.strptime(due_date, "%d/%m/%Y").date().isoformat()
                if due_date
                else None
            )
            extraction_date = record.get("data_extracao", None)

            db_records.append(
                InvestmentRecord.from_dict(
                    {
                        "title": title,
                        "slug": slug,
                        "minimum_investment": minimum_investment,
                        "annual_yield": annual_yield,
                        "due_date": due_iso_format,
                        "extraction_date": extraction_date,
                    }
                )
            )

        return db_records
    except Exception as e:
        print(f"Error while analyzing investments_list: {e}")
        return []
