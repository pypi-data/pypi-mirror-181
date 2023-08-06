# -*- coding: UTF-8 -*-

class Logger:

    def __init__(self):
        pass

    @staticmethod
    def INFO_ERR(info):
        print("[\033[1;37;41mE RR\033[0m]\t" + info)

    @staticmethod
    def INFO_NOTE(info):
        print("[\033[1;36mINFO\033[0m]\t" + info)

    @staticmethod
    def INFO_SUCC(info):
        print("[\033[1;32mSUCC\033[0m]\t" + info)