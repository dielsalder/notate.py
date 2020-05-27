import parselmouth
import numpy as np
from SoundProperties import SoundProperties
from TimeInterval import Interval
from SegmentSet import SegmentSet


def segment_by_loudness(sound_properties):
    """ takes a vector of sound properties and produces an array of timestamps (start, end) corresponding to note segments"""
    segments = SegmentSet(sound_properties)
    frames = sound_properties.to_dict()
    potential_min_or_max = None
    # either 'max' or 'min'
    search_mode = "max"
    current_segment_frames = {}
    for time,frame in frames.items():
        current_segment_frames[time]=frame
        # skip if voiceless
        if np.isnan(frame["intensity"]) or np.isnan(frame["pitch"]):
            continue
        if not potential_min_or_max:
            potential_min_or_max = 0

        if (search_mode == "max" and frame["intensity"] > potential_min_or_max
        or search_mode=="min" and frame["intensity"] < potential_min_or_max):
            # note_segments.append((note_start, time))
            segments.add_boundary(time)
            potential_min_or_max = frame["intensity"]
            search_mode="min" if search_mode=="max" else "max"
            current_segment_frames={}
    return segments

def label_notes_and_rests(segments):
    """mark note segments as N and rests as R"""
    def label_one(segments, i):
        pass
    pass
        
# segment notes by pitch --> step detection
# https://stackoverflow.com/questions/48000663/step-detection-in-one-dimensional-data


def get_notes(filename):
    """driver code to go through entire note getting process"""
    props = SoundProperties(filename)
    segments = segment_by_loudness(props)
    return segments
