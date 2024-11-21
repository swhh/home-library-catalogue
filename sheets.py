
from googleapiclient.errors import HttpError


def update_sheet(service, spreadsheet_id, rows, range):
    body = {
        'values': rows
    }
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print(f"Rows appended: {result.get('updates').get('updatedRows')}")
    except HttpError as err:
        print(err)


def remove_duplicates(spreadsheet_id, sheet_id, range_to_check, service):
    
    request = {
        "requests": [
            {
                "deleteDuplicates": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": range_to_check[0],
                        "endRowIndex": range_to_check[1],
                        "startColumnIndex": 0,
                        "endColumnIndex": 2 
                    },
                    "comparisonColumns": [
                        {
                            "sheetId": sheet_id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 2 
                        }
                    ]
                }
            }
        ]
    }
    
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=request
    ).execute()
    
    return response

