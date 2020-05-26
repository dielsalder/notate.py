class TimeInterval():
    def __init__(self, start, end, label = ""):
        self.start:float = start
        self.end:float = end
        self.scale_pitch:str
        self.label:str = label
        # self.label = 'R' if self.average_intensity()<LOUDNESS_THRESHOLD else 'N'

    def __iter__(self):
        return iter((self.start,self.end, self.label))

    def __repr__(self):
        return str((self.start,self.end, self.label))
    
    def __str__(self):
        return repr(self)