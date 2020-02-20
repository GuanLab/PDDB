#!/usr/bin/env python
import os
import sys
import logging
import numpy as np
import cv2
import time
import theano
from theano import tensor as T
import lasagne

eva=open('eva.txt','w')


size=int(sys.argv[2])
if __name__ == '__main__':
    model = sys.argv[3]
    params = 'params'

    import pkgutil
    loader = pkgutil.get_importer('../model')
    # load network from file in 'models' dir
    model = loader.find_module(model).load_module(model)

    input_var = T.tensor3('input')
    label_var= T.ivector('label')
    shape=(1,3,size)
    
    net, _, _,_ = model.network(input_var, label_var, shape)

    # load saved parameters from "params"
    with open('params', 'rb') as f:
        import pickle
        params = pickle.load(f)
        lasagne.layers.set_all_param_values(net, params)
        pass

    output_var = lasagne.layers.get_output(net, deterministic=True)
    pred = theano.function([input_var], output_var)
    
    
    TEST=open(sys.argv[1],'r')
    for line in TEST:
        line=line.strip()
        table=line.split('\t')
        #image = cv2.imread(table[0], cv2.IMREAD_GRAYSCALE)
        eva.write('%s' % table[0])

## get all 500 sequences;
        try:
            data=np.load(table[1])
            data=data[:,1:]
            data_mean=np.mean(data,axis=0)
            data=(data-data_mean)/np.std(data,axis=0)
            sub_data=np.zeros([3,4000])
            a=len(data)
            if (a<=4000):
                data=data.T
                sub_data[:,0:a]=data
            else:
                data=data.T
                sub_data[:,:]=data[:,0:4000]
            input_pred=[]
            input_pred.append(sub_data)
            input_pred=np.asarray(input_pred,dtype='float32')
            output = pred(input_pred)
            eva.write('\t%.4f' % output)
        except:
            print(line)
            pass


        eva.write('\n')

        pass
        


