import numpy as np

def IQToComplex(IVector,QVector):
    complexVector=[]
    for i in range(len(IVector)):
        complexVector.append(complex(IVector[i],QVector[i]))
    return complexVector

def ComplexToIQ(complexVector):
    I=[]
    Q=[]
    for i in range(len(complexVector)):
        I.append(complexVector[i].real)
        Q.append(complexVector[i].imag)
    return I,Q

def QPSK_generate(nsymbols,samples_in_symbol,bit_stream):
    samples_i = []
    samples_q = []
    q_sample = 0
    i_sample = 0
    #Starting bits modulating
    for k in range(int(nsymbols)):
        if (k%2 == 0): #If odd element, q bit must be changed
            if bit_stream[k]==0:
                q_sample = -1
            else:
                q_sample = bit_stream[k]
        else:
            if bit_stream[k]==0:
                i_sample = -1
            else:
                i_sample = bit_stream[k]
        for j in range(int(samples_in_symbol)):
            samples_i.append(i_sample)
            samples_q.append(q_sample)
    return samples_i,samples_q

def OQPSK_generate(nsymbols, samples_in_symbol, bit_stream):
    samples_i=[]
    samples_q=[]
    nsamples=nsymbols*samples_in_symbol
    #Generating samples based on bit_stream
    i_sample=0
    q_sample=0
    #Generating offset in Q(t) channel
    for k in range(int(samples_in_symbol/2)):
        samples_q.append(q_sample)
    #Starting bits modulating
    for k in range(int(len(bit_stream))):
        if (k%2 == 0): #If odd element, q bit must be changed
            if bit_stream[k]==0:
                q_sample = -1
            else:
                q_sample = bit_stream[k]
            for j in range(int(samples_in_symbol)):
                #Check for correct equal length
                if len(samples_q)<nsamples:
                    samples_q.append(q_sample)
        else:
            if bit_stream[k]==0:
                i_sample = -1
            else:
                i_sample = bit_stream[k]
            for j in range(int(samples_in_symbol)):
                samples_i.append(i_sample)
    return samples_i, samples_q

def smartFFT(samples, fSampling):
    freq = np.linspace(-fSampling/2,fSampling/2,len(samples))
    fftSamples = np.fft.fft(samples)
    fftSamples = np.fft.fftshift(fftSamples)
    return freq, fftSamples

def simpleFFT(samples, fSampling):
    freq = np.linspace(0,fSampling,len(samples))
    fftSamples = np.fft.fft(samples)
    return freq, fftSamples

def logFFT(fftSamples):
    return 20*np.log10(abs(fftSamples)/max(abs(fftSamples)))

def vectorRound(array, digit):
    for i in range(len(array)):
        array[i]=round(array[i],digit)
    return array

def combineIQ(samplesI,samplesQ):
    arr=[]
    for i in range(len(samplesI)):
        arr.append(samplesI[i]+samplesQ[i])
    return arr