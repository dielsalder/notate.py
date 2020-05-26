import parselmouth
import numpy as np
from SoundProperties import SoundProperties
from TimeInterval import TimeInterval
from SegmentSet import SegmentSet


def note_segments(frames):
    """ takes a vector of sound properties and produces an array of timestamps (start, end) corresponding to note segments"""
    note_segments = []
    potential_min_or_max = None
    # either 'max' or 'min'
    note_start = 0
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
            note_segments.append(TimeInterval(note_start,time))
            note_start = time
            potential_min_or_max = frame["intensity"]
            search_mode="min" if search_mode=="max" else "max"
            current_segment_frames={}
    return note_segments

# segment notes by pitch --> step detection
# https://stackoverflow.com/questions/48000663/step-detection-in-one-dimensional-data

def export_labels(note_segments, filename="labels.txt"):
    """export note segment intervals as audacity labels
    audacity documentation: https://ttmanual.audacityteam.org/man/Label_Tracks"""
    with open(filename, 'w') as file:
        for i, segment in enumerate(note_segments):
            start, end, label = segment
            file.write(str(start)+'\t'+str(end)+'\t'+str(label)+"\n")
    file.close()

def get_notes(filename, export = False):
    props = SoundProperties(filename)
    frames = props.to_dict()
    segments = note_segments(frames)
    if export:
        export_labels(segments)
    return segments
