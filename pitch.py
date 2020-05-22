import parselmouth
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# a segment will be considered a note if loudness is greater than this, and a rest otherwise
LOUDNESS_THRESHOLD = 70
# a segment will be considered a note if fraction_voiced is greater than this, and a rest otherwise
FRACTION_VOICED_THRESHOLD=0.5

class Segment():
    """
    start: float, start time
    end: float, end time
    frames: dict of frame properties"""
    start:float
    end:float
    frames:dict
    def __init__(self,start, end, frames):
        self.start = start
        self.end = end
        self.frames = frames
        self.n_frames = len(frames.items())
        # self.label = 'R' if self.average_intensity()<LOUDNESS_THRESHOLD else 'N'
        self.label = 'N' if self.fraction_voiced()<FRACTION_VOICED_THRESHOLD else 'R'

    def __iter__(self):
        return iter((self.start,self.end, self.label))

    def __repr__(self):
        return str((self.start,self.end, self.label))
    
    def __str__(self):
        return repr(self)
    
    def get_frames(self, start,end):
        return {time:props for time,props in self.frames.items() if start <= time < end}
    
    def average_intensity(self):
        return np.average([frame["intensity"] for frame in self.frames.values()])
    
    def voiced_frames(self):
        return {time:props for time,props in self.frames.items() if props["is_voiced"]}
    
    def fraction_voiced(self):
        return len(self.voiced_frames())/self.n_frames

    
def draw_pitch(pitch):
    # taken from parselmouth docs
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

def draw_intensity(intensity):
    intensity_values = []
    for frame in range(1,intensity.get_number_of_frames()+1):
        value = intensity.get_value(intensity.get_time_from_frame_number(frame))
        intensity_values.append(value)
    plt.plot(intensity.xs(),intensity_values)

def sound_properties(sound, voiced_frames_only = False, time_step = None):
    """Generate an array containing a vector of pitch, loudness and voiced/unvoiced decision for each frame"""
    frames = {}
    pitch = sound.to_pitch()
    intensity = sound.to_intensity()
    end_time = sound.get_end_time()
    if not time_step:
        time_step = intensity.get_time_step()

    for time in np.arange(0, end_time, time_step):
        pitch_value = pitch.get_value_at_time(time)
        intensity_value = intensity.get_value(time)
        is_voiced = not np.isnan(pitch_value)
        frames[time] = {
            "intensity": intensity_value,
            "pitch":pitch_value,
            "is_voiced":is_voiced
        }
    voiced_only = {time:props for time,props in frames.items() if props["is_voiced"]}
    # unvoiced_only = tuple(frame for frame in properties_arr if not frame["is_voiced"])
    # print(set(frame["intensity"] for frame in unvoiced_only))
    if voiced_frames_only:
        return voiced_only
    else:
        return frames


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
            note_segments.append(Segment(note_start,time, current_segment_frames.copy()))
            note_start = time
            potential_min_or_max = frame["intensity"]
            search_mode="min" if search_mode=="max" else "max"
            current_segment_frames={}
    return note_segments


def export_labels(note_segments, filename="labels.txt"):
    """export note segment intervals as audacity labels
    audacity documentation: https://ttmanual.audacityteam.org/man/Label_Tracks"""
    with open(filename, 'w') as file:
        for i, segment in enumerate(note_segments):
            start, end, label = segment
            file.write(str(start)+'\t'+str(end)+'\t'+str(label)+"\n")
    file.close()


# something to extract energy + produce vectors for each frame
sns.set()
snd = parselmouth.Sound("data/twinkle_no_legato.wav")
# already works quite well with separated notes! all the ones here are detected
# pitch = snd.to_pitch()
# plt.figure()
# draw_intensity(snd.to_intensity())
# plt.show()
# draw_pitch(pitch)
sound_properties = sound_properties(snd)
note_segments = note_segments(sound_properties)
print(note_segments)
export_labels(note_segments)