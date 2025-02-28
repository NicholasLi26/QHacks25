import objects.hour as h

class day:
    def __init__(self, day, month, num):
        self.day = day
        self.hours = [h.hour() for x in range(24)]
        self.freeTime = 144
        self.num = num
        self.month = month
        self.events = []
        self.freeTimeRemoved = 0
        self.wake = 0
        self.ranges = []
        self.starts = []
        self.tensInd = []
    
    def addEvent(self, event, start, end):
        
        startH = int(start.split(":")[0])
        startT = int(float(start.split(":")[1])/10)
        endH = int(end.split(":")[0])
        endT = int(float(end.split(":")[1])/10)

        
        added = True
        full = False
        for x in range(startH, endH+1):
            if self.hours[x].hourFull():
                full = True
                break
        
        if not full:
            if startH == endH or startH == endH - 1 and endT == 0:
                if endT != 0:
                    self.hours[startH-1].sameHour(event, startT, endT)
                else:
                    self.hours[startH].sameHour(event, startT, 6)
            else:
                for x in range(startH, endH+1):
                    if not added:
                        break
                    if x == startH:
                        added = self.hours[x].start(event, startT)
                        
                    elif x == endH:
                        added = self.hours[x].end(event, endT)
                        
                    else:
                        self.hours[x].fillHour(event)
                        
        if added:
            if event not in self.events:
                self.events.append([event, [startH, startT], [endH, endT]])
            self.freeTimeChange()
        if not added:
            print(f"Event could not be added for event {event}")
        return added
    
    def setWakeTime(self, wake):
        self.wake = wake
    
    def freeTimeChange(self):
        counter = 0
        for hour in self.hours:
            counter += hour.getFreeTime()
        
        self.freeTime = counter
        self.removeTenMinuteBlocks()
        self.freeTime -= self.wake*6

    
    def getFreeTime(self):
        self.freeTimeChange()
        return self.freeTime
    
    def getFreeTimeHours(self):
        rem = self.freeTime%60
        self.freeTime -= rem
        return self.freeTime/60
    
    def getFreeTimeMinutes(self):
        return self.freeTime%60
    
    def printFreeTimes(self):
        sum = 0
        for hour in self.hours:
            sum += hour.getFreeTime()
            print(hour.freeTime, sum)
    
    def addSleepAM(self, wake):
        wakeH = int(wake.split(":")[0])
        wakeT = int(float(wake.split(":")[1])/10)
        for x in range(0, wakeH):
            self.hours[x].fillHour("Sleep")
        self.hours[wakeH].end("Sleep", wakeT)
    
    def addSleepPM(self, sleep):
        sleepH = int(sleep.split(":")[0])
        sleepT = int(float(sleep.split(":")[1])/10)
        
        if sleepH != 23:
            for x in range(sleepH+1, 24):
                self.hours[x].fillHour("Sleep")
        self.hours[sleepH].start("Sleep", sleepT)

    def addSleepSameDay(self, sleep, wake):
        sleepH = int(sleep.split(":")[0])
        sleepT = int(float(sleep.split(":")[1])/10)
        wakeH = int(wake.split(":")[0])
        wakeT = int(float(wake.split(":")[1])/10)
        
        for x in range(sleepH, wakeH):
            self.hours[x].fillHour("Sleep")
        self.hours[sleepH].start("Sleep", sleepT)
        self.hours[wakeH].end("Sleep", wakeT)

    def getEarliest(self):
        for i in range(0, 24):
            for j in range(0, 6):
                if self.hours[i].tens[j] != "Empty" and self.hours[i].tens[j] != "Sleep":
                    temp = str(i) + ":" + str(j*10)
                    return (temp)
        
        return None

    def addWake(self):
        last = ""
        setTrigger = False
        ind = [0,0]
        counter = 0
        for hourInd in range(0, 24):
            for tenInd in range(0, 6):
                if setTrigger:
                    if counter < self.wake*6 -1:
                        self.hours[hourInd].tens[tenInd] = "Wake"
                        counter += 1
                else:
                    if self.hours[hourInd].tens[tenInd] == "Empty":
                        if last == "Sleep":
                            setTrigger = True
                            self.hours[hourInd].tens[tenInd] = "Wake"
                    last = self.hours[hourInd].tens[tenInd]

    
    def getAll(self):
        return self.day, self.month, self.num, self.freeTime
    
    def getAllHours(self):
        for hour in self.hours:
            print(hour.tens)

    def removeTenMinuteBlocks(self):
        last = ""
        last2 = ""
        self.tensInd = []
        self.freeTimeRemoved = 0
        for x in range(0, 24):
            for y in range(0, 6):
                if last == "Empty" and last2 != "Empty" and self.hours[x].tens[y] != "Empty":
                    self.freeTimeRemoved += 1
                    if y!=0:
                        self.tensInd.append([x,y-1])
                    elif x!=0:
                        self.tensInd.append([x-1,5]) 
                last2 = last
                last = self.hours[x].tens[y]
                
        self.freeTime -= self.freeTimeRemoved
        
    
    def getIndexOfStart(self):
        last = ""
        self.starts = []
        for x in range(0, 24):
            for y in range(0, 6):
                if last!= "Empty" and self.hours[x].tens[y] == "Empty" and [x,y] not in self.tensInd:
                    self.starts.append([x,y])
                last = self.hours[x].tens[y]
        
    
    def getRangeOfStarts(self):
        
        self.ranges = []
        counter = 0
        self.getIndexOfStart()
        print(self.starts,1)
        print(self.tensInd,2) 

        for x, y in self.starts:
            while self.hours[x].tens[y] == "Empty":
                counter += 1
                y += 1
                if y == 6:
                    y = 0
                    x += 1
                if x == 24:
                    break
            self.ranges.append(counter)
            counter = 0
            
        
        
    
    
                
                
        
