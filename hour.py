class hour:
    def __init__(self):
        self.tens = ["Empty" for x in range(6)]
        self.freeTime = 6

    def start(self, event, start):
        noContention = True
        temp = self.tens.copy()

        for x in range(start-1, 5):
            if self.tens[x] != "Empty":
                noContention = False
                break
            temp[x] = event
        
        if noContention:
            self.tens = temp
            self.freeTime -= 6-start
            
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
            self.tens = temp
            self.freeTime -= end

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
            self.tens = temp
            self.freeTime -= end-start

        return noContention

    def fillHour(self, event):
        for x in range(0, 6):
            self.tens[x] = event
        self.freeTime = 0
    
    def getFreeTime(self):
        return self.freeTime

    def hourFull(self):
        return self.freeTime == 0