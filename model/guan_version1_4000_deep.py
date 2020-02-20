from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var, label_var, shape):
    print(input_var.shape)
    layer = nn.layers.InputLayer(shape, input_var)                          # 4000
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=5))  # 3996
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=8, filter_size=5))  # 3992
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 1996
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=5)) # 1992
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=16, filter_size=5)) # 1988
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 994
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=5)) # 990
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=5)) # 986
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 493
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=5)) # 489
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=32, filter_size=4)) # 486
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 243
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=5)) # 239
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=4)) # 236
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 118
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=5)) # 114
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=64, filter_size=5)) # 110
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 55
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=5)) # 51
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=128, filter_size=4)) # 48
    layer = nn.layers.MaxPool1DLayer(layer, pool_size=2)                    # 24
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=256, filter_size=5)) # 20
    layer = bn(nn.layers.Conv1DLayer(layer, num_filters=256, filter_size=5)) # 16
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

