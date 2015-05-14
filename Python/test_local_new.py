
"""
read real HRM samples from a csv and use a wavelet transform with overlapping windows
to extract heart rate data
"""

# import numpy as np
from numpy import *
from math import pi
from random import sample, random
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot, xlim, ylim
from scipy import fft, arange
import csv
import sys

def mainLoop(sampleList):
	lastWindow = -1
	windowDiff = 64
	# windowLength = 20
	windowLength = 256
	windowCount = 0
	index = 0
	for sample in sampleList:
		time = sample[0]
		# if we're at the start of a window make an array to be processed
		# if lastWindow == -1 or time-lastWindow > windowDiff:
		if lastWindow == -1 or index-lastWindow > windowDiff:
			windowCount += 1
			# lastWindow = time
			lastWindow = index
			windowList = list()
			for sample in sampleList:
				# if sample[0] >= time and sample[0] < lastWindow + windowLength:
				if sample[0] >= time and len(windowList) < windowLength:
					windowList.append(sample)
			# if windowList[len(windowList)-1][0] - windowList[0][0] < windowLength - 1:
			if len(windowList) < windowLength:
				return
			windowTransform(windowList)
			# return
			# print 'in window ' + str(lastWindow) + ' to ' + str(windowList[len(windowList)-1][0]) + ', heart rate: ' + str(60*windowTransform(windowList))
		index += 1

def windowTransform(windowList):
	n = len(windowList)			# samples
	samp_rate = 64 # getRate(windowList)	# Hz
	# print "rate: " + str(samp_rate)
	levels = 7
	wave = getWave(windowList)

	# Can't detect frequencies that could not oscillate >= 2 times in the window
	# low_cutoff = 1 / ((len(windowList)/samp_rate)/2)
	low_cutoff = 0
	high_cutoff = 8
	# print "low cutoff: " + str(low_cutoff)

	# cA, cD = dwt(wave, 'db2')
	coeffs = my_wavedec(wave, level=levels)

	i = 0
	# print len(coeffs)
	nyquist = samp_rate / 2.

	freqs = zeros(levels+1)
	freq_bounds = zeros(levels+1)
	freq_widths = zeros(levels+1)
	powers = zeros(levels+1)
	freq_range = nyquist - low_cutoff

	for a in coeffs:
		if (i <> 0):
			lower_limit = nyquist / 2.**(levels-i+1)
			upper_limit = nyquist / 2.**(levels-i)
			# print i, len(a), mean(abs(a)), std(a), lower_limit, upper_limit
			# I don't know why the 2 to 1 ratio works better...
			# freqs[i-1] = (2 * lower_limit + upper_limit) / 3.
			freqs[i] = (lower_limit + upper_limit) / 2.
			# print "freq: " + str(freqs[i]) 
			# if(i == 1):
			# 	freq_bounds[i-1] = lower_limit
			# freq_bounds[i] = upper_limit
			# freqs[i-1] = (lower_limit + 2 * upper_limit) / 3.

			# weight the frequencies by the widths of their bins
			# this could be a problem since the largest bin is 512 times the smallest
			# and later on the sum will always be skewed that way
			# freq_widths[i-1] = (upper_limit - lower_limit) / nyquist
			freq_widths[i-1] = freqs[i] - freqs[i-1]
			if (freqs[i] < high_cutoff and freqs[i] > low_cutoff):
				powers[i] = mean(abs(a))
			else:
				powers[i] = 0
			# print "power " + str(powers[i])
			 # powers[i-1] = mean(abs(a)) if (freqs[i-1] <= 8.0 and freqs[i=1] >= .5) else 0	# ignore frequencies higher than 4 Hz
		else:
			freqs[i] = 0
			powers[i] = 0
		i += 1

	core_freq = 0.
	numerator = 0.
	denominator = 0.

	# print str(freqs)

	for i in arange(levels):
		if (i <> 0 and (powers[i] + powers[i-1]) <> 0):
			Area = (freq_widths[i]/2)*(powers[i] + powers[i-1])
			## original method
			# numerator += ((freq_widths[i]**2)/6)*(2*powers[i] + powers[i-1]) * freq_widths[i]
			# denominator += (freq_widths[i]/2)*(powers[i] + powers[i-1]) * freq_widths[i]
			
			## weighted centroid
			# numerator += (1/freq_widths[i])*Area*(freq_widths[i]/2 + (freq_widths[i]/6)*((powers[i]-powers[i-1])/(powers[i]+powers[i-1])) + freqs[i-1])
			# denominator += (1/freq_widths[i])*Area

			##actual centroid
			numerator += ((freqs[i]**3 - freqs[i-1]**3)/3)*((powers[i] - powers[i-1])/freq_widths[i-1]) + ((freqs[i]**2 - freqs[i-1]**2)/2)*(powers[i-1]-freqs[i-1]*((powers[i] - powers[i-1])/freq_widths[i-1]))
			denominator += Area

			# numerator += powers[i-1]*(freqs[1]**2 - freqs[i-1]**2)/2 + (powers[i]-powers[i-1])*(freqs[i]**3 - freqs[i]**3)/(3*freq_widths[i])
			
			# numerator += (powers[i]/2)*(freq_bounds[i+1]**2-freq_bounds[i]**2)
			# denominator += (powers[i])*(freq_bounds[i+1]-freq_bounds[i])
			print "N: " + str(numerator)
			print "D: " + str(freq_widths[i]/2) + " * " + str(powers[i] + powers[i-1])
			print "D: " + str(denominator)
			# print "width: " + str(freq_widths[i])
			# print "N: " + str(numerator) + "   (h: " + str(freq_widths[i-1]) + ", b1: " + str(powers[i-1]) + ", b2: " + str(powers[i]) + ", h1: " + str(freqs[i-1]) + ", h2: " + str(freqs[i]) + "\nD: " + str(denominator)
			# print "unique centroid: " + str((((freqs[i]**3 - freqs[i-1]**3)/3)*((powers[i] - powers[i-1])/freq_widths[i]) + ((freqs[i]**2 - freqs[i-1]**2)/2)*(powers[i-1]-freqs[i-1]*((powers[i] - powers[i-1])/freq_widths[i])))/Area)
	core_freq = numerator/denominator


	print 'in window ' + str(windowList[0][0]) + ' to ' + str(windowList[len(windowList)-1][0]) + ', heart rate: ' + str(60*core_freq)
	plt.plot(freqs,powers)
	plt.xlim(0, 6)
	plt.grid()
	plt.show()
	return core_freq	

