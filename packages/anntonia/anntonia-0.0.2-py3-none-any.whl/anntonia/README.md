# Artificial Neural Network to Node-link Immersive Analytics (ANNtoNIA)

ANNtoNIA is a framework for building immersive node-link visualizations, designed for Artificial Neural Networks (ANN). It is currently under development and unfinished. For any questions, contact @mbellgardt.

## Recommended Setup

Download and install [Anaconda](https://www.anaconda.com), then create an environment, by executing:

```
conda create -c conda-forge --name anntonia --file anntonia-env.txt
```

in the anaconda prompt. Activate the environment using:

```
conda activate anntonia
```

Afterwards you can run one of the examples by, e.g:

```
python linear_model_test_server.py
```

This will start the ANNtoNIA server, you can then connect to with the [ANNtoNIA rendering client](https://devhub.vr.rwth-aachen.de/VR-Group/unreal-development/demos/anntonia_rendering).