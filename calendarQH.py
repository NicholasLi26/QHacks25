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
        self.week = [[[" " for i in range(6)] for j in range(24)]for k in range(7)]
        self.freeTimes = [144 for i in range(7)]
        self.sleep = 0
        self.wake = 0

        
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
    
    def setSleepAndWake(self, sleep, wake):
        self.sleep = sleep
        self.wake = wake
    
    def addSleepingTime(self, sleep, wake):
        for day in range(0, 7):
            earliestH, tens = self.findEarliestClass(self.baseDays[day])
            if earliestH != None:
                hour = earliestH-wake-sleep
                if hour < 0:
                    hour = 24 + hour
                    day = (day-1)%7
                self.insertSleep(self.baseDays[day], hour, tens, wake, earliestH)
            
    def insertSleep(self, day, sleep, tens, wake, earliest):
        wakingH = earliest-wake

        for i in range(sleep, 24):
            if i == sleep:
                for j in range(tens, 6):
                    self.week[self.baseDays.index(day)][i][j] = "sleep"
            
            for j in range(0, 6):
                self.week[self.baseDays.index(day)][i][j] = "sleep"

        print("Sleeping time: ", str(sleep)+":"+str(tens), "Waking time: ", str(wakingH)+":"+str(tens), "Day sleeping: ", day)
            
        self.editFreeTimes(self.baseDays[(self.baseDays.index(day)) %7], str(sleep)+":"+str(tens), "24:00")

        for i in range(0, wakingH):
            if i == wakingH-1:
                for j in range(0, tens):
                    self.week[self.baseDays.index(day)+1][i][j] = "sleep"
            
            for j in range(0, 6):
                self.week[self.baseDays.index(day)+1][i][j] = "sleep"

        self.editFreeTimes(self.baseDays[self.baseDays.index(day)+1], str('0:00'), str(wakingH)+":"+str(tens))

    def addEvent(self, event, day, start, end):
        max = abs(int(start.split(":")[0]) - int(end.split(":")[0]))
        print(int(start.split(":")[1]), int(end.split(":")[1]))
        print(int(start.split(":")[1] /10.0), int(end.split(":")[1] /10.0 ))
        for i in range(max):
            if i == 0:
                for x in range(int(start.split(":")[1]/10.0), 6):
                    self.week[self.baseDays.index(day)][int(start.split(":")[0])-1][x] = event
            
            elif i != max-1:
                for x in range(0, 6):
                    self.week[self.baseDays.index(day)][int(start.split(":")[0])-1+i][x] = event
            elif i == max-1:
                for x in range(0, int(end.split(":")[1] / 10.0)):
                    self.week[self.baseDays.index(day)][end.split(":"[0])-1][x] = event
        self.editFreeTimes(day, start, end)
    
    def editFreeTimes(self, day, start, end):
        max = abs(int(start.split(":")[0]) - int(end.split(":")[0]))
        
        for i in range(max):
            if i == 0:
                for x in range(int(start.split(":")[1] / 10.0), 6):
                    self.freeTimes[self.baseDays.index(day)] -= 1
            
            elif i != max -1:
                for x in range(0, 6):
                    self.freeTimes[self.baseDays.index(day)] -= 1
            elif i == max-1:
                for x in range(0, int(end.split(":")[1] / 10.0)):
                    self.freeTimes[self.baseDays.index(day)] -= 1
        
    def freeTimesF(self):
        counter = 0
        for day in range(0, 7):
            for hour in range(0, 24):
                for tens in range(0, 6):
                    if self.week[day][hour][tens] == "":
                        counter += 1
        
        return counter

    def freeTimeDay(self, day):
        counter = 0
        for hour in range(0, 24):
            for tens in range(0, 6):
                if self.week[self.baseDays.index(day)][hour][tens] == "":
                    counter += 1
        
        return counter
    
    def getDay(self, day):
        return self.week[self.baseDays.index(day)]
    
    def printCalendar(self):
        for day in self.week:
            print(day)
    
    def findEarliestClass(self, day):
        for hour in range(0, 24):
            for tens in range(0, 6):
                if self.week[self.baseDays.index(day)][hour][tens] != ' ':
                    return hour, tens
        return None, None