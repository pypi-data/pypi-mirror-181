from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Union


class SheetsApiTry:
    def __init__(self, spreadsheet_id, dir_path):
        self.spreadsheet_id = spreadsheet_id
        self.scopes = "https://www.googleapis.com/auth/spreadsheets"

        creds = None

        # Если вход уже был, то повторная авторизация не нужна
        if os.path.exists(f'{dir_path}{os.sep}token.json'):
            creds = Credentials.from_authorized_user_file(f'{dir_path}{os.sep}token.json', self.scopes)

        # Если авторизации не было
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{dir_path}{os.sep}credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open(f'{dir_path}{os.sep}token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

    def get_cell(self, column_id: str, row_id: Union[str, int], sheet_name: str) -> list:
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                              range=f"{sheet_name}!{column_id}{row_id}").execute()
            values = result.get('values', [])

            if not values:
                return []

            return values
        except HttpError as error:
            print(f"Ошибка: {error}")

    def update_cell(self, range_name: str, sheet_name: str, values: list, value_input_option="USER_ENTERED") -> None:
        try:
            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!{range_name}",
                valueInputOption=value_input_option, body=body).execute()
            print(f"{result.get('updatedCells')} ячейки обновлено.")
        except HttpError as error:
            print(f"Ошибка: {error}")

    def find_rows(self, value: str, sheet_name: str) -> list:
        rows_with_value = list()
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                              range=f"{sheet_name}").execute()
            values = result.get('values', [])

            for row in values:
                if value in row:
                    rows_with_value.append(row)

            return rows_with_value
        except HttpError as error:
            print(f"Ошибка: {error}")
