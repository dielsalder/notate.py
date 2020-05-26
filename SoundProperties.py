class SoundProperties():
    """
    stores time, pitch, intensity and voiced-or-not at each frame. object to be queried for values at a frame or over an interval"""

    def __init__(self, time, pitch, intensity, is_voiced):
        """"
        time, pitch, intensity: float array
        is_voiced: bool array
        """
        # also store original sound object? maybe start by initializing this?
        assert(
            len(time) == len(pitch) == len(intensity) == len(is_voiced), 
            "Input arrays to SoundProperties must have same length")
        self.time:[float] = time
        self.pitch:[float] = pitch
        self.intensity:[float] = intensity
        self.is_voiced:[bool] = is_voiced
    
    def pitch_at_time(self, time):
        pass

    def intensity_at_time(self, time):
        pass

    def is_voiced_at_time(self, time):
        pass

    def to_frame_interval(self, start_time, end_time):
        pass
    def average_pitch(self, start_time, end_time):
        pass
    def average_intensity(self, start_time, end_time):
        pass
    def voiced_fraction(self, start_time, end_time):
        pass
    def interval_is_voiced(self, start_time, end_time):
        pass
    def as_dict(self):
        pass

