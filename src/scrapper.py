import logging
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, headless=True):
        self.logger = logging.getLogger(__name__)
        self.headless = headless

    def extract_table_data(self, html):
        """Extract data from the #rentabilidadeTable and return a list of dictionaries"""
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"id": "rentabilidadeTable"})

        if not table:
            print("Table #rentabilidadeTable not found in the HTML.")
            return []

        # Extract only the data (ignore the header)
        data_rows = []
        tbody = table.find("tbody")

        if tbody:
            # If there is a tbody, get all rows from the tbody
            rows = tbody.find_all("tr")
        else:
            # If there is no tbody, get all rows except the first (header)
            all_rows = table.find_all("tr")
            rows = all_rows[1:] if len(all_rows) > 1 else []

        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 4:  # Needs at least 4 columns to extract relevant data
                row_data = {}

                # Get the title from the second column (index 1)
                titulo = cells[1].get_text().strip() if len(cells) > 1 else ""

                # Get minimum investment from the correct position
                if len(cells) >= 4:
                    investimento_minimo = (
                        cells[3].get_text().strip() if len(cells) > 3 else ""
                    )
                else:
                    investimento_minimo = (
                        cells[2].get_text().strip() if len(cells) > 2 else ""
                    )

                # Get annual return
                rendimento_anual = cells[4].get_text().strip() if len(cells) > 4 else ""

                # Get expiration date
                vencimento = cells[5].get_text().strip() if len(cells) > 5 else ""

                row_data = {
                    "titulo": titulo,
                    "investimento_minimo": investimento_minimo,
                    "rendimento_anual": rendimento_anual,
                    "vencimento": vencimento,
                    "data_extracao": datetime.now().isoformat(),
                }

                # Only add if there is at least a minimum investment
                if investimento_minimo:
                    data_rows.append(row_data)

        return data_rows

    def get_page_html(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(
                    "https://www.tesourodireto.com.br/produtos/dados-sobre-titulos/rendimento-dos-titulos"
                )
                page.wait_for_selector(
                    "#rentabilidadeTable"
                )  # wait for the table to load
                html = page.content()

                browser.close()
            return html
        except Exception as e:
            self.logger.error(f"Error fetching page HTML: {e}")
            return None

    def execute(self):
        try:
            html = self.get_page_html()

            if not html:
                self.logger.error("Failed to retrieve HTML content.")
                return None, 0

            # Extract the data from the table
            table_data = self.extract_table_data(html)

            # Show the results
            self.logger.info(f"Found {len(table_data)} records in the table:")
            for i, row in enumerate(table_data[:3]):  # Show only the first 3 records
                self.logger.info(f"Record {i+1}: {row}")

            if len(table_data) > 3:
                self.logger.info(f"... and {len(table_data) - 3} more records")

            # Create output directory if it doesn't exist
            data_dir = "./data"
            os.makedirs(data_dir, exist_ok=True)

            # Generate timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(data_dir, f"data-{timestamp}.json")

            # Save the data to a JSON file
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(table_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            filename = None
            table_data = []

        return filename, len(table_data)
