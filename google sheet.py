import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import gspread_dataframe as gd
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = '/Users/wisely/Desktop/intern/CX/wisely-test-235305-76f695b98744.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

spreadsheetId = '1b_DaELg77XQQTVqohRUWyX7eqy8KvQY5Gp8VdOXNa2c'  # Please set the Spreadsheet ID.
sheetName = 'Sheet1'  # Please set the sheet name.

client = gspread.authorize(credentials)
sh = client.open_by_key(spreadsheetId)
df2 = pd.DataFrame({'col1': ['a1', 'a2', 'a3'], 'col2': ['b1', 'b2', 'b3'], 'col4': ['b1', 'b2', 'b3'] })  # This is a sample value.
values = df2.values.tolist()
sh.values_append(sheetName, {'valueInputOption': 'USER_ENTERED'}, {'values': values})

# gc = gspread.authorize(credentials)
# repurch_rate_url = 'https://docs.google.com/spreadsheets/d/1b_DaELg77XQQTVqohRUWyX7eqy8KvQY5Gp8VdOXNa2c/edit#gid=0'
# repurch_rate_ss = gc.open_by_url(repurch_rate_url)
# repurch_rate_ws = repurch_rate_ss.worksheet('Sheet1')
# repurch_rate_df = get_as_dataframe(repurch_rate_ws, evaluate_formulas=True)
#
# df = pd.DataFrame({'col1': ['a1', 'a2', 'a3'], 'col2': ['b1', 'b2', 'b3'], 'col3': ['b1', 'b2', 'b3'] })  # This is a sample value.
# updated = repurch_rate_df.append(df)
# gd.set_with_dataframe(repurch_rate_ws, updated)