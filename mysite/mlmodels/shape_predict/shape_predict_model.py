#author:Haoqiu Wu Time 19.4.12
from scipy.io import loadmat
import numpy as np
import tensorflow as tf

def store_file(input_data):
    print(input_data.name)
    print(input_data.content_type)
    print(input_data.size)
    if input_data.content_type !='application/octet-stream' or input_data.size > 100000:
        return False
    else:
        # overwrite the file if it exists
        with open('mysite/media/shape_predict/uploaded/data.mat', 'wb+') as destination:
            for chunk in input_data.chunks():
                destination.write(chunk)
        return True
def predict():
    try:
        x = loadmat('C:/Users/whq672437089/Envs/engr597-unstable/mysite/media/shape_predict/uploaded/data.mat')
        input_data = np.zeros((1, 100, 3))
        x_values = list(x.values())
        # usually the last element is required data
        x_array = np.array(x_values[-1])
        if x_array.shape != (3, 100):
            return 'data dimension is not correct, dimension should be (3,100)'
        else:
            input_data[None, :, :] = x_array.T
            model2 = tf.keras.models.load_model('C:/Users/whq672437089/Envs/engr597-unstable/mysite/media/shape_predict/models/movement_shape_predict.h5')
            d = {0: 'bad curve', 1: 'medium curve', 2: 'good curve'}
            # predict result
            predict_result=d[np.argmax(model2.predict(input_data))]
        return predict_result
    except Exception:
        return 'errors happen when reading uploaded data'

if __name__=='__main__':
    x = loadmat('C:/Users/whq672437089/Envs/engr597-unstable/mysite/media/shape_predict/uploaded/data.mat')
    input_data = np.zeros((1, 100, 3))
    x_values = list(x.values())
    x_array = np.array(x_values[-1])
    if x_array.shape != (3, 100):
        print('yes')
    else:
        input_data[None, :, :] = x_array.T
        model2 = tf.keras.models.load_model(
            'C:/Users/whq672437089/Envs/engr597-unstable/mysite/media/shape_predict/models/movement_shape_predict.h5')
        d = {0: 'bad curve', 1: 'medium curve', 2: 'good curve'}
        predict_result = d[np.argmax(model2.predict(input_data))]
