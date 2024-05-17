import sys

from utils.google_sheets.getSpreadsheet import getSpreadsheet
import const

class ShipmentScript:
    def __init__(self):
        gs_new_shipment.clear() # unsure if this also clears formatting
        self.genShipmentData()
        self.format_gs()

    header = ['SKU', 'Product name', 'Cases', 'Units', 'Available', '90-day sales (est)', 'remaining supply (days)', 'new shipment (est)']
    data = [header]

    def genShipmentData(self):
        for row in gs_inventory.get_all_values()[2:]:
            remaining_days = row[12]

            if remaining_days:
                if int(remaining_days) < 40:
                    SKU = row[1]
                    units_per_case = 0
                    for _, case_row in enumerate(gs_case_data.get_all_values()[1:]):
                        if SKU in case_row[1]:
                            units_per_case = int(case_row[3])

                    new_shipment_est = int(row[13]) # explore algorithms to best calculate new shipment est

                    product_name = row[2]
                    case_quantity = round(new_shipment_est / units_per_case)
                    unit_quantity = case_quantity * units_per_case
                    current_quantity = int(row[3]) + int(row[4]) + int(row[5])
                    sales_90_days = int(row[11])

                    item_restock_row = [SKU, product_name, case_quantity, unit_quantity, current_quantity, sales_90_days, remaining_days, new_shipment_est]
                    self.data.append(item_restock_row)
        gs_new_shipment.append_rows(self.data)

    def format_gs(self):
        header_range = f'A{1}:H{1}'
        header_format = {'textFormat': {'bold': True}, 'backgroundColor': {'red': 243/255, 'green': 243/255, 'blue': 243/255, 'alpha': 1.0}}
        gs_new_shipment.format(header_range, header_format)

        meta_data_range = f'E{2}:H{len(self.data)}'
        meta_data_format = {'backgroundColor': {'red': 217/255, 'green': 234/255, 'blue': 211/255, 'alpha': 1.0}}
        gs_new_shipment.format(meta_data_range, meta_data_format)

if __name__ == '__main__':
    gs_inventory = getSpreadsheet(const.GS_INVENTORY_ID, const.GS_INVENTORY_NAME)
    gs_new_shipment = getSpreadsheet(const.GS_INVENTORY_ID, "Shipment")
    gs_case_data = getSpreadsheet("137LXGLm_o6KZejsfMcGtkqX9s_-EWMM8AkETjng200U", "Case")

    ShipmentScript()

    # gs_new_shipment.insert_row(["Created", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")], 1)
