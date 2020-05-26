# functions for drawing/graphing to test out parselmouth
import parselmouth
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
