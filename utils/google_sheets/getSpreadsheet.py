from oauth2client.service_account import ServiceAccountCredentials
import gspread

def getSpreadsheet(gs_id: str, gs_name: str):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(gs_id).worksheet(gs_name)
    return worksheet

if __name__ == '__main__':
    getSpreadsheet()
