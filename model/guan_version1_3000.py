from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer = nn.layers.InputLayer(shape, input_var)                          # 3000
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=5))  # 2996
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 1498
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=5)) # 1494
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 747
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 744
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 372
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=5)) # 368
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 184
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=5)) # 180
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 90
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=5)) # 86
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 43
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=4)) # 40
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 20
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=5)) # 16
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

