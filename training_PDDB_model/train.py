#!/usr/bin/env python
import sys
import cv2
import numpy as np
import theano
from theano import tensor as T
from theano import shared 
import lasagne
import pkgutil
import pickle
import random
import math

## import DM specific modules
import GS_split as GS_split

## argv[1]=TRAIN_LIST, argv[1]: size




size=int(sys.argv[2]) #500


def norm_axis(a,b,c):
    newa=a/(math.sqrt(float(a*a+b*b+c*c)))
    newb=b/(math.sqrt(float(a*a+b*b+c*c)))
    newc=c/(math.sqrt(float(a*a+b*b+c*c)))
    return ([newa,newb,newc])

def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)], [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)], [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


def rotateC(image,theta,a,b,c): ## theta: angle, a, b, c, eular vector
    axis=norm_axis(a,b,c)
    imagenew=np.dot(rotation_matrix(axis,theta), image)
    return imagenew

def scaleImage(image,scale):
    [x,y]= image.shape
    y1=int(y*scale)
    x1=3
    image=cv2.resize(image,(y1,x1))
    new=np.zeros((x,y))
    if (y1>y):
        start=0
        end=start+y
        new=image[:,start:end]
    else:
        new_start=0
        new_end=new_start+y1
        new[:,new_start:new_end]=image
    return new
        


batch=16
max_scale=1.2
min_scale=0.8

def run_epoch(input_var,label_var,fn,if_train):
    input_var=np.array(input_var)

    count=int(input_var.shape[0]/batch)
    i=0
    err = 0 
    while (i<count):
        tmp_input=[] 
        tmp_label=[] 
        jjj=i*batch
        while (jjj<(i*batch+batch)):
                seq=input_var[jjj,:,:]
                #seq_img=seq.reshape(3,size);

                rrr=random.random()
                rrr_scale=rrr*(max_scale-min_scale)+min_scale
                if (if_train==1):
                    seq=scaleImage(seq,rrr_scale)
                    theta=random.random()*math.pi*2
                    a=random.random()
                    b=random.random()
                    c=random.random()
                    seq=rotateC(seq,theta,a,b,c)

                tmp_input.append(seq)
                label=label_var[jjj]
                tmp_label.append(label)
                jjj=jjj+1

        tmp_input_a=np.asarray(tmp_input)
        tmp_label_a=np.asarray(tmp_label)
        #print(tmp_input_a.shape)
        #print(tmp_label_a.shape)
        e = fn(tmp_input_a,tmp_label_a)
        err+=e
	#print(e/batch)
        i=i+1
    err=err/count;
    return err



## train the model
# model setup
def run_params(train_input_var, train_label_var, test_input_var, test_label_var,fold):
    record=open(fold,'w')
    input_var= T.tensor3('input')
    label_var= T.ivector('label')
    loader = pkgutil.get_importer('../model')
    model=sys.argv[3]
    model = loader.find_module(model).load_module(model)

    net, loss, te_loss, te_acc= model.network(input_var, label_var, [batch,3,size])

    params = lasagne.layers.get_all_params(net, trainable=True)
    lr = theano.shared(lasagne.utils.floatX(1e-4))

    updates = lasagne.updates.adam(loss, params, learning_rate=lr)

    best = None # (score, epoch, params)
    epoch=1
    max_epoch=101

    train_fn = theano.function([input_var, label_var], loss, updates=updates,allow_input_downcast=True)

    test_fn = theano.function([input_var, label_var], te_loss, allow_input_downcast=True)
    print("start training\n")
    train_loss_record = open("training_loss.txt", 'w')

    best_te_err=100

    while (epoch<=max_epoch):
        
## train_input_var is a name, so that sub-sequence can be selected there;
        tr_err = run_epoch(train_input_var,train_label_var, train_fn,1)
        te_err = run_epoch(test_input_var, test_label_var, test_fn,0)
        train_loss_record.write("%d\t%f\t%f\n"% (epoch,tr_err,te_err))
        print(tr_err,te_err)

        if (te_err<best_te_err):
            best =[np.copy(p) for p in (lasagne.layers.get_all_param_values(net))]
            best_te_err=te_err
            best_epoch=epoch

        if (epoch%25==0):
            te_err = run_epoch(test_input_var, test_label_var,test_fn,0)
            #param_vals = lasagne.layers.get_all_param_values(best[2])
            params_file=fold+'_params_'+str(epoch)
            
            with open(params_file, 'w') as wr:
                pickle.dump(best, wr)
            record.write('%d\t%d\t%.4f\t%.4f\n' % (epoch,best_epoch,tr_err,te_err))

        epoch=epoch+1
    train_loss_record.close()
    record.close()


(train_input_var, train_label_var, test_input_var, test_label_var)=GS_split.GS_split(sys.argv[1],4000,1)
run_params(train_input_var, train_label_var, test_input_var, test_label_var,'fold1')

(train_input_var, train_label_var, test_input_var, test_label_var)=GS_split.GS_split(sys.argv[1],4000,2)
run_params(train_input_var, train_label_var, test_input_var, test_label_var,'fold2')

(train_input_var, train_label_var, test_input_var, test_label_var)=GS_split.GS_split(sys.argv[1],4000,3)
run_params(train_input_var, train_label_var, test_input_var, test_label_var,'fold3')

(train_input_var, train_label_var, test_input_var, test_label_var)=GS_split.GS_split(sys.argv[1],4000,4)
run_params(train_input_var, train_label_var, test_input_var, test_label_var,'fold4')

(train_input_var, train_label_var, test_input_var, test_label_var)=GS_split.GS_split(sys.argv[1],4000,5)
run_params(train_input_var, train_label_var, test_input_var, test_label_var,'fold5')
