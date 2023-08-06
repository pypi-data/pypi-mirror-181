# ANNtoNIA_Keras
ANNtoNIA_Keras is an extension for the [ANNtoNIA](https://git-ce.rwth-aachen.de/vr-vis/VR-Group/anntonia) framework, which allows ANNtoNIA to extract the needed data from Keras models to visualize them.


## Using ANNtoNIA_Keras
Instantiate a KerasReader from to path to your Keras model, for example with:

```
model = KerasReader('path_to_your_model')
```

Then, you can use this reader for a visualizer, such as the LinearModelVisualizer from ANNtoNIA:
```
LinearModelVisualizer(model, test_data)
```