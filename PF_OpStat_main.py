from PF_Bot import PF_Bot
import datetime
import time

if __name__ == '__main__':

    t = datetime.datetime.now()
    year, month, day, hour, minumte = t.year, t.month, t.day, t.hour, t.minute
    current_date = str(year) + ('0' + str(month) if len(str(month)) == 1 else str(month)) + \
                   ('0' + len(str(day)) if str(day) == 1 else str(day))

    PF = PF_Bot()
    cookie = PF.login_API()

    # PF-운영통계 가져오기
    data_to_append_opstat = PF.get_PF_OpStat_data(current_date, current_date, cookie)
    time.sleep(6.317231678)
    PF.append_data('test', data_to_append_opstat)
    time.sleep(5.12948930)