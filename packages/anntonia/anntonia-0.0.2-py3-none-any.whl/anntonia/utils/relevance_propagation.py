import numpy as np


# Layer-wise Relevance Propagation (LRP)
# Montavon et al. 2019
# see also http://heatmapping.org/tutorial/ for coding example


def LayerwiseRelevancePropagation(weights, biases, example_image_label, activation_output):
    '''Performs LRP on the given weights and activations to a specific input image.'''
    length = len(weights)
    activations = [None] * (length + 1)
    for l in range(length + 1):
        activations[l] = np.array(activation_output[l]).flatten()
    relevances = [None] * length + [activations[length] * (example_image_label == np.arange(10))]

    # gamma-rule of LRP: gamma factors in how much positive weights should be favored over negatives,
    # thus a small fraction is added to positive values
    def rho(layer_values, gamma=0.1):
        return layer_values + gamma * np.maximum(0, layer_values)

    # epsilon-rule: add small increment to denominantor, eps absorbs relevance of weak explanation factors
    def incr(z, eps=0.1):
        return z + eps * (z ** 2).mean() ** .5 + 1e-9

    for l in range(1, length)[::-1]:
        layer_weights = rho(weights[l], l)
        layer_biases = rho(biases[l], l)
        z = incr(activations[l].dot(layer_weights) + layer_biases, l)  # step 1
        s = relevances[l + 1] / z  # step 2
        c = s.dot(layer_weights.T)  # step 3
        relevances[l] = activations[l] * c  # step 4
    # different propagation rule for pixels of the input layer
    layer_weights = weights[0]
    weight_max = np.maximum(0, layer_weights)
    weight_min = np.minimum(0, layer_weights)
    lower_bound = activations[0] * 0 - 1
    upper_bound = activations[0] * 0 + 1
    z = activations[0].dot(layer_weights) - lower_bound.dot(weight_max) - upper_bound.dot(weight_min) + 1e-9  # step 1
    s = relevances[1] / z  # step 2
    c, c_max, c_min = s.dot(layer_weights.T), s.dot(weight_max.T), s.dot(weight_min.T)  # step 3
    relevances[0] = activations[0] * c - lower_bound * c_max - upper_bound * c_min  # step 4
    return relevances
