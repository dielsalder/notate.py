class TimeInterval():
    def __init__(self, start, end):
        self.start:float = start
        self.end:float = end
        self.scale_pitch:str
        self.label:str = ""
        # self.label = 'R' if self.average_intensity()<LOUDNESS_THRESHOLD else 'N'

    def __iter__(self):
        return iter((self.start,self.end, self.label))

    def __repr__(self):
        return str((self.start,self.end, self.label))
    
    def __str__(self):
        return repr(self)
    
    def set_rest(self):
        self.label = 'R'
    def set_note(self):
        self.label = 'N'