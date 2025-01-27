import time
import day as d

class calendarQH:
    def __init__(self):
        self.baseD = "sun"
        self.baseM = "jan"
        self.baseN = 5
        self.baseY = 2025
        self.baseM = 1
        self.daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.baseDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        self.baseMonths = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]  
        self.daysInCal = self.makeNumCalendar()
        self.monthOffsets = [0,]
        self.weekObj = [[d.day(self.baseDays[i], self.daysInCal[j][i][1], self.daysInCal[j][i][0]) for i in range(7)]for j in range(12)]
        self.sleep = 0
        self.wake = 0
              
    def makeNumCalendar(self):
        copy = self.baseN
        index = 0
        days = [[[0, ""] for i in range(7)] for j in range(12)]
        for week in range(0, 12):
            for day in range(0, 7):
                days[week][day] = [copy, self.baseMonths[index]]
                if copy < self.daysPerMonth[index]:
                    copy += 1
                else:
                    copy = 1
                    index += 1
        return days
    
    def setSleepAndWake(self, sleep, wake):
        self.sleep = sleep
        self.wake = wake
    
    def addSleepingTime(self, sleep, wake):
        noContention = True
        return noContention
            
    def insertSleep(self, day, sleep, tens, wake, earliest):
        noContention = True
        return noContention

    def addEvent(self, event, day, start, end):
        for week in self.weekObj:
            index = self.baseDays.index(day)

            week[index].addEvent(event, start, end)

