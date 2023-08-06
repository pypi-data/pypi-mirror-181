import keras
import numpy as np
import scipy as sp
from keras import backend as K
from sklearn.preprocessing import normalize
from anntonia.server.state import LayerType


class KerasReader():
    '''Specific reader class suited for Keras models.'''

    @classmethod
    def is_reader_for(cls, library):
        return library == 'Keras'

    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)
        self.path = model_path
        self.max_epoch = 0

    def GetWeights(self):
        '''Returns the normalized weights of each layer.'''
        weights = np.empty(len(self.model.weights), dtype=object)
        for layer, _ in enumerate(self.model.weights):
            weights[layer] = self.model.weights[layer]
        layer_weights = [weights[n * 2] for n in
                         range(int(len(weights)/2))]  # because every second array of weights contains the biases
        # normalize to (-1,1)
        layer_weights = [K.get_value(l) for l in layer_weights]
        end_shapes = [(np.prod(np.shape(l)[:int(len(np.shape(l))/2)]), np.prod(np.shape(l)[int(len(np.shape(l))/2):])) for l in layer_weights]
        layer_weights = [np.reshape(l, (np.prod(np.shape(l)[:-1]), np.shape(l)[-1]), order='F') for l in layer_weights]
        layer_weights = [normalize(l, axis=0, norm='l2') for l in layer_weights]
        layer_weights = [np.reshape(l, end_shapes[i], order = 'F') for i, l in enumerate(layer_weights)]
        return layer_weights

    def GetBias(self):
        '''Returns the normalized bias of each layer.'''
        weights = np.empty(len(self.model.weights), dtype=object)
        for layer, _ in enumerate(self.model.weights):
            weights[layer] = self.model.weights[layer]
        bias = [weights[n * 2 + 1] for n in
                range(int(len(weights)/2))]  # because every second array of weights contains the biases
        bias = [K.get_value(b) for b in bias]
        bias = [normalize(b.reshape(1, -1), axis=1, norm='l2') for b in bias]
        return bias

    def GetStride(self, layer_num):
        return self.model.layers[layer_num].get_config()["strides"]

    def GetPoolSize(self, layer_num):
        return self.model.layers[layer_num].get_config()["pool_size"]


    def GetLayerSizes(self):
        return [l.output_shape[1:] for l in self.model.layers]

    def GetWeightedLayerSizes(self):
        '''Returns a list of layer sizes of all layers that have weights'''
        layers = []
        for layer in self.model.layers:
            if len(layer.get_weights()) != 0:
                layers.append(layer.output_shape[1:])
        return layers

    def GetWeightSizes(self):
        '''Calculates the total number of weights in the layer connections.'''
        weight_sizes = []
        for ind, l in enumerate(self.model.layers):
            print(f"Layer size: {l.output_shape}")
            if ind < len(self.model.layers) - 1:
                weight_sizes.append(l.output_shape[1] * self.model.layers[ind + 1].output_shape[1])
        return weight_sizes

    def GetLayerType(self, layer_num):
        if isinstance(self.model.layers[layer_num], (keras.layers.Flatten)):
            return LayerType.SUPPORTING
        elif isinstance(self.model.layers[layer_num], (keras.layers.MaxPooling2D)):
            return LayerType.POOLING
        elif isinstance(self.model.layers[layer_num], (keras.layers.Conv2D)):
            return LayerType.CONVOLUTIONAL
        elif isinstance(self.model.layers[layer_num], (keras.layers.Dense)):
            return LayerType.FULLY_CONNECTED
        else:
            print("Layer type not recognized")
            return LayerType.FULLY_CONNECTED

    def GetActivationOutputAllLayers(self, input):
        '''Determine the node activations for a given input.'''
        activations = []
        for layer in self.model.layers:
            get_layer_output = K.function([self.model.layers[0].input],
                                          [layer.output])
            layer_output = get_layer_output([input])[0]
            activations.append(sp.transpose(layer_output).astype('float32'))
        return activations

    def GetActivationOutput(self, input, layer_num):
        '''Determine the node activations for a given input on a certain layer.'''
        layer = self.model.layers[layer_num]
        get_layer_output = K.function([self.model.layers[0].input],
                                      [layer.output])
        layer_output = get_layer_output([input])[0]
        activations = sp.transpose(layer_output).astype('float32')
        return activations

    def ApplyActivationFunction(self, input, layer_num):
        '''Apply the activation function of a layer to a given input.'''
        try:
            activation_function = self.model.layers[layer_num].activation
            if isinstance(activation_function, keras.activations.Softmax):
                return input
            return activation_function(input)
        except AttributeError:
            return input