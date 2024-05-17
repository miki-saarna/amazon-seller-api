import sys

import json
import requests
import datetime
import urllib.parse
import urllib.request
import gzip
import time
import os

from utils.google_sheets.getSpreadsheet import getSpreadsheet
from utils.amazon.genHeader import genHeader
from utils.amazon.genAuth import genAuth

import const

def createDateIntervals():
    time_periods = []
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    days_since_last_wednesday = (yesterday.weekday() - 3) % 7
    last_wednesday = yesterday - datetime.timedelta(days=days_since_last_wednesday)

    for _ in range(4):
        start_time = last_wednesday - datetime.timedelta(days=7)
        end_time = last_wednesday - datetime.timedelta(days=1)
        interval = {
            "amazon": {
                "start": start_time.strftime("%Y-%m-%d") + 'T00:00:00-00:00',
                "end": end_time.strftime("%Y-%m-%d") + 'T00:00:00-00:00'
            },
            "google_sheets": start_time.strftime("%b %d") + ' - ' + end_time.strftime("%b %d")
        }
        time_periods.append(interval)
        last_wednesday -= datetime.timedelta(days=7)
    return time_periods


def createSalesReport(interval, headers, auth):
    # data["dataStartTime"] = interval["start"]
    # data["dataEndTime"] = interval["end"]

    data = {
        "reportType": "GET_SALES_AND_TRAFFIC_REPORT",
        "reportOptions": {
            "reportPeriod": "WEEK",
            "asinGranularity": "CHILD"
        },
        'dataStartTime': interval["start"],
        'dataEndTime': interval["end"],
        "marketplaceIds": ["ATVPDKIKX0DER"],
    }

    report_request_response = requests.post("https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports",
        headers=headers,
        auth=auth,
        json=data
    )
    report_request_id = report_request_response.json()['reportId']
    return report_request_id


def getReportDocID(report_request_id, headers, auth):
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


def downloadReport(interval, headers, auth):
    downloaded_report = requests.get('https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/documents/' + interval["report_document_id"],
        headers=headers,
        auth=auth
    )

    report_URL = downloaded_report.json()['url']
    file_name = "~/Downloads/orders_report_" + interval["report_request_id"] + ".json"

    zipRes = urllib.request.urlopen(report_URL)
    compressed_data = zipRes.read()
    decompressed_data = gzip.decompress(compressed_data)
    with open(os.path.expanduser(file_name), "wb") as f:
        f.write(decompressed_data)

    dt = {}
    with open(os.path.expanduser(file_name)) as f:
        dt = json.load(f)
        sales_map = map(createSalesMap, dt['salesAndTrafficByAsin'])
        return sales_map


def updateInventorySheet(interval, sales_map):
    column_number = 8 + interval["iteration_idx"]
    header_row = f'{chr(64 + column_number)}{2}'
    gs_inventory.update(header_row, interval['google_sheets'])

    for _, product in enumerate(sales_map):
        ASIN = product["ASIN"]
        units_ordered = product["unitsOrdered"]
        for idx, row in enumerate(SKU_list):
            if ASIN in row:
                row_number = idx + 3
                cell_address = f'{chr(64 + column_number)}{row_number}'
                gs_inventory.update(cell_address, units_ordered)
                break


def createSalesMap(prod):
    return {
        "ASIN": prod["childAsin"],
        "unitsOrdered": prod["salesByAsin"]["unitsOrdered"]
    }


if __name__ == '__main__':
    intervals = createDateIntervals()
    headers = genHeader()
    auth = genAuth()

    gs_inventory = getSpreadsheet(const.GS_INVENTORY_ID, const.GS_INVENTORY_NAME)
    SKU_list = gs_inventory.col_values(1)[2:]
    
    for idx, interval in enumerate(intervals):
        interval["iteration_idx"] = idx
        interval["report_request_id"] = createSalesReport(interval["amazon"], headers, auth)
        interval["report_document_id"] = getReportDocID(interval["report_request_id"], headers, auth)
        sales_map = downloadReport(interval, headers, auth)
        updateInventorySheet(interval, sales_map)

        
    update_row = f'{chr(64 + 2)}{1}'
    gs_inventory.update(update_row, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
