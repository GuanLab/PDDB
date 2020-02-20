from theano import tensor as T
import lasagne as nn
from lasagne.layers import batch_norm as bn
from lasagne.layers import DenseLayer

#def sorenson_dice(pred, tgt, ss=10):

def network(input_var_outbound, input_var_rest,input_var_return, label_var, shape):
    ## outbound block

    layer_outbound = nn.layers.InputLayer(shape, input_var_outbound)                          # 4000
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=8, filter_size=5))  # 3996
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 1998
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=16, filter_size=5)) # 1994
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 997
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=32, filter_size=4)) # 994
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 497
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=32, filter_size=4)) # 494
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 247
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=64, filter_size=4)) # 244
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 122
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=64, filter_size=4)) # 118
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 59
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=128, filter_size=4)) # 56
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 28
    layer_outbound = bn(nn.layers.Conv1DLayer(layer_outbound, num_filters=128, filter_size=5)) # 24
    layer_outbound = nn.layers.MaxPool1DLayer(layer_outbound, pool_size=2)                    # 12


    ## rest block

    layer_rest= nn.layers.InputLayer(shape, input_var_rest)                          # 4000
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=8, filter_size=5))  # 3996
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 1998
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=16, filter_size=5)) # 1994
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 997
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=32, filter_size=4)) # 994
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 497
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=32, filter_size=4)) # 494
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 247
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=64, filter_size=4)) # 244
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 122
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=64, filter_size=4)) # 118
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 59
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=128, filter_size=4)) # 56
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 28
    layer_rest= bn(nn.layers.Conv1DLayer(layer_rest, num_filters=128, filter_size=5)) # 24
    layer_rest= nn.layers.MaxPool1DLayer(layer_rest, pool_size=2)                    # 12


    ## return block

    layer_return= nn.layers.InputLayer(shape, input_var_return)                          # 4000
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=8, filter_size=5))  # 3996
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 1998
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=16, filter_size=5)) # 1994
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 997
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=32, filter_size=4)) # 994
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 497
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=32, filter_size=4)) # 494
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 247
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=64, filter_size=4)) # 244
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 122
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=64, filter_size=4)) # 118
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 59
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=128, filter_size=4)) # 56
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 28
    layer_return= bn(nn.layers.Conv1DLayer(layer_return, num_filters=128, filter_size=5)) # 24
    layer_return= nn.layers.MaxPool1DLayer(layer_return, pool_size=2)                    # 12


    layer=nn.layers.ConcatLayer((layer_outbound,layer_rest,layer_return),axis=1)
    layer = DenseLayer(layer, num_units=1,nonlinearity=nn.nonlinearities.sigmoid) 
    output = nn.layers.get_output(layer).flatten().clip(0.00001,0.99999)
    output_det = nn.layers.get_output(layer, deterministic=True).flatten().clip(0.00001,0.99999)
    loss = nn.objectives.binary_crossentropy(output, label_var).mean() #, ss=ss)
    te_loss = nn.objectives.binary_crossentropy(output_det, label_var).mean() #,ss=ss)
    te_acc = nn.objectives.binary_accuracy(output_det, label_var).mean()

    return layer, loss, te_loss, te_acc