def getRate(windowList):
	numSamples = len(windowList)
	timeElapsed = windowList[numSamples-1][0]-windowList[0][0]
	rate = numSamples/timeElapsed
	return rate

def getWave(windowList):
	wave = list()
	for sample in windowList:
		wave.append(sample[1])
	return wave

def getTime(windowList):
	time = list()
	for sample in windowList:
		time.append(sample[0])
	return time

def getFactor(n, i):
	# factor = (n+1)/2 + abs((n-1)/2 - i)
	factor = 1 + abs((n-1)/2 - i)
	scale = 1
	return 1/float(scale*factor)

def freqSkew(n, i):
	scale = .25
	if(i < (n-1)/2):
		factor = 1 + scale*abs((n-1)/2 - i)
	else:
		factor = 1 - scale*abs((n-1)/2 - i)
	return factor

def plotFFTSpectrum(y,Fs):
	"""
	Plots a Single-Sided Amplitude Spectrum of y(t)
	"""
	n = len(y) # length of the signal
	k = arange(n)
	T = n/Fs
	frq = k/T # two sides frequency range
	frq = frq[range(n/2)] # one side frequency range

	Y = fft(y)/n # fft computing and normalization
	Y = Y[range(n/2)]

	plot(frq,abs(Y),'r') # plotting the spectrum
	xlim(0, 4)
	# set_xticks(arange(0, 5, .25))
	xlabel('Freq (Hz)')
	ylabel('|Y(freq)|')


def readFile():
	sampleList = list()
	with open('samples_finger_02.csv','rU') as samplesFile:
		reader = csv.reader(samplesFile, dialect=csv.excel_tab)
		for row in reader:
			valuePair = row[0].split(",", 1)
			sampleList.append(map(float, valuePair))
	return sampleList

def waveGen():
	n = 4096			# samples
	freq0 = 0 	# Hz
	samp_rate = 64	# Hz
	levels = 8

	start_freq = 1	# Hz
	end_freq = 2	# Hz
	if (start_freq != end_freq):
		freq0 = arange(start_freq, end_freq, (end_freq - start_freq) / (n * 1.0))
	else:
		freq0 = start_freq


	factor0 = samp_rate / freq0
	time = arange(n)/float(samp_rate)
	wave0 = sin(2 * pi * freq0 * time)

	# errors = [random() - 0.5 for _ in range(n)]
	# wave0 += errors

	sampleList = list()
	for t in arange(len(time)):
		sample = [time[t], wave0[t]]
		sampleList.append(sample)

	return sampleList

def printTransformArray(sampleList):
	i = 0
	transformArray = []
	sys.stdout.write("{")
	for sample in sampleList:
		if (i <> 256 and i <> 0):
			sys.stdout.write(", ")
		sys.stdout.write(str(sample[1]))
		transformArray.append(sample[1])
		i += 1 
		if (i == 256):
			sys.stdout.write("}; \n {")
		if(i == 326):
			sys.stdout.write("};")
			return transformArray


