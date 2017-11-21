import datetime


class TimeService:
    __timeStringFormat = "%Y-%m-%d_%H-%M-%S-%f"

    def __init__(self):
        pass

    def getTimestampStringNow(self):
        return datetime.datetime.now().strftime(self.__timeStringFormat)

    def getTimestampDatetimeObjectNow(self):
        return datetime.datetime.now()

    def getDateObjectFromTimeString(self, timeString):
        return datetime.datetime.strptime(timeString, self.__timeStringFormat)

    def isDataObjectOutofTime(self, dateToCheck, timeoutMS):
        timeDelta = self.getTimestampDatetimeObjectNow() - dateToCheck
        timeDeltaMS = timeDelta.total_seconds()*1000
        return timeDeltaMS > timeoutMS
