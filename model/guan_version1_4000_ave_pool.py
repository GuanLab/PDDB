from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer = nn.layers.InputLayer(shape, input_var)                          # 4000
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=5))  # 3996
    layer = nn.layers.Pool1DLayer(layer, pool_size=2, mode='average_exc_pad')                    # 1998
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=5)) # 1994
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 997
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 994
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 497
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 494
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 247
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 244
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 122
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 118
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 59
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=4)) # 56
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 28
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=5)) # 24
    layer = nn.layers.Pool1DLayer(layer, pool_size=2,mode='average_exc_pad')                    # 12
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

