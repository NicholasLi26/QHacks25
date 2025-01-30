class hour:
    def __init__(self):
        self.tens = ["Empty" for x in range(6)]
        self.freeTime = 6
        self.events = []

    def start(self, event, start):
        noContention = True
        temp = self.tens.copy()
        
        for x in range(start, 6):
            if self.tens[x] != "Empty":
                noContention = False
                break
            temp[x] = event
        
        if noContention:
            self.tens = temp.copy()
            self.freeTime -= 6-start
            if event not in self.events:
                self.events.append(event)
        
        return noContention
    
    def end(self, event, end):
        noContention = True
        temp = self.tens.copy()
        for x in range(0, end):
            if self.tens[x] != "Empty":
                noContention = False
                break
            temp[x] = event
        
        if noContention:
            self.tens = temp.copy()
            self.freeTime -= end
            if event not in self.events:
                self.events.append(event)
        
        return noContention
    
    def sameHour(self, event, start, end):
        noContention = True
        temp = self.tens.copy()

        for x in range(start-1, end):
            if self.tens[x] != "Empty":
                noContention = False
                break
            temp[x] = event
        
        if noContention:
            self.tens = temp.copy()
            self.freeTime -= end-start
            if event not in self.events:
                self.events.append(event)
        
        return noContention

    def fillHour(self, event):
        for x in range(0, 6):
            self.tens[x] = event
        self.freeTime = 0
        if event not in self.events:
            self.events.append(event)
    
    def getFreeTime(self):
        return self.freeTime

    def hourFull(self):
        return self.freeTime == 0