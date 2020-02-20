from theano import tensor as T
import lasagne as nn
import tensorflow as tf
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer_input = nn.layers.InputLayer(shape, input_var)                          # 4000
    layer_con1 = bn(nn.layers.Conv1DLayer(layer_input, num_filters=8, filter_size=5))  # 3996
    #output_1 = nn.layers.get_output(layer_con1, deterministic=True).flatten()
    #g1 = tf.gradients(output_1, input_var, grad_ys = None)
    layer_max1 = nn.layers.MaxPool1DLayer(layer_con1, pool_size=2)                    # 1998
    layer_con2 = bn(nn.layers.Conv1DLayer(layer_max1, num_filters=16, filter_size=5)) # 1994
    #output_2 = nn.layers.get_output(layer_con2, deterministic=True).flatten()
    #g2 = tf.gradients(output_2, output1, grad_ys = None)
    layer_max2 = nn.layers.MaxPool1DLayer(layer_con2, pool_size=2)                    # 997
    layer_con3 = bn(nn.layers.Conv1DLayer(layer_max2, num_filters=32, filter_size=4)) # 994
    layer_max3 = nn.layers.MaxPool1DLayer(layer_con3, pool_size=2)                    # 497
    layer_con4 = bn(nn.layers.Conv1DLayer(layer_max3, num_filters=32, filter_size=4)) # 494
    layer_max4 = nn.layers.MaxPool1DLayer(layer_con4, pool_size=2)                    # 247
    layer_con5 = bn(nn.layers.Conv1DLayer(layer_max4, num_filters=64, filter_size=4)) # 244
    layer_max5 = nn.layers.MaxPool1DLayer(layer_con5, pool_size=2)                    # 122
    layer_con6 = bn(nn.layers.Conv1DLayer(layer_max5, num_filters=64, filter_size=4)) # 118
    layer_max6 = nn.layers.MaxPool1DLayer(layer_con6, pool_size=2)                    # 59
    layer_con7 = bn(nn.layers.Conv1DLayer(layer_max6, num_filters=128, filter_size=4)) # 56
    layer_max7 = nn.layers.MaxPool1DLayer(layer_con7, pool_size=2)                    # 28
    layer_con8 = bn(nn.layers.Conv1DLayer(layer_max7, num_filters=128, filter_size=5)) # 24
    layer_max8 = nn.layers.MaxPool1DLayer(layer_con8, pool_size=2)                    # 12
    layer_dense = DenseLayer(layer_max8, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    #output = nn.layers.get_output(layer_dense).flatten().clip(0.00001,0.99999)
    #output_det = nn.layers.get_output(layer_dense, deterministic=True).flatten().clip(0.00001,0.99999)
    #loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    #te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    #te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer_dense#, output1, output2, g1, g2

