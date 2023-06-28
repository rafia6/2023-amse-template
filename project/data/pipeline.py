#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# In[49]:


####Extracting the Data into Dataframes####
accidents = pd.read_csv("https://offenedaten-konstanz.de/sites/default/files/Unfallatlas_Konstanz_Gesamt_2016-2019.csv")
enforcement = pd.read_csv("https://offenedaten-konstanz.de/sites/default/files/Blitzerdaten%20Jahresstatistik%202019.csv", sep=';')


# In[50]:


enforcement


# In[51]:


accidents


# In[52]:


########Cleaning the data############## 

#Dropping columns that are not needed
accidents = accidents.drop(columns=['LINREFX','LINREFY','XGCSWGS84','YGCSWGS84','STRZUSTAND','Jahr-Monat'
])


# In[53]:


#Changing column names from german to english
accidents.rename(columns = {'UnfallID':'AccidentId', 
                      'UJAHR':'Year',
                      'UMONAT':'Month',
                     'UWOCHENTAG':'Weekday',
                     'USTUNDE':'Hour',
                     'UKATEGORIE':'Category',
                     'UART':'CollisionType',
                     'UTYP1':'AccidentType',
                     'ULICHTVERH':'LightningCondition',
                     'IstRad':'IsBicycle',
                     'IstPKW':'IsPassengerCar',
                     'IstFuss':'IsFoot',
                     'IstKrad':'IsMotorcyle',
                     'IstGkfz':'IsLorry',
                     'IstSonstige':'IsOther'}, inplace = True)

enforcement.rename(columns = {'standort':'Location',
                    'monat':'Month',
                    'gemessene_fahrzeuge':'Measured_vehicle',
                    'verstoesse':'Violate',
                    'gueltige_verstoesse':'Valid_violations',
                    'verwarnungen':'Warnings',
                    'bussgelder':'Fines',
                    'max_geschwindigkeit':'Max_speed',
                    'einnahmen':'Revenue'}, inplace = True)


# In[54]:


#Filling up NA's with 0's
accidents['LightningCondition'].fillna(0, inplace = True)


# In[55]:


#Converting Month in Numerical Data
enforcement.Month =pd.Categorical(enforcement.Month,['Gesamt','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'], ordered=True)
enforcement.Month=enforcement.Month.cat.codes


# In[56]:


#Converting Location to Numerical Data
enforcement.Location=pd.Categorical(enforcement.Location,['Casino','Europabruecke','Gartenstr','Laube','Loh','Mainaustr','Moschee','gesamt'],ordered=True)
enforcement.Location = enforcement.Location.cat.codes


# In[57]:


createDb = create_engine("sqlite:///konstanz.db")


# In[58]:


####Loading the Data to SQL####

enforcement.to_sql('SpeedEnforcement', createDb, if_exists='replace')


# In[59]:


accidents.to_sql('AccidentData', createDb, if_exists='replace')


# In[ ]:




