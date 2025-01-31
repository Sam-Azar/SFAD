# SFAD
SFAD (Signal Filtering and Arrhythmia Detection) contains Python code for processing ECG (electrocardiogram) signals and detecting arrhythmias. The code applies various filters to clean the ECG signal, extracts features such as R-peaks and RR intervals, and uses a rule-based approach to detect arrhythmias. 

Features
Signal Filtering: High-pass, notch, and low-pass filters are applied to remove noise from the ECG signal.

Feature Extraction: R-peaks and RR intervals are detected using the neurokit2 library.

Arrhythmia Detection: A rule-based algorithm detects arrhythmias based on deviations in RR intervals.

Visualization: The filtered ECG signal and RR intervals are plotted, with arrhythmic beats marked.

Usage
Prepare Your ECG Signal:

Place your ECG signal data in a file (e.g., SignalExtraction.py).

Ensure the file contains the ecg_signal and sampling_rate variables.

Run the Code:

Execute the ArrDetection.py script to process the ECG signal and detect arrhythmias.

View the Results:

The script will print whether arrhythmia is detected.

It will also generate two plots:

Filtered ECG Signal: Shows the filtered ECG signal with arrhythmic beats marked.

RR Intervals: Displays the RR intervals over time, with the mean RR interval highlighted.

Customization
Adjust Filters: Modify the cutoff frequencies in the hp_filter, notch_filter, and lowpass_filter functions to suit your data.

Change Arrhythmia Detection Thresholds: Adjust the threshold_low and threshold_high parameters in the detect_arrhythmia function.




