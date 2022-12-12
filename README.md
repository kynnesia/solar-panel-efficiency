# SunSight 🔋🛰
## 🌄 Improving Solar Panel Efficiency

A model: 
* __that__ predicts solar energy generation in any location, 
* __that__ +90% of the time predicts it correctly, and
* __that__ can be scalable worldwide.

## 📚 Context
We have seen that Renewables are growing.  
One of them being Solar Energy.  
And the required investments that these imply.  

To avoid spending millions in solar stations that, in the end, could not be optimal (as it happened with the Crescent Dunes, where 1,000M dollars were spent), we have created a model that enables data-driven decision making.

## 📊 The model
The model is an XGB regressor with more than 15 features. Most of them being weather-related, but also considering Solar Radiation, and Elevation.  
The model explains more than 90% of the variation in the energy generated. That was calculated using a cross-validation in the test-set of the dataframe. So, no data leakage. 

## The result
We created a web page using Streamlit, in which we showed where it would be most optimal to set up a solar panel in Spain. We did more than 8,000 predictions, and you can check the results on the following page.  
Moreover, we created a page directly linked through an API, where any point of the world can be chosen (if the API can collect the information needed), and __predict which would be the energy generated in an average-size solar station per year__. 

[Sunsight Website](https://kynnesia-solar-panel-efficiency-apphome-final-front-end-1854c0.streamlit.app/)



