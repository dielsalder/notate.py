from SoundProperties import SoundProperties
from TimeInterval import TimeInterval
import bisect

class SegmentSet():
    def __init__(self, sound_properties):
        # bisect for maintaining sorted list
        self.boundaries:[float] = [0.0,]
        # label i in self.labels corresponds to the interval (i, i+1) in self.boundaries
        self.labels:[float] = []
        self.sound_properties = sound_properties
    def add_boundary(self, time):
        pass
    def remove_boundary(self, time):
        # also clean up self.labels
        pass
    def label_boundary(self, time):
        pass
    def label_all_boundaries(self):
        pass
    def to_intervals(self):
        pass
    def export(self):
        pass
