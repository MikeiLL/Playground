import numpy as np
import matplotlib.pyplot as plt
samples = np.arange(44000) # cd quality 44k
wav = np.sin(samples * 0.0314159)
plt.plot(wav[1:1000]) #1/44 of a second or 22ms
plt.show()
