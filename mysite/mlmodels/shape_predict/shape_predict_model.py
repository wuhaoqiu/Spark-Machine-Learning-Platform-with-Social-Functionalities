#author:Haoqiu Wu Time 19.4.12


def store_file(input_data):
    # overwite the file if it exists
    with open('mysite/media/shape_predict/uploaded/data.mat', 'wb+') as destination:
        for chunk in input_data.chunks():
            destination.write(chunk)

def predict():
    from scipy.io import loadmat
    import numpy as np
    import tensorflow as tf
    try:
        x = loadmat('mysite/media/shape_predict/uploaded/data.mat')
        input_data = np.zeros((1, 100, 3))
        x_values = list(x.values())
        x_array = np.array(x_values[-1])
        if x_array.shape != (3, 100):
            return 'data dimension is not correct, dimension should be (1,100,3)'
        else:
            input_data[None, :, :] = x_array.T
            model2 = tf.keras.models.load_model('mysite/shape_predict/models/movement_shape_predict.h5')
            d = {0: 'bad curve', 1: 'medium curve', 2: 'good curve'}
            predict_result=d[np.argmax(model2.predict(input_data))]
        return predict_result
    except Exception:
        return 'errors happen when reading uploaded data'