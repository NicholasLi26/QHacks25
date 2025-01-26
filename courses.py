class courses:
    def __init__(self, courseID, start, end, day):    
        self.courseID = courseID
        self.ranking = 0
        self.times = []
        self.days = []
        self.addTime(start, end, day)

    def setRanking(self, ranking):
        self.ranking = ranking
    
    def addTime(self, start, end, day):
        self.times.append((start, end, day))
        self.days.append(day)

    def getTimes(self):
        return self.times
    
    def getDays(self):
        return self.days
    
    def getCourseID(self):
        return self.courseID
    
    
