import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import random

# The dataset 'after' post-processing and cleaning
eeg_data = 'EEG_dataset_complete.csv'

loaded = False

def pad(single_signal):
	# Pad the signal if less than or greater than 260 length
	if len(single_signal) < 260:
		while len(single_signal) != 260:
			single_signal.append(np.mean(single_signal))
	elif len(single_signal) > 260:
		while len(single_signal) != 260:
			del single_signal[-1]
	return single_signal
	
def load_data():
	try:
		# Look for the cleaned dataset - if none, you'll be asked to load the original and clean it.
		dataset = pd.read_csv(eeg_data)
		loaded = True
	except:
		ans = input("[!] No dataset found! Would you like to load the original?\nyes/y or no/n: ")
		if ans == 'yes' or ans == 'y':
			dataset = pd.read_csv('EP1.01.txt', sep="\t", names=["id", "event", "device", "channel", "code", "size", "data"], error_bad_lines=False)
		else:
			exit(0)

	if not loaded:
		dataset["data"] = dataset["data"].str.replace(',', ' ')
		dataset.drop(columns=["event", "device", "channel", "size"], inplace=True)
		dataset.to_csv(eeg_data)
		
	return dataset

dataset = load_data()

# Shuffle the dataset
shuffle(dataset)
shuffle(dataset)

# Select a random row to use as a test case
rand = random.randint(1, 200)
single_signal = dataset.iloc[rand]["data"]
single_signal = [float(x) for x in single_signal.split()]

# Pad the signal (if necessary)
single_signal = pad(single_signal)

# Select the corresponding code (digit) for the selected signal
num = dataset.iloc[rand]["code"]

# Plot the data points as a scatter plot
plt.scatter(np.arange(0, 2, 0.0076923076923077), single_signal)
plt.xticks(np.arange(0, 2, step=0.2))
plt.yticks(np.arange(np.floor(np.min(single_signal) - 20.), np.floor(np.max(single_signal) + 20.), step=20))
plt.title("The number {}".format(num))
plt.show()

# Plot the entire EEG signal as a waveform
plt.plot(np.arange(0, 2, 0.0076923076923077), single_signal)
plt.xticks(np.arange(0, 2, step=0.2))
plt.yticks(np.arange(np.floor(np.min(single_signal) - 20.), np.floor(np.max(single_signal) + 20.), step=20))
plt.title("The number {}".format(num))
plt.show()

# Plot the data points and signal as waveform on each other
plt.plot(np.arange(0, 2, 0.0076923076923077), single_signal)
plt.scatter(np.arange(0, 2, 0.0076923076923077), single_signal)
plt.xticks(np.arange(0, 2, step=0.2))
plt.yticks(np.arange(np.floor(np.min(single_signal) - 20.), np.floor(np.max(single_signal) + 20.), step=20))
plt.title("The number {}".format(num))
plt.show()


#----  Comparison of multiple signals (preset to 20) for the same number ----#
max_range = 0
min_range = 10000
count = 0
for i in range(len(dataset)):
    if count == 20:
        break

    if dataset.iloc[i]["code"] == num:
        count += 1
        single_signal = [float(x) for x in dataset.iloc[i]["data"].split()]
        single_signal = pad(single_signal)
        if np.max(single_signal) > max_range:
            max_range = np.max(single_signal)
        if np.min(single_signal) < min_range:
            min_range = np.min(single_signal)

        plt.plot(np.arange(0, 2, 0.0076923076923077), single_signal)

plt.xticks(np.arange(0, 2, step=0.2))
plt.yticks(np.arange(np.floor(min_range - 20.), np.floor(max_range + 20.), step=20))
plt.title("The number {}".format(num))
plt.show()
#---------------------------------------------------------------------------#

