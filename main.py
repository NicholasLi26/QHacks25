#from reqestest import ask_gemini, process_gemini
import google.generativeai as genai
import time
import os
import re
import courses as c


class mainManagement:
    def __init__(self):
        self.test = [['BME 393L - 001', '8:30AM', '11:20AM', 'BME 355 - 101', '12:30PM', '1:20PM', 'BME 355 - 001', '1:30PM', '2:20PM', 'BME 361 - 001', '2:30PM', '4:20PM', 'SYDE 552 - 001', '4:30PM', '6:20PM'], ['BME 381 - 001', '9:30AM', '10:50AM', 'BME 393 - 001', '11:00AM', '12:20PM', 'PSYCH 236 - 001', '4:00PM', '5:20PM'], ['BME 301 - 001', '12:30PM', '1:20PM', 'BME 393 - 101', '1:30PM', '2:20PM', 'BME 361 - 001', '2:30PM', '3:20PM', 'BME 361 - 101', '3:30PM', '4:20PM', 'SYDE 552 - 001', '4:30PM', '5:20PM', 'SYDE 552 - 101', '5:30PM', '6:20PM'], ['BME 381 - 001', '9:30AM', '10:50AM', 'BME 393 - 001', '11:00AM', '12:20PM', 'PSYCH 236 - 001', '4:00PM', '5:20PM'], ['BME 381 - 101', '9:30AM', '10:20AM', 'BME 355 - 001', '10:30AM', '12:20PM'], [], []]
        self.courseIDs = []
        self.courseList = []
        # with open('keys/gemini.txt', 'r') as file:
        #     key = file.read()

        # genai.configure(api_key=key)

        # self.model = genai.GenerativeModel(model_name = "gemini-1.5-flash")

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
for course in m.courseList:
    print(course.getCourseID())
    print(course.getTimes())
    print(course.getDays())
    print("\n")