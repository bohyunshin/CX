from BIZ_Bot import BIZ_Bot
import datetime
import time

if __name__ == '__main__':

    t = datetime.datetime.now()
    year, month, day, hour, minumte = t.year, t.month, t.day, t.hour, t.minute
    current_date = str(year) + ('0'+str(month) if str(month) == 1 else str(month)) + ('0'+str(day) if str(day) == 1 else str(day))

    # BIZ 데이터 다운받기
    project_list = ['와이즐리','오픈워크','헤드웍스','와이즐리_상담톡','My Page']
    channel_list = ['WEBCHAT','WEBCHAT','WEBCHAT','KAKAO','WEBCHAT']
    sheet_list = ['BIZ_WEB_WS','BIZ_WEB_OW','BIZ_WEB_HW','BIZ_KAKAO','BIZ_WEB_MyPage']
    BIZ = BIZ_Bot()
    # 로그인을 위한 쿠키 받기
    cookie = BIZ.login_API()

    # 구글시트에 데이터 쏘기
    for project, channel, sheet in zip(project_list, channel_list, sheet_list):
        data_to_append = BIZ.get_BIZ_data(current_date,current_date,cookie,project,channel)
        time.sleep(5.412312)
        BIZ.append_data(sheet, data_to_append)
        time.sleep(7.631728)