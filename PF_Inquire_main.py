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

    # PF-조회 가져오기
    data_to_append_inquire = PF.get_PF_Inquire_data(current_date,current_date, hour-1, hour,cookie)
    time.sleep(5.412312)
    PF.append_data('PF_Inquire', data_to_append_inquire)
    time.sleep(7.631728)