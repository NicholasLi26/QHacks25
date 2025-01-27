import hour as h

class day:
    def __init__(self, day, month, num):
        self.day = day
        self.hours = [h.hour() for x in range(24)]
        self.freeTime = 144
        self.num = num
        self.month = month
    
    def addEvent(self, event, start, end):
        startH = int(start.split(":")[0])
        startT = int(start.split(":")[1])
        endH = int(float(end.split(":")[0])/10)
        endT = int(float(end.split(":")[1])/10)
        added = True

        if h.hourFull in self.hours[x in range(startH-1, endH)] != True:
            
            if startH == endH:
                self.hours[x].sameHour(event, startT, endT)
            
            for x in range(startH-1, endH):
                if not added:
                    break
                if x == startH-1:
                    added = self.hours[x].start(event, startT)
                elif x == endH-1:
                    added = self.hours[x].end(event, endT)
                else:
                    added = self.hours[x].fillHour(event)

        self.freeTimeChange()

        return added
    
    def freeTimeChange(self):
        counter = 0
        for hour in self.hours:
            counter += hour.getFreeTime()
        
        self.freeTime = counter
    
    def getFreeTime(self):
        return self.freeTime
    
    def getAll(self):
        return self.day, self.month, self.num, self.freeTime
