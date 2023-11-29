# OSU_NARS_ModifiedSwitchMedianFilter
Code is used on noisy radiographs to appropriately identify and remove unique noise found in (fast) neutron radiography acquisitions.

ReadMe for Ohio State University Nuclear Analysis and Radiation Sensor (NARS) Codes for the Modified Switch Median Filter
*******************************************************************************************************
Original Author: Matthew Bisbee
Affiliations: Ohio State University Dept. of Mechanical and Aerospace Engineering, Nuclear Engineering
	      Nuclear Analysis and Radiation Sensor (NARS) Laboratory
	      DOE NEUP Fellowship FY19
	      Points of Contact: Advisor Dr. Raymond Cao - cao.152@osu.edu
			         Author Matthew Bisbee - bisbee.11@osu.edu
********************************************************************************************************

Python script: ModifiedSwitchMedianFilter.py
InputFile: ImageFilterInputHDPE1_11-29-21.txt
Example Image Stack: OSUPhantomHDPE1_11-29-21

********************************************************************************************************
General Information:

This code is written in Python3.X based language and was run on a Windows device. Small changes may need to be made for Mac/Linux machines in terms of navigating to files. The code was written as a new way to apply a switch median filter on radiographs that are collected with cameras in high radiation environments. Radiation induced noise is specifically a problem in CCD based cameras in fast neutron detection systems as the silicon chips are sensitive to neutrons and gamma-rays which can create large tracks of noise in the image not well handled by conventional filtering processes. This code uses the switch median filtering technique to identify and flag noise that is statistically significant in the image. This noise is handled based on the size of the cluster (1,2-6 or 7+ pixels) with varied filters. There is an option in the code to pull gray value information from neighboring radiographs if the image sequence included rotated projection angles with sufficiently small rotation angles. The filter only affects pixels discovered by the switch median filter and not lesser noisy pixels. Therefore, it is suggested to apply a small order median filter (W_1 or 3x3 is suggested) to remove Poisson noise. 

********************************************************************************************************
Input File:

The input file is built using % as comments (unfortunately for us at OSU we couldn't use # like typical Python comments as we had used # as a character in some images). As soon as the % is seen the line or rest of the line is skipped. Otherwise, it is important to look at the order in which the information is read into the script as I just have this as a line by line input file. The comments in the example script and comments in the Python script itself should be useful in interpretting how to build your own input file for your own data. In the case of this input file, I supplied data that had already calculated MedianDifference and FlagMap images but when using raw data, input None (or YesFlag) in those specific areas to have the code run each of those steps.

********************************************************************************************************
Further Information:
     
How the code actually works can be seen if you take a look at Chapter 6 of the dissertation "Advancing Radiographic Acquisition and Post-Processing Capabilities for a University Research Reactor Fast and Thermal Neutron Radiography and Tomography Instrument" as that goes into more detail on logic and decisions. Otherwise, the code is well commented, good luck!
