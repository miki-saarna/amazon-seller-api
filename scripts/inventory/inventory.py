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

def createInventoryReport():
    data = {
        "reportType": "GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA",
        "marketplaceIds": ["ATVPDKIKX0DER"]
    }
    report_request_response = requests.post("https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports",
        headers=headers,
        auth=auth,
        json=data
    )
    report_request_id = report_request_response.json()['reportId']
    return report_request_id


def getReportDocID(report_request_id):
    report_status = ''
    while report_status != "DONE":
        report_status_response = requests.get('https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports/' + report_request_id,
            headers=headers,
            auth=auth
        )
        report_status = report_status_response.json()['processingStatus']
        print(report_status)
        if report_status == "DONE":
            report_document_id = report_status_response.json()['reportDocumentId']
            return report_document_id
        else:
            time.sleep(10)


def downloadReport(report_request_id, report_document_id):
    download_report = requests.get('https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/documents/' + report_document_id,
        headers=headers,
        auth=auth
    )
    report_URL = download_report.json()['url']
    file_name = "~/Downloads/inventory_report_" + report_request_id + ".csv"
    urllib.request.urlretrieve(report_URL, os.path.expanduser(file_name))

    DataFrame = pd.read_csv(file_name, sep='\t')
    # value = DataFrame.iloc[4, 9] # reads value found at specified row and column

    for _, row in DataFrame.iterrows():
        sku = row['sku']
        available = row['afn-fulfillable-quantity']
        inbound = row['afn-inbound-shipped-quantity'] + row['afn-inbound-receiving-quantity']
        reserved = row['afn-reserved-quantity']

        for idx, row in enumerate(SKU_list):
            if sku in row:
                row_number = idx + 3
                cell_address = f'{chr(64 + 4)}{row_number}'
                cell_address_inbound = f'{chr(64 + 5)}{row_number}'
                cell_address_reserved = f'{chr(64 + 6)}{row_number}'
                gs_inventory.update(cell_address, available)
                gs_inventory.update(cell_address_inbound, inbound)
                gs_inventory.update(cell_address_reserved, reserved)
                break


if __name__ == '__main__':
    headers = genHeader()
    auth = genAuth()

    report_request_id = createInventoryReport()
    report_document_id = getReportDocID(report_request_id)
    gs_inventory = getSpreadsheet(const.GS_INVENTORY_ID, const.GS_INVENTORY_NAME)
    SKU_list = gs_inventory.col_values(2)[2:]

    downloadReport(report_request_id, report_document_id)
        
    update_row = f'{chr(64 + 2)}{1}'
    gs_inventory.update(update_row, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
