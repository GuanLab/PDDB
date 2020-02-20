#!/usr/bin/env python
import numpy as np 
import pandas as pd
import skimage.measure
import json, os

#read catalogue file
data = pd.read_csv('Walking_Activity_training.tsv',sep='\t', dtype = str)
accel_outbound_file = data.loc[:,'accel_walking_outbound.json.items']+'.tmp'
#outbound_file = data.loc[:,'deviceMotion_walking_outbound.json.items']+'.tmp'
accel_rest_file = data.loc[:,'accel_walking_rest.json.items']+'.tmp'
#rest_file = data.loc[:,'deviceMotion_walking_rest.json.items']+'.tmp'
#task1: import datapoints and timestamps

os.mkdir('./outbound')
os.mkdir('./rest')
os.mkdir('./return')

for filepath in accel_outbound_file:
	try:
		outbound_file = open('Data/'+str(filepath),'r')
		outbound = json.load(outbound_file)
		accel = [[outbound[i]['userAcceleration']['x'],outbound[i]['userAcceleration']['y'],outbound[i]['userAcceleration']['z']] for i in range(0,len(outbound),2)]  #downsampling 100Hz to 50hz
		accel = np.array(accel)
		np.save('outbound/'+filepath.split('.')[0],accel)
		outbound_file.close()
	except:
		print(filepath)
	#accel = [[outbound[i]['userAcceleration']['x'],outbound[i]['userAcceleration']['y'],outbound[i]['userAcceleration']['z']] for i in range(0,len(outbound),2)]   #downsampling 100Hz to 50hz
	#accel = np.array(accel)
	#gyros = [[outbound[i]['rotationRate']['x'],outbound[i]['rotationRate']['y'],outbound[i]['rotationRate']['z']] for i in range(0,len(outbound),2)]
	#gyros = np.array(gyros)
			
for filepath in accel_rest_file:
	try:
		rest_file = open('Data/'+str(filepath),'r')
		rest = json.load(rest_file)
		accel = [[rest[i]['userAcceleration']['x'],rest[i]['userAcceleration']['y'],rest[i]['userAcceleration']['z']] for i in range(0,len(rest),2)]  #downsampling 100Hz to 50hz
		accel = np.array(accel)
		np.save('rest/'+filepath.split('.')[0],accel)
		rest_file.close()
	except:
                print(filepath)
	#accel = [[rest[i]['userAcceleration']['x'],rest[i]['userAcceleration']['y'],rest[i]['userAcceleration']['z']] for i in range(0,len(rest),2)]   #downsampling 100Hz to 50hz
    #accel = np.array(accel)
	#gyros = [[rest[i]['rotationRate']['x'],rest[i]['rotationRate']['y'],rest[i]['rotationRate']['z']] for i in range(0,len(rest),2)]
	#gyros = np.array(gyros)
			    




