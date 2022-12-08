from fastapi import FastAPI
import xgboost as xgb
import pandas as pd
import numpy as np


app = FastAPI()

#model_path = '/home/thomas/code/kynnesia/solar-panel-efficiency/python_files/api/model/model_3.json'

#loaded_model = pickle.load(open(model_path, 'rb'))

#model = xgb.XGBRegressor()
#model.load_model(model_path)

model = xgb.XGBRegressor(alpha = 90.0,
                         colsample_bylevel=0.93,
                         colsample_bytree=0.5,
                         grow_policy = 'lossguide',
                         reg_lambda = 1.2,
                         learning_rate = 0.13,
                         max_depth = 13,
                         min_child_weight = 4,
                         n_estimators = 250,
                         objective = 'reg:squarederror',
                         refresh_leaf = 1,
                         scale_pos_weight = 29,
                         gamma=0.0)

X = pd.read_csv('python_files/api/model/X.csv')
y = pd.read_csv('python_files/api/model/y.csv')

y = y['production']
X = X.drop(columns= ['Unnamed: 0'], axis=1)


model.fit(X,y)

@app.get('/predict')
def predict (latitude:float,
            longitude : float,
            temperature_2m_max : float,
            temperature_2m_min : float,
            precipitation_sum : float,
            rain_sum : float,
            snowfall_sum: float,
            precipitation_hours: float,
            sun_hours: float,
            windspeed_10m_max: float,
            windgusts_10m_max: float,
            winddirection_10m_dominant:float,
            shortwave_radiation_sum:float,
            et0_fao_evapotranspiration :float,
            altitude :float,
            solrad :float) :
    input_data = pd.DataFrame(
            {
            'latitude' : [latitude],
            'longitude' : [longitude],
            'temperature_2m_max' : [temperature_2m_max],
            'temperature_2m_min' : [temperature_2m_min],
            'precipitation_sum' : [precipitation_sum],
            'rain_sum' : [rain_sum],
            'snowfall_sum': [snowfall_sum],
            'precipitation_hours': [precipitation_hours],
            'sun hours': [sun_hours],
            'windspeed_10m_max': [windspeed_10m_max],
            'windgusts_10m_max': [windgusts_10m_max],
            'winddirection_10m_dominant':[winddirection_10m_dominant],
            'shortwave_radiation_sum':[shortwave_radiation_sum],
            'et0_fao_evapotranspiration' :[et0_fao_evapotranspiration],
            'altitude' :[altitude],
            'solrad' : [solrad]})
    prediction = model.predict(input_data)
    return {'prediction': np.exp(float(prediction[0]))}
