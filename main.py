#from reqestest import ask_gemini, process_gemini
import PIL.Image
import google.generativeai as genai
import time
import os
import re
import objects.courses as c
import calendarQH as cq
from reqestest import ask_gemini, process_gemini, ask_gemini_Text


class mainManagement:
    def __init__(self):
        self.test = [['BME 393L - 001', '8:30AM', '11:20AM', 'BME 355 - 101', '12:30PM', '1:20PM', 'BME 355 - 001', '1:30PM', '2:20PM', 'BME 361 - 001', '2:30PM', '4:20PM', 'SYDE 552 - 001', '4:30PM', '6:20PM'], ['BME 381 - 001', '9:30AM', '10:50AM', 'BME 393 - 001', '11:00AM', '12:20PM', 'PSYCH 236 - 001', '4:00PM', '5:20PM'], ['BME 301 - 001', '12:30PM', '1:20PM', 'BME 393 - 101', '1:30PM', '2:20PM', 'BME 361 - 001', '2:30PM', '3:20PM', 'BME 361 - 101', '3:30PM', '4:20PM', 'SYDE 552 - 001', '4:30PM', '5:20PM', 'SYDE 552 - 101', '5:30PM', '6:20PM'], ['BME 381 - 001', '9:30AM', '10:50AM', 'BME 393 - 001', '11:00AM', '12:20PM', 'PSYCH 236 - 001', '4:00PM', '5:20PM'], ['BME 381 - 101', '9:30AM', '10:20AM', 'BME 355 - 001', '10:30AM', '12:20PM'], [], []]
        self.courseIDs = []
        self.courseList = []
        self.cal = cq.calendarQH()
        with open('keys/gemini.txt', 'r') as file:
            key = file.read()

        genai.configure(api_key=key)

        self.model = genai.GenerativeModel(model_name = "gemini-1.5-flash")

    def initializeCalendar(self):
        for course in self.courseList:
            courseID = course.getCourseID()
            list = course.getTimes()
            #print( courseID, list)
            for start, end, day in list:
                self.cal.addEvent(courseID, day, start, end)

            

            #
            # Refer to the Python quickstart on how to setup the environment:
            # https://developers.google.com/calendar/quickstart/python
            # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
            # stored credentials.

            # recurring_course = {
            # 'summary': courseID,
            # 'start': {
            #     'dateTime': f'2025-01-{jan_days[day]}T{start}:00.000',
            #     'timeZone': 'America/Toronto'
            # },
            # 'end': {
            #     'dateTime': f'2011-01-{jan_days[day]}T{end}:00.000',
            #     'timeZone': 'America/Toronto'
            # },
            # 'recurrence': [
            #     f'RRULE:FREQ=WEEKLY;UNTIL=202503{mar_days[day]}T170000Z',
            # ],
            # }

            #recurring_event = service.events().insert(calendarId='primary', body=recurring_course).execute()
            # calendar object for google calendar? haven't really properly investigated the rest of the api to know what to do with this but there's a python setup guide

            # print recurring_event['id']


            #

    def initialize1Event(self):
        courseID = self.courseList[1].getCourseID()
        list = self.courseList[1].getTimes()
        for start, end, day in list:
            self.cal.addEvent(courseID, day, start, end)

    def initializeCourse(self, id, start=None, end=None, day=None):
        if id not in self.courseIDs:
            self.courseIDs.append(id)
            temp = c.courses(id, start, end, day)
            self.courseList.append(temp)
        else:
            for course in self.courseList:
                if course.getCourseID() == id:
                    course.addTime(start, end, day)


    def ProcessSchedule(self):
        pathS = "scheduleImages"
        imageNames = os.listdir(r"scheduleImages")
        for imageName in imageNames:
            print(pathS+imageName)
    
    def ProcessSyllabus(self):
        
        foldersInImage = os.listdir("runtimeImages")
        syllabusArray = [len(foldersInImage)]
        
        for folders in foldersInImage:
            syllabusArray.append(os.listdir(f"runtimeImages/{folders}"))
        
        print(syllabusArray)

    def splitList(self, list):
        templist = []
        while len(list) > 0:
            if len(list) < 3:
                templist.append(list)
                break
            templist.append(list[:3])
            list = list[3:]
        return templist
    
    def calendarSchedule(self):
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        ind = 0
        for day in self.test:
            daySplit = self.splitList(day)
            
            for subject, start, end in daySplit:
                subject = subject.split(" - ")[0]
                half = start[-2:]
                if half == "AM":
                    start = start[:-2]
                    if start.split(":")[0] == "12":
                        start = "00:" + start.split(":")[1]
                    end = end[:-2]
                    if end.split(":")[0] == "12":
                        end = "00:" + end.split(":")[1]
                else:
                    start = start[:-2]
                    if start.split(":")[0] != "12":
                        start = str(int(start.split(":")[0]) + 12) + ":" + start.split(":")[1]
                    end = end[:-2]
                    if end.split(":")[0] != "12":
                        end = str(int(end.split(":")[0]) + 12) + ":" + end.split(":")[1]
                    

                self.initializeCourse(subject, start, end, days[ind])
            ind += 1
    
    
                


        

            

m = mainManagement()
# m.ProcessSyllabus()
# m.ProcessSchedule()
m.calendarSchedule()
m.initializeCalendar()
#m.initialize1Event()
m.cal.printWeekThings(0)
m.cal.setSleepAndWake("8:00", 8, 2)

m.cal.insertSleep()
print(m.cal.weekObj[1][1].getFreeTime())
print(m.cal.weekObj[1][0].getAllHours())
print(m.cal.weekObj[1][1].getAllHours())
