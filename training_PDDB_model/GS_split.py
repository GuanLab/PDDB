#!/usr/bin/env python

import random
import cv2
import numpy as np

def GS_split (FILE,size,seed):
    all_train_line=[]
    TRAIN_LIST=open(FILE,'r')
    for line in TRAIN_LIST:
        line=line.rstrip()
        all_train_line.append(line)
    random.seed(seed)
    random.shuffle(all_train_line)

    
    cut=int(len(all_train_line)/2)
    train_input_var=[]
    train_input_label=[]
    test_input_var=[]
    test_input_label=[]

    total_line=0
    for line in all_train_line:
        try:
            table=line.split('\t')
            the_file= table[1]
            label=float(table[0])
            data=np.load(the_file)
            data=data[:,1:]
            data_mean=np.mean(data,axis=0)
            data=(data-data_mean)/np.std(data,axis=0)

## get all 500 sequences;
            if (total_line<cut):
                sub_data=np.zeros([3,4000])
                a=len(data)
                if (a<=4000):
                    data=data.T

                    sub_data[:,0:a]=data
                else:
                    data=data.T
                    sub_data[:,:]=data[:,0:4000]
                train_input_var.append(sub_data)
                train_input_label.append(label)
    #            print(len(train_input_var))
                pass
            else:
                sub_data=np.zeros([3,4000])
                a=len(data)
                if (a<=4000):
                    data=data.T
                    sub_data[:,0:a]=data
                else:
                    data=data.T
                    sub_data[:,:]=data[:,0:4000]
                test_input_var.append(sub_data)
                test_input_label.append(label)

                pass
                #print(len(test_input_var))

        except:
            print(line)

        total_line=total_line+1

    print('done')
    train_input_var=np.asarray(train_input_var)
    test_input_var=np.asarray(test_input_var)
    print(train_input_var.shape)
    return (train_input_var, train_input_label, test_input_var, test_input_label)
