import pandas as pd
import urllib.request
import zipfile
from sqlalchemy import create_engine, types

datasetUrl = 'https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip'
path = 'data.zip'
csvFile = 'data.csv'

##DATA EXPORTING
urllib.request.urlretrieve(datasetUrl,path)
with zipfile.ZipFile(path) as data:
    with data.open(csvFile) as csv:
        df = pd.read_csv(csv, sep=";", decimal=',', index_col=False,usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)","Batterietemperatur in °C", "Geraet aktiv"])

#DATA RESHAPING
df = df.rename(columns = {'Temperatur in °C (DWD)': 'Temperatur', 'Batterietemperatur in °C': 'Batterietemperatur'})

def tempConversion(celcius):
    return (celcius * 9 / 5) + 32

#DATA TRANSFORMATION
df["Temperatur"] = df["Temperatur"].apply(tempConversion)
df["Batterietemperatur"] = df["Batterietemperatur"].apply(tempConversion)

#DATA VALIDATION
df = df.loc[df["Geraet"] > 0]
df = df.loc[df["Monat"] > 0]

engine = create_engine('sqlite:///temperatures.sqlite')

dtypes = {
          'Geraet': types.INTEGER,
          'Hersteller': types.TEXT,
          'Model': types.TEXT,
          'Monat': types.INTEGER,
          'Temperatur': types.FLOAT,
          'Batterietemperatur': types.FLOAT,
          'Geraet aktiv': types.TEXT,
          }
df.to_sql('temperatures', engine, if_exists='replace', index=False, dtype=dtypes)





