from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer = nn.layers.InputLayer(shape, input_var)                          # 4000
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=3))  # 3998
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 1999
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=4)) # 1996
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 998
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=3)) # 996
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 498
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=3)) # 496
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 248
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=3)) # 246
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 123
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 120
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 60
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=3)) # 58
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 29
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=4)) # 26
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 13
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

