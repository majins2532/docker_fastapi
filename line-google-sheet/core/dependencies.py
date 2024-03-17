from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader

# import schemas
from core.settings import API_TOKEN_KEY, USER_API, SECRET_KEY, ALGORITHM, KEYGOOGLE
import gspread
from oauth2client.service_account import ServiceAccountCredentials
header_scheme = APIKeyHeader(name="api-token-key")

def test_google(sheet,url,datas):
    # Authenticate with Google Sheets
    gc = gspread.service_account_from_dict(KEYGOOGLE)

    # Open the Google Sheet by URL
    wb = gc.open_by_url(url) # A URL of your workbook.
    sheet1 = wb.worksheet(sheet) # Enter your sheet name.
    # Define the row data
    for data in datas:
        sheet1.append_row(data)

    # Append the row to the sheet
    original_df = sheet1.get_all_values()
    #print(original_df)

def set_data_log(data_request,data_response,data_error):
    data_log = {
        "data_request": data_request,
        "data_response": data_response,
        "data_error": data_error
    }
    return data_log

async def get_token_header(api_token_key: str = Depends(header_scheme)):
    if api_token_key != API_TOKEN_KEY:
        err = {
            "error_code": "E100",
            "message": {
                "massage_th": "API-TOKEN-KEY ไม่ถูกต้อง",
                "massage_en": "API-TOKEN-KEY not correct",
            }
        }
        raise HTTPException(status_code=401, 
            detail=set_data_log("",err,err))