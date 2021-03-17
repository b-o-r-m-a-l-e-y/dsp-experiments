filename = "/home/bormaley/my/dsp-experiments/data.bin"
import numpy as np
import matplotlib.pyplot as plt
import dspfunc as dsp

class MSKModulator:
    def __init__(self, filename, samples_per_symbol):
        self.fileName = filename
        self.samplesPerSymbol = samples_per_symbol
        self.time = 0.0
        self.prevPhase = 0
        self.prevBit = 0
        self.fd = open(filename, 'rb')
        self.cmplxSamples = []

    def process(self, nBytes = 0):
        if nBytes == 0:
            bytes = self.fd.read()
        else:
            bytes = self.fd.read(nBytes)
        generatedSamplesI = []
        generatedSamplesQ = []
        for byte in bytes:
            bits = map(lambda x: 1 if x>0 else -1, [(byte & 1 << i) for i in range(8)])
            for i, bit in enumerate(bits):
                for _ in range(self.samplesPerSymbol):
                    if i%2==0:
                        phase = self.prevPhase
                    elif bit != self.prevBit:
                        phase = self.prevPhase + np.pi
                    else:
                        phase = self.prevPhase
                    generatedSamplesI.append(np.cos(np.pi*self.time/2/self.samplesPerSymbol)*np.cos(phase))
                    generatedSamplesQ.append(-bit*np.cos(phase)*np.sin(np.pi*self.time/2/self.samplesPerSymbol))
                    self.prevPhase = phase
                    self.prevBit = bit
                    self.time += 1
        return generatedSamplesI, generatedSamplesQ

sps = 4
MSKMod = MSKModulator(filename, sps)
i,q = MSKMod.process(10)
cplx = dsp.IQToComplex(i, q)
bandSignal = []
time = 0.0
for sample in cplx:
    bandSignal.append(sample*np.exp(1j*100*time))
    time += 1
i,q = dsp.ComplexToIQ(bandSignal)
plt.plot(i)
plt.plot(q)
plt.show()