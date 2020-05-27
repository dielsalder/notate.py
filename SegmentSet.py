from SoundProperties import SoundProperties
from TimeInterval import Interval
import bisect

class SegmentSet():
    # rep invariant: labels has one less item than boundaries
    def __init__(self, sound_properties):
        end_time = sound_properties.sound.get_end_time()
        # bisect for maintaining sorted list
        self.boundaries:[float] = [0.0,end_time]
        # label i in self.labels corresponds to the interval (i, i+1) in self.boundaries
        # if there is no label, use None as placeholder
        self.labels:[float] = [None]
        self.sound_properties = sound_properties

    def __check_rep(self):
        assert len(self.labels) == len(self.boundaries) - 1
    
    def __iter__(self):
        for i, label in enumerate(self.labels):
            yield self.get_interval(i)
    
    def get_interval(self, i):
        return Interval(self.boundaries[i], self.boundaries[i+1], self.labels[i])

    def find_index(self, time):
        '''
        Locate index of the leftmost value equal to time
        taken from bisect docs
        '''
        i = bisect.bisect_left(self.boundaries, time)
        return i

    def add_boundary(self, time):
        i = self.find_index(time)
        self.boundaries.insert(i, time)
        self.labels.insert(i, None)
        self.__check_rep()

    def remove_boundary(self, time):
        # also clean up self.labels -- how to do this?
        pass

    def label(self, label:str, time = None, i = None):
        if not i:
            i = self.find_index(time)
        self.labels[i] = label
        self.__check_rep()

    def label_segment_type(self, time = None, i = None):
        if not i:
            i = self.find_index(time)
        start = self.boundaries[i]
        end = self.boundaries[i+1]
        self.label('N' if self.sound_properties.segment_is_voiced(start, end) else 'R', i=i)
        self.__check_rep()

    def label_all(self):
        for idx, _label in enumerate(self.labels):
            self.label_segment_type(i=idx)

    def __repr__(self):
        r = "SegmentSet containing: \n"
        for interval in list(iter(self)):
            r += repr(interval)
            r += "\n"
        return r

    def export_labels(self, filename="labels.txt"):
        """export note segment intervals as audacity labels
        audacity documentation: https://ttmanual.audacityteam.org/man/Label_Tracks"""
        with open(filename, 'w') as file:
            for _i, segment in enumerate(self):
                start, end, label = segment
                file.write(str(start)+'\t'+str(end)+'\t'+str(label)+"\n")
        file.close()
