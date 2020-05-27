import parselmouth
import numpy as np
import bisect
from parameters import FRACTION_VOICED_THRESHOLD
class SoundProperties():
    """
    stores time, pitch, intensity and voiced-or-not at each frame. object to be queried for values at a frame or over an interval"""

    def __init__(self, filename, voiced_only = False):
        # also store original sound object? maybe start by initializing this?
        self.sound = parselmouth.Sound(filename)
        self.end_time = self.sound.get_end_time()
        # smooth if necessary
        self.pitch = self.sound.to_pitch()
        self.intensity:parselmouth.Intensity = self.sound.to_intensity()
        self.make_frame_arrays()


    def make_frame_arrays(self, voiced_only=False):
        """Generate instance arrays containing pitch, loudness and voiced/unvoiced decision for each frame"""
        # time step being different for pitch and intensity messes this up, so use intensity time step
        time_step = self.intensity.get_time_step()
        self.times = np.arange(0, self.end_time, time_step)
        self.pitch_values:[float] = [
            self.pitch.get_value_at_time(time) for time in self.times
        ]
        self.intensity_values:[float] = [
            self.intensity.get_value(time) for time in self.times
        ]
        self.voiced_values:[float] = [not np.isnan(pitch) for pitch in self.pitch_values]

    def slice_range(self, start_time, end_time):
        return (
            bisect.bisect_left(self.times, start_time), 
            bisect.bisect_right(self.times, end_time))

    def is_voiced_at_time(self, time):
        return self.voiced_values[self.times.index(time)]

    def average_pitch(self, start_time, end_time):
        pass
    def average_intensity(self, start_time, end_time):
        pass

    def fraction_voiced(self, start_time, end_time):
        start, end = self.slice_range(start_time, end_time)
        all_frames = self.pitch_values[start:end]
        voiced_frames = [f for f in all_frames if not np.isnan(f)]
        return len(voiced_frames)/len(all_frames)

    def segment_is_voiced(self, start_time, end_time):
        return self.fraction_voiced(start_time, end_time) >= FRACTION_VOICED_THRESHOLD
    def to_dict(self):
        frame_dict = {}
        for (time, pitch, intensity, voiced) in zip(self.times, self.pitch_values, self.intensity_values, self.voiced_values):
            frame_dict[time] = {
                "intensity":intensity,
                "pitch":pitch,
                "is_voiced":voiced
            }
        return frame_dict


