import requests
import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class BIZ_Bot:
    def __init__(self):
        return None

    def login_API(self):
        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://bzm-center.bizmsg.io/services/login'

        # ID and PW
        id = "wisely_admin01"
        password = "wlffpxm1!@"

        # POST에 넘길 ID, PASSWORD 정의
        PARAMS = {'ID': id, 'PASSWORD': password}

        ses.post(url, data=PARAMS)
        cookieJar = ses.cookies
        for cookie in cookieJar:
            login_cookie = cookie.value

        return login_cookie

    def get_BIZ_data(self, _from, _to, cookie, project, channel):
        """
        _from: Start YearMonthDay in STRING FORMAT
        _to: End YearMonthDay in STRING FORMAT
        cookie: login cookie from login_API function
        project: 와이즐리 / 오픈워크 / 헤드웍스 / 와이즐리_상담톡 / My Page
        channel: WEBCHAT / KAKAO
        """

        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://bzm-center.bizmsg.io/services/auth/rawdata/rawdataList'

        PROJECT_SEQ_dict = {'와이즐리':215, '오픈워크':216, '헤드웍스':219, '와이즐리_상담톡': 217, 'My Page':220 }

        # POST에 넘길 Form Data 정의
        BILL_TITLE = f'와이즐리_{project}_{_from}-{_to}'
        SCH_RANGE = 'PJ'
        COMPANY_CD = '와이즐리'
        PROJECT_SEQ = PROJECT_SEQ_dict[project]
        SCH_TERM_S = _from[:4] + '-' + _from[4:6] + '-' + _from[6:]
        SCH_TERM_E = _to[:4] + '-' + _to[4:6] + '-' + _to[6:]

        PARAMS = {'BILL_TITLE' : BILL_TITLE, 'SCH_RANGE' : SCH_RANGE,
                  'COMPANY_CD' : COMPANY_CD, 'PROJECT_SEQ' : PROJECT_SEQ,
                  'CHANNEL_TYPE' : channel,
                  'SCH_TERM_S' : SCH_TERM_S, 'SCH_TERM_E' : SCH_TERM_E}
        headers = {'Cookie' : 'JSESSIONID=' + cookie}

        response = ses.post(url, data = PARAMS, headers = headers)
        status_code = response.status_code
        content = json.loads(response.content)['rs']

        keys = ['COMPANY_NM', 'PROJECT_NM', 'SENDER', 'SESSION_ID',
                'START_TIME', 'END_TIME','USER_KEY', 'REQUESTED','ANSWERED',
                'BILL_TIME', 'BILL']

        result = {}
        for key in keys:
            if key == 'SESSION_ID' and project == '와이즐리_상담톡':
                result[key] = content[key]
            elif key == 'SESSION_ID' and project != '와이즐리_상담톡':
                result[key] = ['null']*len(content['PROJECT_NM'])
            else:
                result[key] = content[key]
        # 해당 날짜에 조회된 데이터 개수
        N = len(result['PROJECT_NM'])
        data = pd.DataFrame()
        # dataframe 만들어줄때 길이를 맞춰줘야함
        # 맨 마지막 값이 없을 경우, 길이가 짧아짐
        for key in keys:
            if len(result[key]) < N:
                data[key] = result[key] + ['NULL']*(N-len(result[key]))
            else:
                data[key] = result[key]
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