def my_wavedec(data, level=None):
	coeffs_list = []
	length = len(data) >> 1
	a = array(zeros(length), float) #list(zeros(length))
	d = array(zeros(length), float) #list(zeros(length))
	for j in xrange(level):
		a = array(zeros(length), float) #list(zeros(length))
		d = array(zeros(length), float) #list(zeros(length))
		for i in xrange(length):
			total = data[i*2] + data[i*2+1]
			diff = data[i*2] - data[i*2+1]
			a[i] = total
			d[i] = diff

		data = a
		coeffs_list.append(d)

		# print "length = " + str(length) + " a: " + str(a) + ", d: " + str(d)
		length = length >> 1
	coeffs_list.append(a)
	coeffs_list.reverse()
	return coeffs_list

def rawData():
	# sampleList = list();
	sampleList = [[0.01, 198], [0.03, 185], [0.05, 178], [0.06, 172], [0.08, 166], [0.09, 157], [0.11, 148], [0.12, 138], [0.14, 131], [0.15, 124], [0.17, 120], [0.19, 120], [0.20, 120], [0.22, 121], [0.23, 122], [0.25, 123], [0.26, 125], [0.28, 127], [0.29, 129], [0.31, 131], [0.33, 133], [0.34, 135], [0.36, 138], [0.37, 141], [0.39, 143], [0.40, 145], [0.42, 146], [0.44, 147], [0.45, 148], [0.47, 149], [0.48, 151], [0.50, 153], [0.51, 155], [0.53, 157], [0.55, 159], [0.56, 161], [0.58, 163], [0.59, 164], [0.61, 165], [0.62, 166], [0.64, 167], [0.65, 167], [0.67, 168], [0.69, 169], [0.70, 170], [0.72, 170], [0.73, 170], [0.75, 170], [0.76, 171], [0.78, 172], [0.80, 173], [0.81, 174], [0.83, 174], [0.84, 174], [0.86, 174], [0.87, 174], [0.89, 174], [0.90, 175], [0.92, 176], [0.94, 176], [0.95, 176], [0.97, 177], [0.98, 178], [1.00, 179], [1.01, 179], [1.03, 179], [1.04, 178], [1.06, 171], [1.08, 161], [1.09, 150], [1.11, 140], [1.12, 156], [1.14, 125], [1.15, 123], [1.17, 123], [1.19, 123], [1.20, 124], [1.22, 125], [1.23, 127], [1.25, 129], [1.26, 132], [1.28, 135], [1.29, 138], [1.31, 141], [1.33, 144], [1.34, 147], [1.36, 150], [1.37, 152], [1.39, 154], [1.40, 156], [1.42, 158], [1.44, 159], [1.45, 160], [1.47, 161], [1.48, 162], [1.50, 164], [1.51, 166], [1.53, 168], [1.54, 170], [1.56, 171], [1.58, 172], [1.59, 173], [1.61, 174], [1.62, 174], [1.64, 174], [1.65, 174], [1.67, 174], [1.69, 174], [1.70, 174], [1.72, 174], [1.73, 174], [1.75, 174], [1.76, 174], [1.78, 175], [1.79, 176], [1.81, 177], [1.83, 177], [1.84, 177], [1.86, 177], [1.87, 177], [1.89, 177], [1.90, 177], [1.92, 178], [1.94, 178], [1.95, 178], [1.97, 178], [1.98, 178], [2.00, 179], [2.01, 179], [2.03, 179], [2.04, 175], [2.06, 168], [2.08, 159], [2.09, 149], [2.11, 140], [2.12, 132], [2.14, 127], [2.15, 127], [2.17, 126], [2.19, 126], [2.20, 126], [2.22, 144], [2.23, 140], [2.25, 140], [2.26, 141], [2.28, 142], [2.29, 144], [2.31, 146], [2.33, 148], [2.34, 149], [2.36, 151], [2.37, 152], [2.39, 153], [2.40, 154], [2.42, 155], [2.44, 157], [2.45, 159], [2.47, 160], [2.48, 162], [2.50, 164], [2.51, 166], [2.53, 167], [2.54, 168], [2.56, 170], [2.58, 171], [2.59, 172], [2.61, 173], [2.62, 174], [2.64, 174], [2.65, 174], [2.67, 174], [2.69, 174], [2.70, 174], [2.72, 174], [2.73, 174], [2.75, 174], [2.76, 174], [2.78, 174], [2.79, 175], [2.81, 176], [2.83, 177], [2.84, 177], [2.86, 178], [2.87, 178], [2.89, 179], [2.90, 179], [2.92, 180], [2.94, 180], [2.95, 180], [2.97, 180], [2.98, 180], [3.00, 176], [3.01, 166], [3.03, 160], [3.04, 153], [3.06, 147], [3.08, 144], [3.09, 142], [3.11, 142], [3.12, 142], [3.14, 142], [3.15, 143], [3.17, 145], [3.19, 147], [3.20, 149], [3.22, 151], [3.23, 153], [3.25, 156], [3.26, 158], [3.28, 160], [3.29, 162], [3.31, 164], [3.33, 166], [3.34, 167], [3.36, 168], [3.37, 169], [3.39, 170], [3.40, 171], [3.42, 172], [3.44, 173], [3.45, 174], [3.47, 175], [3.48, 177], [3.50, 178], [3.51, 179], [3.53, 180], [3.54, 181], [3.56, 182], [3.58, 183], [3.59, 184], [3.61, 185], [3.62, 186], [3.64, 186], [3.65, 184], [3.67, 183], [3.69, 182], [3.70, 182], [3.72, 182], [3.73, 182], [3.75, 182], [3.76, 182], [3.78, 182], [3.79, 182], [3.81, 182], [3.83, 182], [3.84, 182], [3.86, 192], [3.87, 186], [3.89, 186], [3.90, 185], [3.92, 184], [3.94, 179], [3.95, 170], [3.97, 182], [3.98, 152], [4.00, 144], [4.01, 137], [4.03, 133], [4.04, 131], [4.06, 131], [4.07, 131], [4.09, 131], [4.11, 132], [4.12, 133], [4.14, 150], [4.15, 150], [4.17, 150], [4.19, 150], [4.20, 151], [4.22, 152], [4.23, 154], [4.25, 156], [4.26, 158], [4.28, 160], [4.29, 162], [4.31, 164], [4.32, 165], [4.34, 166], [4.36, 167], [4.37, 168], [4.39, 169], [4.40, 170], [4.42, 171], [4.43, 172], [4.45, 173], [4.47, 174], [4.48, 175], [4.50, 176], [4.51, 177], [4.53, 178], [4.54, 179], [4.56, 189], [4.57, 189], [4.59, 189], [4.61, 189], [4.62, 189], [4.64, 189], [4.65, 185], [4.67, 182], [4.68, 181], [4.70, 181], [4.72, 181], [4.73, 181], [4.75, 181], [4.76, 181], [4.78, 181], [4.79, 181], [4.81, 181], [4.82, 181], [4.84, 181], [4.86, 181], [4.87, 181], [4.89, 181], [4.90, 181], [4.92, 181], [4.93, 181], [4.95, 179], [4.97, 173], [4.98, 163], [5.00, 153], [5.01, 142], [5.03, 133], [5.04, 127], [5.06, 121], [5.07, 119], [5.09, 119], [5.11, 119], [5.12, 120], [5.14, 121], [5.15, 122], [5.17, 124], [5.18, 126], [5.20, 128], [5.22, 130], [5.23, 133], [5.25, 136], [5.26, 140], [5.28, 144], [5.29, 147], [5.31, 150], [5.32, 152], [5.34, 154], [5.36, 156], [5.37, 158], [5.39, 160], [5.40, 162], [5.42, 163], [5.43, 164], [5.45, 165], [5.47, 166], [5.48, 167], [5.50, 168], [5.51, 169], [5.53, 170], [5.54, 171], [5.56, 172], [5.57, 173], [5.59, 173], [5.61, 173], [5.62, 173], [5.64, 173], [5.65, 173], [5.67, 172], [5.68, 169], [5.70, 167], [5.71, 167], [5.73, 166], [5.75, 165], [5.76, 165], [5.78, 165], [5.79, 165], [5.81, 166], [5.82, 167], [5.84, 168], [5.86, 169], [5.87, 170], [5.89, 171], [5.90, 172], [5.92, 173], [5.93, 174], [5.95, 175], [5.96, 176], [5.98, 177], [6.00, 178], [6.01, 178], [6.03, 175], [6.04, 167], [6.06, 179], [6.07, 144], [6.09, 132]]
	while len(sampleList) > 256:
		sampleList.pop()
	return sampleList

if __name__ == '__main__':
	# sampleList = readFile()
	# sampleList = waveGen()
	sampleList = rawData();
	mainLoop(sampleList)
	# printTransformArray(sampleList)
	plt.plot(getTime(sampleList), getWave(sampleList))
	plt.show()
	# plt.plot(printTransformArray(sampleList))
	# plt.show()
