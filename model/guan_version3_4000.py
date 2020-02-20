from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer = nn.layers.InputLayer(shape, input_var)                          # 4000
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=7))  # 3994
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 1997
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=6)) # 1992
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 996
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=7)) # 990
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 495
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=6)) # 490
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 245
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=6)) # 240
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 120
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=7)) # 114
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 57
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=6)) # 52
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 26
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=7)) # 20
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 10
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

