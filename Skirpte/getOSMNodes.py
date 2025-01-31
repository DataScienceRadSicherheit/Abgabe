import pandas as pd
import requests
import time
import numpy as np

#df = pd.read_csv('Radunfaelle_Leipzig_2016-2023.csv', delimiter=";")
df = pd.read_csv('Radunfaelle_Augsburg_2016-2023.csv', delimiter=";")

print(df)

for index, row in df.iterrows():
    PARAMS = {'format':"json", 'lat': row['YGCSWGS84'].replace(",", "."), 'lon': row['XGCSWGS84'].replace(",", "."), 'zoom': 17}
    url = "http://localhost:8080/reverse"
    result = requests.get(url = url, params = PARAMS)
    print(result.status_code)
    data = result.json()
    print(data)
    df.loc[index, ["place_id"]] = data['place_id']
    df.loc[index, ["osm_id"]] = data['osm_id']
    time.sleep(200 / 1000)
    print(index, data['place_id'], data['osm_id'])

print(df)
 
df.to_csv('out_augsburg.csv', index=False)  

np.savetxt('out_augsburg.txt', df['osm_id'].values, fmt='%d')