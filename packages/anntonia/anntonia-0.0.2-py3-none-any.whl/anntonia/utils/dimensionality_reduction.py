import numpy as np
import scipy as sp
import sklearn.manifold as mf


def GetDistanceFunction(usealg=0):
    '''Calculate the distance between 2 neurons: 0  =  Pearsons correlation, 1  =  Euclidian distance, 2  =  Spearman, 3  =  distance_func = None.'''
    if (usealg == 0):
        # values from -1 to 1, 0 is no correlation, <0 negative correlation, >0 pos correlation
        def pearson(x, y):
            (_dist, _) = sp.stats.pearsonr(x, y)
            return _dist

        distance_func = pearson
    elif (usealg == 1):
        def euclidian(x, y):
            _dist = np.linalg.norm(x - y)
            return _dist

        distance_func = euclidian
    elif (usealg == 2):
        def spearmanr(x, y):
            (_dist, _) = sp.stats.spearmanr(x, y)
            return _dist

        distance_func = spearmanr
    else:
        def pearson(x, y):
            (_dist, _) = sp.stats.pearsonr(x, y)
            return _dist

        distance_func = pearson
    return distance_func


def GetDissimilarityMatrix(_activs, distancealg=0):
    '''Calculate the Dissimilarity Matrix using one of the above distance fucntions.'''
    neuron_amt = len(_activs)
    _dissimilarity_matrix = np.zeros((neuron_amt, neuron_amt))
    distance_function = GetDistanceFunction(distancealg)
    for i in range(neuron_amt):
        if not np.any(_activs[i]):  # or use np.all(_activs[i]==0)
            continue
        for j in range(i, neuron_amt):
            if not np.any(_activs[j]):  # or use np.all(_activs[i]==0)
                continue
            distance = distance_function(_activs[i], _activs[j])
            if distance != distance:
                print(i, j)
            assert (distance == distance)  # all weights zero
            # if(math.isnan(distance)): distance = 0
            _dissimilarity_matrix[i][j] = 1 - abs(distance)  # upper half   ## Note: has to be symmetric on the diagonal
            _dissimilarity_matrix[j][i] = 1 - abs(distance)  # lower half
    return _dissimilarity_matrix


def GetDimensionReduction(_dissimilarity_matrix, usealg=0):
    '''Reduce dimensions of the dissimilarity matrix to 2 dimensions: 0  =  MDS, 1  =  t-SNE.'''
    if (usealg == 0):
        _model = mf.MDS(n_components=2, dissimilarity='precomputed')
    elif (usealg == 1):
        _model = mf.TSNE()
    else:
        _model = mf.MDS(n_components=2, dissimilarity='precomputed')
    return _model.fit_transform(_dissimilarity_matrix)