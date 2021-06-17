import requests
import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class PF_Bot:
    def __init__(self):
        return None

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

    def get_PF_data(self, _from, _to, cookie):
        ses = requests.Session()
        ses.headers['User-Agent'] = 'Mozilla/5'
        url = 'https://cxpert.bizmsg.io/services/auth/search/advhist/advisorHistoryExcelDown'

        # ID and PW
        id = "SBH-IND"
        password = "bbeb237230b679a56858a0951458d2e5fc9f62ce67e49fb68284e6d466d08b24"

        # POST에 넘길 ID, PASSWORD 정의
        PARAMS = {'MAIN_HIST_YN': 'Y', 'CHOICE_HISTORY_CNT': 0, 'SCH_S_RCV_YMD': '2021-06-17', 'SCH_E_RCV_YMD': '2021-06-17' }
        headers = {'Cookie': 'TCK_LOCALE=ko; JSESSIONID=' + cookie}

        response = ses.post(url, data=PARAMS)

        status_code = response.status_code
        print(status_code)
        print(response.content)
        # content = json.loads(response.content)

        # print(content)