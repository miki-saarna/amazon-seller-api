import sys
import os
import pandas
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os
import pickle

from utils.google_sheets.getSpreadsheet import getSpreadsheet
import const

class ShipmentEmailScript:
    def __init__(self):
        self.main()

    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def create_message(self, sender, to, subject, shipment_table):
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        # html = GenCommissionEmail().genHTML(self.report_data)
        html = shipment_table.to_html()
        message.attach(MIMEText(html, 'html'))

        file = os.path.expanduser(f'~/Downloads/SBP_new_shipment.pdf')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        message.attach(part)

        # Return the message as base64url encoded string.
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        return {'raw': raw}
    
    @staticmethod
    def create_draft(service, user_id, message_body):
        try:
            message = {'message': message_body}
            draft = service.users().drafts().create(userId=user_id, body=message).execute()
            print("Draft id: %s\nDraft message: %s" % (draft['id'], draft['message']))
            return draft
        except Exception as e:
            print('An error occurred: %s' % e)
            return None
        
    # @staticmethod
    # def get_filled_rows_to_first_empty(sheet):
    #     data = sheet.get_all_values()
    #     filled_rows_to_first_empty = next((i for i, x in enumerate(data) if all(cell == '' for cell in x)), None)
    #     if filled_rows_to_first_empty is None:
    #         return len(data)
    #     else:
    #         return filled_rows_to_first_empty

        
    def main(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # number_of_filled_rows = self.get_filled_rows_to_first_empty(gs_new_shipment)
        shipment_table = pandas.DataFrame(gs_new_shipment.get_all_records())

        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        sender_email = "myemail@gmail.com"
        to_email = "toemail@gmail.com"
        subject = f'Amazon | New Shipment'
        message = self.create_message(sender_email, to_email, subject, shipment_table)
        draft = self.create_draft(service, 'me', message)


if __name__ == '__main__':
    gs_new_shipment = getSpreadsheet(const.GS_INVENTORY_ID, "Shipment")
    ShipmentEmailScript()

