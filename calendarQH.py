import time
import objects.day as d
import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']

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
        self.weekObj = [[d.day(self.baseDays[i], self.daysInCal[j][i][1], self.daysInCal[j][i][0]) for i in range(7)]for j in range(12)]
        self.sleep = 0
        self.wake = 0
        self.ideal = 0
        self.service = None

        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json')

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
                
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        
    
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

    def getFreeTimeStarts(self):
        starts = []
        for week in self.weekObj:
            for day in week:
                day.getRangeOfStarts()
                starts.append(day.ranges)
                print(day.day, day.ranges,3)
        return starts

    def testingGettingFreeTimeStarts(self):
        starts = []
        day = self.weekObj[0][1]
        day.getRangeOfStarts()
        print(day.ranges)
    
    def addCourses(self):
        for week in self.weekObj:
            for day in week:
                self.addGCSchedule(day, "schedule")
    
    def addCoursesWeek(self, week):
        for day in self.weekObj[week]:
            self.addGCSchedule(day, "schedule")

    def addGCSchedule(self, day, type):
        try:
            if type == "schedule":
                colorID = 7
            elif type == "event":
                colorID = 5
            else:
                colorID = 2
            
            if self.service == None:
                self.service = build("calendar", "v3", credentials=self.creds)

            for event, start, end in day.events:
                startH = start[0]
                startT = str(start[1]) + "0"
                endH = end[0]
                endT = str(end[1]) + "0"
                month = self.baseMonths.index(day.month) + 1
                if month < 10:
                    month = "0" + str(month)
                else:
                    month = str(month)
                if day.num < 10:
                    num = "0" + str(day.num)
                else:
                    num = str(day.num)
                
                if startH < 10:
                    start = "0" + str(startH)
                else:
                    start = str(startH)
                if endH < 10:
                    end = "0" + str(endH)
                else:
                    end = str(endH)
            
                event = {
                    'summary': event,
                    'colorId': colorID,
                    'start': {
                        'dateTime': f'{self.baseY}-{month}-{num}T{start}:{str(startT)}:00',
                        'timeZone': 'America/Toronto'
                    },
                    'end': {
                        'dateTime': f'{self.baseY}-{month}-{num}T{end}:{str(endT)}:00',
                        'timeZone': 'America/Toronto'
                    }
                }

                event = self.service.events().insert(calendarId='primary', body=event).execute()

                print(f"Event created: {event.get('htmlLink')}")
            
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    def clearCal(self):
        self.service.clear(calendarId='primary').execute()
    

              
        

