from PF_Bot import PF_Bot

if __name__ == '__main__':
    PF = PF_Bot()
    cookie = PF.login_API()
    data_to_append = PF.get_PF_data('20210615','20210615',cookie)