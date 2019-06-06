# Spark & Machine Learning Platform for Strain Movement Curve with Social Functionalities

### Author: 

Haoqiu Wu

### Operating System

Linux-CentOS 7

### Spark & ML

* Given a seires of strain movement data from a MATLAB Android Sensor in our CRN lab, I segment it into separate curves and smooth & normalize them to 100 length with amplitude from 0~1.
* Data augmentation: Calculate the first and second derivatives for those curves.
* Build two-layer LSTM RNN model.
* Fit data of curves with corresponding derivatives into this model.
* Grid search with CV.
* Store the best model.
* Use model for real-time prediction with Spark Streaming.
* Use model for prediction for uploaded data file.
* An Entertaiment Chatbot.

### Social Functionality
* Account Module
* Article Module
* Image Module
* Admin Module

### Techniques Used in this System: 

* MATLAB for Time Series Data Segmentation and Smoothing and Augmentation.
* Keras for RNN Model.
* Spark Streaming for Real-time Process for Sensor Data.
* Sklearn and NLTK for Chatbot by Word-Embedding and Cosine-Similarity.
* Python Django for Backend.
* Haystack-whoosh for Full Text Search.
* Bootstrap and jQuery and AJAX for Frontend.
* MySQL, Redis, MongoDB for Data Storage.


### Part of Screenshots

* Overall Architecture

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/overall.png)

* Main Page

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/main_page.png)

* Real-time Prediction and RNN Architecture

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/realtime_prediction.png)

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/model_archi.png)

* Chatbot

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/chatbot.png)

* Articles

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/articles.png)

* Image Detail 

![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/image_detail.png)

### How to use this program:
* Fork it.
* Install all necessary Software.
* Create virtule environment and then install all dependecies in requirements.txt
* Finally
![alt text](https://github.com/wuhaoqiu/engr597-stable/blob/Linux-Version/screenshots/start.png)




