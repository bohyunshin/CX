import requests
import json
import datetime
import io

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class PF_Bot:
    def __init__(self):
        return

    def login_API(self):
        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://cxpert.bizmsg.io/services/login'

        # ID and PW
        id = "SBH-IND"
        password = "bbeb237230b679a56858a0951458d2e5fc9f62ce67e49fb68284e6d466d08b24"

        # POST에 넘길 ID, PASSWORD 정의
        PARAMS = {'ACCOUNT_ID': id, 'ACCOUNT_PWD': password, 'LOCALE_INFO': 'ko'}

        ses.post(url, data=PARAMS)
        cookieJar = ses.cookies
        for cookie in cookieJar:
            if cookie.value == 'ko':
                break
            login_cookie = cookie.value

        return login_cookie

    def get_PF_Inquire_data(self, _from, _to, _from_hour, _to_hour, cookie):
        """
        _from: Start YearMonthDay in STRING FORMAT
        _to: End YearMonthDay in STRING FORMAT
        cookie: login cookie from login_API function
        """
        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://cxpert.bizmsg.io/services/auth/search/advhist/advisorHistoryExcelDown'

        # POST에 넘길 ID, PASSWORD 정의
        SCH_S_RCV_YMD = _from[:4] + '-' + _from[4:6] + '-' + _from[6:]
        SCH_E_RCV_YMD = _to[:4] + '-' + _to[4:6] + '-' + _to[6:]
        PARAMS = {'MAIN_HIST_YN': 'Y', 'CHOICE_HISTORY_CNT': 0, 'SCH_S_RCV_YMD': SCH_S_RCV_YMD, 'SCH_E_RCV_YMD': SCH_E_RCV_YMD }
        headers = {'Cookie': 'TCK_LOCALE=ko; JSESSIONID=' + cookie,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        response = ses.post(url, data=PARAMS, headers=headers)

        status_code = response.status_code

        with io.BytesIO(response.content) as fh:
            df = pd.io.excel.read_excel(fh, engine='openpyxl')
        # na 안채우면 오류뜸
        df.fillna('', inplace=True)

        # 바로 이전 시간대의 상담 이력을 가져와야 한다
        # 즉, 지금이 3시 05분이라면, 2시 ~ 3시까지의 상담을 가져온다
        df = df[ pd.to_datetime(df['접수일시']).dt.hour == _from_hour]

        return df

    def get_PF_OpStat_data(self, _from, _to, cookie, _from_hour='00', _to_hour='24'):
        """
        _from: Start YearMonthDay in STRING FORMAT
        _to: End YearMonthDay in STRING FORMAT
        _from_hour: Start hour in STRING FORMAT
        _to_hour: End hour in STRING FORMAT
        cookie: login cookie from login_API function
        """

        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://cxpert.bizmsg.io/services/auth/mng/stats/statsList'

        # POST에 넘길 Form Data 정의
        PAGE_NO = 1
        PAGE_SIZE = 10
        BLOCK_SIZE = 10
        STATS_MENU = 'RAWDATA'
        STATS_AUTH = 'MENU_IN_MAIN,MENU_OUT_MAIN,MENU_CHAT_MAIN,MENU_EMAIL_MAIN'
        PROJECT_SEQ = 5

        START_DATE = _from[:4] + '-' + _from[4:6] + '-' + _from[6:]
        END_DATE = _to[:4] + '-' + _to[4:6] + '-' + _to[6:]

        START_HOUR = '0' + str(_from_hour) if str(_from_hour) == 1 else _from_hour
        END_HOUR = '0' + str(_to_hour) if str(_to_hour) == 1 else _to_hour

        START_MINUTE = '00'
        END_MINUTE = '00'
        DATE_UNIT_TYPE = 'DAY'

        PARAMS = {'PAGE_NO':PAGE_NO, 'PAGE_SIZE':PAGE_SIZE,
                  'BLOCK_SIZE':BLOCK_SIZE, 'STATS_MENU':STATS_MENU,
                  'STATS_AUTH':STATS_AUTH, 'PROJECT_SEQ':PROJECT_SEQ,
                  'START_DATE':START_DATE, 'START_HOUR':START_HOUR, 'START_MINUTE':START_MINUTE,
                  'END_DATE':END_DATE, 'END_HOUR':END_HOUR, 'END_MINUTE':END_MINUTE,
                  'DATE_UNIT_TYPE':DATE_UNIT_TYPE}
        headers = {'Cookie' : 'TCK_LOCALE=ko; JSESSIONID=' + cookie}

        response = ses.post(url, data = PARAMS, headers = headers)
        status_code = response.status_code
        content = json.loads(response.content)['rs']

        keys = ['NO', 'MASTER_SEQ', 'BRAND_NM', 'LEVEL1_MENU', 'LEVEL2_MENU', 'LEVEL3_MENU',
                'CUST_NM', 'CUST_PHONE1',
                'SESSION_REG_DT', 'INIT_DT', 'MASTER_REG_DT', 'CHAT_END_DT',
                'TO_COMPLETE_DT', 'ON_STANDBY_DT', 'HISTORY_REG_DT',
                'ADVISORTYPE_SEQ1', 'ADVISORTYPE_SEQ2', 'ADVISORTYPE_SEQ3',
                'ADVISOR_END_DT' ,'CUSTOMER_END_DT', 'SYSTEM_END_DT', 'NAME']

        data = pd.DataFrame()
        for key in keys:
            data[key] = content[key]
        return data

    def append_data(self, sheet_name, data_to_append):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]
        json_file_name = 'wisely-test-235305-76f695b98744.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

        spreadsheetId = '15YkYCMBRi5Bjrpj-xj91qos3No_7-6SMOIcV9pOo5yQ'  # Please set the Spreadsheet ID.

        client = gspread.authorize(credentials)
        sh = client.open_by_key(spreadsheetId)
        values = data_to_append.values.tolist()
        sh.values_append(sheet_name, {'valueInputOption': 'USER_ENTERED'}, {'values': values})