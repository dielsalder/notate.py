import parselmouth
class SoundProperties():
    """
    stores time, pitch, intensity and voiced-or-not at each frame. object to be queried for values at a frame or over an interval"""

    def __init__(self, filename):
        # also store original sound object? maybe start by initializing this?
        self.sound = parselmouth.Sound(filename)
        # smooth if necessary
        self.pitch = self.sound.to_pitch()
        self.intensity:parselmouth.Intensity

        #create framewise arrays and is_voiced
        self.times:[float]
        self.sound_values:[float]
        self.pitch_values:[float]
        self.voiced_values:[float]
    
    def pitch_at_time(self, time):
        pass

    def intensity_at_time(self, time):
        pass

    def is_voiced_at_time(self, time):
        pass

    def to_frame_interval(self, start_time, end_time):
        pass
    def interval_pitch(self, start_time, end_time):
        pass
    def interval_intensity(self, start_time, end_time):
        pass
    def interval_voiced_fraction(self, start_time, end_time):
        pass
    def interval_is_voiced(self, start_time, end_time):
        pass
    def as_dict(self):
        pass

