import sys

import requests
import datetime
import urllib.parse
import urllib.request
import time
import os
import pandas as pd

from utils.google_sheets.getSpreadsheet import getSpreadsheet
from utils.amazon.genHeader import genHeader
from utils.amazon.genAuth import genAuth

import const

class Gen_Inventory_Report():
    def __init__(self) -> None:
        self.SP_API_URL = "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30"
        self.headers = genHeader()
        self.auth = genAuth()
        self.report_request_id = self.create_inventory_report()
        self.report_document_id = self.get_report_doc_id()
        self.gs_inventory = getSpreadsheet(const.GS_INVENTORY_ID, const.GS_INVENTORY_NAME)
        self.sku_list = self.gs_inventory.col_values(2)[2:]
        self.download_report()
        self.extract_inventory_from_report()
        self.gs_inventory.batch_update(self.data)
        self.update_row = f'{chr(64 + 2)}{1}'
        self.gs_inventory.update(self.update_row, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        
    def create_inventory_report(self):
        data = {
            "reportType": "GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA",
            "marketplaceIds": ["ATVPDKIKX0DER"]
        }
        report_request_response = requests.post(f"{self.SP_API_URL}/reports",
            headers=self.headers,
            auth=self.auth,
            json=data
        )
        report_request_id = report_request_response.json()['reportId']
        return report_request_id
    
    def get_report_doc_id(self):
        start_time = datetime.datetime.now().timestamp()
        report_status = ''
        while report_status != "DONE":
            report_status_response = requests.get(f"{self.SP_API_URL}/reports/{self.report_request_id}",
                headers=self.headers,
                auth=self.auth
            )
            report_status = report_status_response.json()['processingStatus']
            print(report_status)
            if report_status == "DONE":
                report_document_id = report_status_response.json()['reportDocumentId']
                return report_document_id
            elif report_status == "FATAL":
                break
            else:
                current_time = datetime.datetime.now().timestamp()
                surpassed_time = current_time - start_time
                if surpassed_time > 120:
                    break
                else:
                  time.sleep(10)

    def download_report(self):
        download_report = requests.get(f"{self.SP_API_URL}/documents/{self.report_document_id}",
            headers=self.headers,
            auth=self.auth
        )
        report_URL = download_report.json()['url']
        self.file_name = f"~/Downloads/inventory_report_{self.report_request_id}.csv"
        urllib.request.urlretrieve(report_URL, os.path.expanduser(self.file_name))

    def extract_inventory_from_report(self):
        DataFrame = pd.read_csv(self.file_name, sep='\t')

        self.data = []

        for _, row in DataFrame.iterrows():
            sku = row['sku']
            available = row['afn-fulfillable-quantity']
            inbound = row['afn-inbound-shipped-quantity'] + row['afn-inbound-receiving-quantity']
            reserved = row['afn-reserved-quantity']

            for idx, row in enumerate(self.sku_list):
                if sku in row:
                    row_number = idx + 3

                    self.data.append({
                        "range": f'{chr(64 + 4)}{row_number}',
                        "values": [[available]]
                    })
                    self.data.append({
                        "range": f'{chr(64 + 5)}{row_number}',
                        "values": [[inbound]]
                    })
                    self.data.append({
                        "range": f'{chr(64 + 6)}{row_number}',
                        "values": [[reserved]]
                    })

                    break # is break necessary here?

if __name__ == '__main__':
    Gen_Inventory_Report()
