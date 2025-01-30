class queryObj:
    def __init__(self):
        self.query = []
    
    def addQuery(self, query):
        self.query.append(query)
    
    def getQuery(self):
        return self.query
    
    def queryIsEmpty(self):
        return len(self.query) == 0
