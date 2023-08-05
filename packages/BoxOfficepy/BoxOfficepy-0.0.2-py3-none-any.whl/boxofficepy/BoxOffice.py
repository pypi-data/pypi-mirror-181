import requests
import pandas as pd
from requests_html import HTML

class RevenueAPI(object):

    url = 'https://www.boxofficemojo.com/year/world/'

    def __init__(self):
        pass
    
    def get_text_response(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            html_text = r.text
            return html_text
        return ""

    def get_details(self):
        html_text = self.get_text_response()
        r_html = HTML(html=html_text)

        table_class = ".imdb-scroll-table"
        r_table =  r_html.find( table_class )

        table_data = []
        header_names = []
        if len(r_table) == 1:
            parsed_table = r_table[0]
            rows = parsed_table.find("tr")

            header_row = rows[0]
            header_cols = header_row.find('th')

            header_names = [x.text for x in header_cols]

            for row in rows[1:]:
                cols = row.find("td")
                row_data = []
                for i,col in enumerate(cols):
                    row_data.append(col.text)
                table_data.append(row_data)
        return header_names, table_data