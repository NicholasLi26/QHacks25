import time

class calendarQH:
    def __init__(self):
        self.baseD = "sun"
        self.baseN = 5
        self.baseY = 2025
        self.baseM = 1
        self.daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.weeks = [[0 for i in range(7)] for j in range(12)]
        self.baseDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        self.baseMonths = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]  
        self.monthOffsets = [0,]
        self.makeNumCalendar()

        
    def makeNumCalendar(self):
        copy = self.baseN
        index = 0
        for week in range(0, 12):
            for day in range(0, 7):
                self.weeks[week][day] = copy
                if copy < self.daysPerMonth[index]:
                    copy += 1
                else:
                    copy = 1
                    index += 1
