import time
import objects.day as d

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
        self.ideal = 0
              
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
    
    def setSleepAndWake(self, ideal, sleepH, wakeH):
        self.sleep = sleepH
        self.wake = wakeH
        self.ideal = int(ideal.split(":")[0])        
        
            
    def insertSleep(self):
        for weekInd in range(0, 12):
            for dayInd in range(0, 7):
                day = self.weekObj[weekInd][dayInd]
                day.setWakeTime(self.wake)
                earliest = day.getEarliest()
                if earliest == None:
                    if self.ideal - self.sleep >= 0:
                        day.addSleepSameDay(str(self.ideal-self.sleep) + ":00", str(self.ideal) + ":00")
                    
                    else:
                        day.addSleepAM(str(self.ideal) + ":00")
                        if dayInd == 0 and weekInd != 0:
                            dayPrevious = self.weekObj[weekInd-1][6]
                            dayPrevious.addSleepPM(str(24 - (self.sleep-self.ideal) ) + ":00")

                        elif dayInd != 0:
                            dayPrevious = self.weekObj[weekInd][dayInd-1]
                            dayPrevious.addSleepPM(str(24 - (self.sleep-self.ideal) ) + ":00")
                    
                else:
                    earliestH = int(earliest.split(":")[0])
                    earliestT = int(float(earliest.split(":")[1])/10)                    
                    if earliestH < self.ideal + self.wake:
                        #print(day.day,  str((24-(self.sleep - earliestH + self.wake))%24) + ":" + str(earliestT*10),str(earliestH-self.wake) + ":" + str(earliestT*10))
                        day.addSleepAM(str(earliestH-self.wake) + ":" + str(earliestT*10))

                        if earliestH - self.sleep - self.wake >= 0:
                            day.addSleepSameDay(str(self.earliest-self.sleep-self.wake) + ":" + str(earliestT*10), str(self.earliest - self.wake) + ":" + str(earliestT*10))
                        
                        else:
                            day.addSleepAM(str(earliestH - self.wake) + ":" + str(earliestT*10))
                            if dayInd == 0 and weekInd != 0:
                                dayPrevious = self.weekObj[weekInd-1][6]
                                #print (str(24-(self.sleep - earliestH + self.wake)) + ":" + str(earliestT*10))
                                dayPrevious.addSleepPM(str(24-(self.sleep - earliestH + self.wake)) + ":" + str(earliestT*10))
                            elif dayInd != 0:
                                dayPrevious = self.weekObj[weekInd][dayInd-1]
                                #print (str(24-(self.sleep - earliestH + self.wake)) + ":" + str(earliestT*10))
                                dayPrevious.addSleepPM(str(24-(self.sleep - earliestH + self.wake)) + ":" + str(earliestT*10))
                    
                    else:
                        #print(day.day, str(24 - (self.sleep-self.ideal) ) + ":00", str(self.ideal) + ":00")
                        if self.ideal - self.sleep >= 0:
                            day.addSleepSameDay(str(self.ideal-self.sleep) + ":00", str(self.ideal) + ":00")
                    
                        else:
                            day.addSleepAM(str(self.ideal) + ":00")
                            if dayInd == 0 and weekInd != 0:
                                dayPrevious = self.weekObj[weekInd-1][6]
                                dayPrevious.addSleepPM(str(24 - (self.ideal-self.sleep) ) + ":00")

                            elif dayInd != 0:
                                dayPrevious = self.weekObj[weekInd][dayInd-1]
                                dayPrevious.addSleepPM(str(24 - (self.ideal-self.sleep) ) + ":00")
                day.addWake()

    def addEvent(self, event, day, start, end):
        #print(event, day, start, end)
        for week in self.weekObj:
            index = self.baseDays.index(day)
            week[index].addEvent(event, start, end)
    
    def getFreeTime(self, week):
        sum = 0
        for day in self.weekObj[week]:
            sum+= day.getFreeTime()
        return sum
    
    def printWeekThings(self, week):
        for day in self.weekObj[week]:
            print(day.day, day.events)
        

