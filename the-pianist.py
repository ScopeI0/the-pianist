#] [0] Dependencies:
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import sounddevice as sd
#] [1] Frequency Table:
Octave3 = {'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
           'G3': 196, 'A3': 220, 'B3': 246.93}
Octave4 = {'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
           'G4': 392, 'A4': 440, 'B4': 493.88}
#] [2] Sound Track:
Song = [('C3', 'C4', 0.2), ('D3', 0, 0.15), ('E3', 'E4', 0.15),
        ('F3', 0, 0.15), ('G3', 'G4', 0.15), ('A3', 0, 0.15),
        ('B3', 'B4', 0.15), ('B3', 'B4', 0.15), (0, 'A4', 0.15),
        ('G3', 'G4', 0.15), (0, 'F4', 0.15), ('E3', 'E4', 0.15),
        (0, 'D4', 0.15), ('C3', 'C4', 0.2)]
#] [3] Initial Values:
Time = np.linspace(0, 3, 12 * 1024)
tOutput = np.zeros(Time.shape)
iTime = 0
Separation = 0.06
#] [4] Summation:
for Chord in Song:
    iOctave3 = Octave3.get(Chord[0], 0)
    iOctave4 = Octave4.get(Chord[1], 0)
    Duration = Chord[2]
    #] [5] Function:
    iOutput = np.sin(2 * np.pi * iOctave3 * Time) + np.sin(2 * np.pi * iOctave4 * Time)
    Step = np.reshape([(Time >= iTime) & (Time <= iTime + Duration)], Time.shape)
    tOutput += iOutput * Step
    iTime += Duration + Separation
#] [6] Frequency Conversion:
Sample = 3 * 1024
Frequency = np.linspace(0, 512, int(Sample / 2))
fOutput = 2 / Sample * np.abs(fft(tOutput)[:np.int_(Sample / 2)])
#] [7] Noise Generation:
rFrequency1, rFrequency2 = np.random.randint(0, 512, 2)
Noise = np.sin(2 * rFrequency1 * np.pi * Time) + np.sin(2 * rFrequency2 * np.pi * Time)
ntOutput = tOutput + Noise
nfOutput = 2 / Sample * np.abs(fft(ntOutput)[:np.int_(Sample / 2)])
#] [8] Noise Cancellation:
Peak = np.ceil(np.max(fOutput))
Indicies = np.where(nfOutput > Peak)[0]
nFrequency1, nFrequency2 = np.int_(Frequency[Indicies])
ftOutput = ntOutput - (np.sin(2 * nFrequency1 * np.pi * Time) +
                       np.sin(2 * nFrequency2 * np.pi * Time))
ffOutput = 2 / Sample * np.abs(fft(ftOutput)[:np.int_(Sample / 2)])
#] [6] Preview:
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(Time, tOutput)
plt.subplot(3, 1, 2)
plt.plot(Time, ntOutput)
plt.subplot(3, 1, 3)
plt.plot(Time, ftOutput)
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(Frequency, fOutput)
plt.subplot(3, 1, 2)
plt.plot(Frequency, nfOutput)
plt.subplot(3, 1, 3)
plt.plot(Frequency, ffOutput)
# sd.play(tOutput, 3 * 1024)
# sd.play(ntOutput, 3 * 1024)
sd.play(ftOutput, 3 * 1024)