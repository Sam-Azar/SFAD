from scipy.signal import butter, filtfilt, iirnotch
from SignalExtraction import sampling_rate, ecg_signal
import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np

# High-Pass Filter (Removes Low-Freq Noise)
def hp_filter(fs, signal, cutoff, order=2):
    ny = 0.5 * fs
    normal_cutoff = cutoff / ny
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, signal)

# Notch Filter (Remove 50 Hz Powerline Noise)
def notch_filter(signal, notch_freq, fs, quality_factor=30):
    nyquist = 0.5 * fs
    freq = notch_freq / nyquist  # Normalize notch frequency
    b, a = iirnotch(freq, quality_factor)
    return filtfilt(b, a, signal)

# Low-Pass Filter (Remove High-Freq Noise)
def lowpass_filter(signal, cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, signal)

# Apply filters to the ECG signal
filtered_ecg = hp_filter(signal=ecg_signal, cutoff=0.5, fs=sampling_rate)
filtered_ecg = notch_filter(filtered_ecg, notch_freq=50, fs=sampling_rate)
filtered_ecg = lowpass_filter(filtered_ecg, cutoff=40, fs=sampling_rate)

# Feature Extraction using NeuroKit2
def extract_features(ecg_signal, sampling_rate):
    # Detect R-peaks in the ECG signal
    signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_rate)
    r_peaks = info['ECG_R_Peaks']  # Get R-peak locations

    # Calculate RR intervals (in seconds)
    rr_intervals = np.diff(r_peaks) / sampling_rate

    # Check for invalid RR intervals
    if len(rr_intervals) == 0 or np.any(np.isnan(rr_intervals)) or np.any(rr_intervals <= 0):
        raise ValueError("Invalid RR intervals detected. Check the ECG signal and R-peak detection.")

    # Calculate HRV features using R-peak locations (not RR intervals)
    hrv_features = nk.hrv_time(r_peaks, sampling_rate=sampling_rate)

    return rr_intervals, hrv_features, r_peaks  # Return RR intervals, HRV features, and R-peak locations

# Arrhythmia Detection (Rule-Based)
def detect_arrhythmia(rr_intervals, threshold_low=0.6, threshold_high=1.2):
    mean_rr = np.mean(rr_intervals)
    arrhythmia_detected = False
    
    for rr in rr_intervals:
        if rr < threshold_low * mean_rr or rr > threshold_high * mean_rr:
            arrhythmia_detected = True
            break
    
    return arrhythmia_detected

# Main processing
try:
    # Extract features from the filtered ECG signal
    rr_intervals, hrv_features, r_peaks = extract_features(filtered_ecg, sampling_rate)

    # Detect arrhythmia
    arrhythmia_detected = detect_arrhythmia(rr_intervals)

    # Print arrhythmia detection result
    if arrhythmia_detected:
        print("Arrhythmia detected!")
    else:
        print("No arrhythmia detected.")

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_ecg[:2000], label="Filtered ECG Signal", linewidth=2)

    # Mark arrhythmic beats
    arrhythmic_beats = np.where(np.abs(rr_intervals - np.mean(rr_intervals)) > 0.2 * np.mean(rr_intervals))[0]
    for beat in arrhythmic_beats:
        plt.axvline(x=r_peaks[beat], color='r', linestyle='--', alpha=0.5, label='Arrhythmic Beat' if beat == arrhythmic_beats[0] else "")

    plt.title("Filtered ECG Signal with Detected Arrhythmia")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude (mV)")
    plt.legend()
    plt.show()

except ValueError as e:
    print(f"Error: {e}")

plt.figure(figsize=(10, 4))
plt.plot(rr_intervals, label="RR Intervals")
plt.axhline(y=np.mean(rr_intervals), color='r', linestyle='--', label="Mean RR Interval")
plt.title("RR Intervals Over Time")
plt.xlabel("Beat Number")
plt.ylabel("RR Interval (s)")
plt.legend()
plt.show()
