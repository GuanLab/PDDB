from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import *


#def sorenson_dice(pred, tgt, ss=10):


N_HIDDEN=512
GRAD_CLIP=100

def network(input_var, label_var, shape):
    layer = nn.layers.InputLayer(shape, input_var,nsteps=3)                          # 4000

    #l_forward_1 = nn.layers.LSTMLayer(layer, N_HIDDEN, grad_clipping=GRAD_CLIP,nonlinearity=nn.nonlinearities.tanh)
    #l_forward_2 = nn.layers.LSTMLayer(l_forward_1, N_HIDDEN, grad_clipping=GRAD_CLIP,nonlinearity=nn.nonlinearities.tanh,only_return_final=True)
    #l_in_to_hid = nn.layers.Conv1DLayer(nn.layers.InputLayer((None,3,4000)),8, 3, pad='same')
    #print(nn.layers.get_output_shape(l_in_to_hid))
    #l_hid_to_hid = nn.layers.Conv1DLayer(nn.layers.InputLayer(l_in_to_hid.output_shape),8, 3, pad='same')
    #print(nn.layers.get_output_shape(l_hid_to_hid))

    #l_rec = nn.layers.CustomRecurrentLayer(layer, l_in_to_hid, l_hid_to_hid,only_return_final=True)
   # print(nn.layers.get_output(l_hid_to_hid))

    #print(nn.layers.get_output_shape(l_rec))
    
  #  print(nn.layers.get_output(l_rec))
    

    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=5))  # 3996
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 1998
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=5)) # 1994
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 997
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 994
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 497
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 494
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 247
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 244
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 122
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 118
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 59
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=4)) # 56
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 28
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=5)) # 24
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 12
    layer= nn.layers.LSTMLayer(incoming=layer, num_units=512,only_return_final=True)

    print(nn.layers.get_output_shape(layer))
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    print(nn.layers.get_output_shape(layer))
    print(nn.layers.get_output(layer))

    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)

    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

