import numpy as np #importing Numpy with an alias np
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 
from scipy.signal import butter, lfilter

CHUNK = 1024 * 2
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pa.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 뚝 끊기는게 아니라 -50hz~+50hz 점차적으로 필터링됨

fs = RATE
cutoff = 200 # cut할 hz
order = 6


# Figure 그래프 만드는 코드
fig, ax1 = plt.subplots()
x_fft = np.linspace(0, RATE, CHUNK)
line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
ax1.set_xlim(20,RATE/20)
ax1.set_ylim(0,1)
fig.show()

# 그래프에 선 움직이는 코드
while 1:
    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    y = butter_lowpass_filter(dataInt, cutoff, fs, order)
    line_fft.set_ydata(np.abs(np.fft.fft(y))*2/(11000*CHUNK))
    fig.canvas.draw()
    fig.canvas.flush_events()
    list = np.abs(np.fft.fft(y))*2/(11000*CHUNK)
    vi = (list[1]*5 + list[2]*4 + list[3]*3 + list[4]*2 + list[5]*1)/5
    

    if(vi>0.5):
        print("진동 {0:.2}단계".format(vi))