from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import numpy as np
import keras
from datetime import datetime,date
import pymongo
# "/root/github/engr597-v3/engr597-stable/mysite/media/shape_predict/models/movement_shape_predict.h5"
keras_model_path='/root/spark/spark-2.3.3-bin-hadoop2.7/scripts/models/movement_shape_predict.h5'
batch_interval=2.7
where_to_scan='/root/jupyter/data/'
dbname='movement_shape_predict'
# colname=date.today().strftime('%Y-%m-%d')
colname='movement_shape_predict'

"""
MongoDB connection part
"""
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print('fail to connect to mongodb, pls check connection')
    
#collection in databases is named by current date
mydb=myclient[dbname]
collist=mydb.list_collection_names()
mycol = mydb[colname]# if not exit, mongodb create one for you
if not (colname in collist):
  mycol.insert_one({'time':'test','data':'test','result':'test'})
"""
End of mongodb part
"""

"""
keras model part
"""
keras.backend.clear_session()
pre_trained_model=keras.models.load_model(keras_model_path)
#fix thread bug in keras
pre_trained_model._make_predict_function()
d = {0: 'bad curve', 1: 'medium curve', 2: 'good curve'}
# model input shape is 100,3, so create one container as preparation
input_data=np.zeros((1,100,3))
"""
end of keras model part
"""
# make sure data stores in mongodb has correct dimension and data type
def saveRDD(rdd):
  l=rdd.collect()
  if len(l)==3:
    try:
      data_nparray=np.array([float(val) for line in l for val in line.rstrip().split(' ') if len(val)>1])
      # because after spark read txt file, the format of l is ['1 2','3 4','5 6'],
      # each line is a string separate by space, so need to convert it to numeric values
      if len(data_nparray)==300:
        data_nparray=data_nparray.reshape((3,100))
        print(data_nparray.shape)
        input_data[None,:,:]=data_nparray.T
        # predict result
        predict_result=d[np.argmax(pre_trained_model.predict(input_data))]
        print(predict_result)
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_nparray=data_nparray.reshape((1,300))
        string_data=np.array2string(data_nparray, precision=5, separator=',',suppress_small=False)
        data_dict={'time':time,'data':string_data,'result':predict_result}
        x=mycol.insert_one(data_dict)
        if x:
          print('insert correctly')
        else:
          print('fail to insert')
      else:
        print('Input dimension wrong, dim should be (3,100)')
    except:
      print('fail to convert data from string to float, may contain empty value')
  elif len(l)==0 :
    pass
  else:
    print('wrong dimension,dim should be (3,100)')
sc = SparkContext("local[2]", "Shape_Data_Scan")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, batch_interval)
movement_data=ssc.textFileStream(where_to_scan)
movement_data.foreachRDD(saveRDD)
ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate

#assume in $SPARK_HOME
#./bin/spark-submit scripts/spark_task.py
