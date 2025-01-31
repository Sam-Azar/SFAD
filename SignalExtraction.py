import wfdb
import matplotlib.pyplot as plt

# Define the correct file path (omit file extension)
file_path = r"C:\Users\samue\Desktop\112"

# Load the ECG record 
record, fields = wfdb.rdsamp(file_path)  

# Extract ECG signal from the first lead
ecg_signal = record[:, 0]  

# Get sampling rate
sampling_rate = fields['fs']  # Extract from metadata dictionary

# Plot the raw ECG signal
plt.figure(figsize=(10, 4))
plt.plot(ecg_signal[:2000])  # Plot first 2000 samples
plt.title("Raw ECG Signal (First 2000 Samples)")
plt.xlabel("Samples")
plt.ylabel("Amplitude (mV)")
plt.show()






