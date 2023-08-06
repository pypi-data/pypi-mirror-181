import numpy as np

  
def SampleImage(x_train, y_train, random=True):
    '''Generates example image from the training data.'''
    if random:
        rand_image=np.random.choice(x_train.shape[0])
    else:
        rand_image = 0
    example_image = x_train[rand_image]  # grayscale
    example_image = example_image.reshape((1,28, 28))
    example_image_label = y_train[rand_image]
    return example_image, example_image_label


def CalculateNodeCoordinates(dimension_reduction, fig_size, layer_num, layer_size):
    '''Applies the dimension reduction to determine 2D-coordinates of the nodes of a specific layer.'''
    x_pos = 0
    # node_coordinates = []
    n = layer_num
    # for n in range(layer_count):
    node_coords = []
    sqrt_layer_size = int(np.sqrt(layer_size))
    range_array = range(sqrt_layer_size)
    for i in range_array:
        for j in range_array:
            if n == 0:
                node_coords.append(
                    [x_pos,
                     1 - 1 / fig_size / 2 - i * 1 / fig_size,
                     1 - 1 / fig_size / 2 - j * 1 / fig_size])
                continue
            node_coords.append(
                [x_pos,
                 -i / (sqrt_layer_size + 1),
                 -j / (sqrt_layer_size + 1)])

    # extra layer to fit in nodes that are potentially cut of due to rounding
    for x in range(layer_size - sqrt_layer_size * sqrt_layer_size):
        node_coords.append(
            [x_pos,
             -i / (sqrt_layer_size + 1),
             -j / (sqrt_layer_size + 1)])

    node_coords = np.array(node_coords)
    node_coords[:, 0] = x_pos
    # normalize coords of dimension reduction
    if n != 0:
        for ind, coord in enumerate(node_coords[::-1]):
            min_y = min(dimension_reduction[:, 0])
            max_y = max(dimension_reduction[:, 0])
            min_z = min(dimension_reduction[:, 1])
            max_z = max(dimension_reduction[:, 1])
            coord[1] = (dimension_reduction[ind][0] - min_y) / (max_y - min_y)
            coord[2] = (dimension_reduction[ind][1] - min_z) / (max_z - min_z)

    x_pos += 1
    return node_coords

