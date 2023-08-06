"""
This module implements the main data access functionalities of I/O Sense
Author: Rishi Sharma from Faclon Labs
"""

__author__ = "Rishi Sharma, Faclon Labs Private Limited"
__email__ = "rishi.sharma@faclon.com"
__status__ = "development"

import pandas as pd
import requests
import json
import time
import datetime
import sys
import urllib3
pd.options.mode.chained_assignment = None
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import numpy as np

class Caliberation:
    
    def getsensoralias(self,device_id,df):
   
        list1 = list(df['sensor'].unique())
        raw_metadata          = dataAccess.getDeviceMetaData(self,device_id)
        sensor_spec           = 'sensors'
        header                = ['sensorId','sensorName']
        para_value_list       = []
        sen_spec_data_collect = []
        sensor_param_df = pd.DataFrame(raw_metadata[sensor_spec])
        list2 = []
        for i in list1:
            sensor_param_df1= sensor_param_df[sensor_param_df['sensorId'] == i]
            sname =  sensor_param_df1.iloc[0]['sensorName']
            df['sensor'] = df['sensor'].str.replace(i, sname+" ("+i+")")
        return df
    def getcaliberation(self,device_id,qq):
        sensor_param_df = pd.DataFrame()
        qq.sort_values("sensor", inplace = True)
        raw_metadata          = dataAccess.getDeviceMetaData(self,device_id)
        sensor_spec           = 'params'
        header                = ['sensorID','m','c','min','max','automation']
        para_value_list       = []
        sen_spec_data         = raw_metadata[sensor_spec].keys()
        sen_spec_data_collect = []
        for sensor in sen_spec_data:
            m=c=min_=max_=automation=0
            for name_value in raw_metadata[sensor_spec][sensor]:
                if name_value['paramName']=='m':
                    m=name_value['paramValue']
                if name_value['paramName']=='c':
                    c=name_value['paramValue']
                if name_value['paramName']=='min':
                    min_=name_value['paramValue']
                if name_value['paramName']=='max':
                    max_=name_value['paramValue']
                if name_value['paramName']=='automation':
                    automation=name_value['paramValue']
            sen_spec_data_collect.append([sensor,m,c,min_,max_,automation])
        sensor_param_df       = pd.DataFrame(sen_spec_data_collect, columns=header)
        sensor_data_with_meta = qq.merge(sensor_param_df, left_on='sensor', right_on='sensorID').drop('sensor', axis =1)
        
        sensor_data_with_meta["value"] = sensor_data_with_meta["value"].astype('float')
        sensor_data_with_meta["m"]     = sensor_data_with_meta["m"].astype('float')
        sensor_data_with_meta["c"]     = sensor_data_with_meta["c"].astype('int')
        sensor_data_with_meta["max"]   = sensor_data_with_meta["max"].astype('int')
        sensor_data_with_meta["min"]   = sensor_data_with_meta["min"].astype('int')
        
        sensor_data_with_meta['final_value'] = (sensor_data_with_meta['value']*sensor_data_with_meta['m']) + sensor_data_with_meta['c'] #PLEASE CHECK WHAT DO WE HAVE TO MULTIPLY I HAVE ASSUMED m
        
        sensor_data_with_meta['final_value'] = sensor_data_with_meta['final_value'].astype('float')
        sensor_data_with_meta['final_value'] = np.where(
            sensor_data_with_meta["final_value"] > sensor_data_with_meta["max"], sensor_data_with_meta["max"], sensor_data_with_meta["final_value"]
        )
        sensor_data_with_meta['final_value'] = np.where(
            sensor_data_with_meta["final_value"] < sensor_data_with_meta["min"], sensor_data_with_meta["min"], sensor_data_with_meta["final_value"]
        )
        df = sensor_data_with_meta[['time','final_value','sensorID']]
        df.rename(columns = {'time':'time','final_value':'value','sensorID':'sensor'}, inplace = True)
        return df
    
    
class dataAccess:
    
    def __init__(self, apikey, url):
        self.apikey= apikey
        self.url= url
    
    def timegrouping(self,df,bands):
        df['Time']  = pd.to_datetime(df['time'])
        df.sort_values("Time",inplace= True)
        df       = df.drop(['time'],axis=1)
        df       = df.set_index(['Time'])
        df.index = pd.to_datetime(df.index)
        df       = df.groupby(pd.Grouper(freq=str(bands)+"Min", label='right')).mean()
        df.reset_index(drop=False,inplace= True)
        return df
        
    def getcleanedtable(self,df):
        df=df.sort_values('time')
        results   = df.pivot(index='time', columns='sensor',values='value')
        results.reset_index(drop=False,inplace=True)
        return results
    
    
    def getDeviceDetails(self):
        try:
            qq       = pd.DataFrame()
            url      = "https://"+self.url+"/api/metaData/allDevices"
            header   = {'apikey': self.apikey}
            payload  = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)
            
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                rawData = json.loads(response.text)['data']
                qq      = pd.DataFrame(rawData)
                return qq
            
        except Exception as e:
            print('Failed to fetch device Details')
            print(e)

            
    def getDeviceMetaData(self,device_id):
        try:
            qq       = pd.DataFrame()
            url      = "https://"+self.url+"/api/metaData/device/"+device_id
            header   = {'apikey': self.apikey}
            payload  = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)
            
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                rawData = json.loads(response.text)['data']
                return rawData
            
        except Exception as e:
            print('Failed to fetch device Metadata')
            print(e)
            
            
    def getUserInfo(self):
        try:
            
            qq       = pd.DataFrame()
            url      = "https://"+self.url+"/api/metaData/user"
            header   = {'apikey': self.apikey}
            payload  = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)
            
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                rawData = json.loads(response.text)['data']
                return rawData     
            
        except Exception as e:
            print('Failed to fetch user Information')
            print(e)    
          
    def getDP(self,device_id, sensors=['D0'], n = None, cal = None,end_time = time.time()):
        try:
            frameCount  = 0
            lim         = n
            sub_list    = []
            
            e_time      = pd.to_datetime(end_time)
            en_time     = int(round(e_time.timestamp()))
            header      = {'apikey': self.apikey}
    
            qq          = pd.DataFrame()
            qq1         = pd.DataFrame()
            qq2         = pd.DataFrame(columns=['time','sensor','value'])
            cursor      = {'end': en_time}
            
            if n == 1:
                if len(sensors) == 1:
                    url      = "https://"+self.url+"/api/apiLayer/lastDP?device="+device_id+"&sensor=" + sensors[0]
                    payload  = {}
                    param    = 'GET'
                    response = requests.request(param, url, headers=header, data=payload, verify=False)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw['error'])
                    if 'success' in raw:
                        raise ValueError(raw['error']) 
                    if len(json.loads(response.text)) == 0:
                        raise ValueError('No Data!')
                    
                    else:
                        rawData = json.loads(response.text)
                        qq      = pd.DataFrame(rawData[0])
                        qq['sensor'] = sensors[0]
                        
                        if cal == True or cal == 'true' or cal == "TRUE":
                            df = Caliberation.getcaliberation(self,device_id,qq)
                            df = Caliberation.getsensoralias(self,device_id,df)
                        else:
                            df = qq
                            df = Caliberation.getsensoralias(self,device_id,df)
                    return df    
                
                else:
                    payload  = {"sensors":sensors}
                    url      = "https://"+self.url+"/api/apiLayer/getLastDps?device="+device_id
                    param    = 'PUT'
                    response = requests.request(param, url, headers=header, data=payload, verify=False)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw['error'])
                    if 'success' in raw:
                        raise ValueError(raw['error']) 
                    
                    elif len(json.loads(response.text)) == 0 :
                        raise ValueError('No Data!')
                    
                    else:
                        time_list = []
                        raw       = json.loads(response.text)
                        for i in raw[0]:
                            filtered = raw[0][i]
                            sub_list = sub_list + filtered
                        
                        qq = pd.DataFrame(sub_list)
                        if cal == True or cal == 'true' or cal == "TRUE":
                            df = Caliberation.getcaliberation(self,device_id,qq)
                            print(df)
                            df = Caliberation.getsensoralias(self,device_id,df)
                            df = df.sort_values('time')
                            df = df.pivot(index='time', columns='sensor',values='value')
                            df.reset_index(drop=False,inplace=True)
                        else:
                            # df = qq
                            # print(df)
                            df = Caliberation.getsensoralias(self,device_id,qq)
                            df = df.sort_values('time')
                            df = df.pivot(index='time', columns='sensor',values='value')
                            df.reset_index(drop=False,inplace=True)
                        return df
            else:
                str1          = ","
                sensor_values = str1.join(sensors)
                payload       = {}
                a             = 0 
                while True:
                    if a == 0:
                        url  = "https://"+self.url+"/api/apiLayer/getLimitedDataMultipleSensors/?device="+device_id+"&sensor="+sensor_values+"&eTime="+str(en_time)+"&lim="+str(lim)+"&cursor=true"
                    else:
                        url  = "https://"+self.url+"/api/apiLayer/getLimitedDataMultipleSensors/?device="+device_id+"&sensor="+sensor_values+"&eTime="+str(cursor['end'])+"&lim="+str(lim)+"&cursor=true"
                    response = requests.request("GET", url, headers=header, data=payload)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw['error'])
                    if 'success' in raw:
                        raise ValueError(raw['error'])    
                    if len(json.loads(response.text)['data']) == 0 :
                        raise ValueError('No Data!')
                    
                    else:
                        rawData = json.loads(response.text)['data']
                        cursor  = json.loads(response.text)['cursor']
                        a       = a+1
                        qq      = pd.DataFrame(rawData)
                        
                    if cursor['end'] == None:
                        break
                if cal == True or cal == 'true' or cal == "TRUE":
                    df  = Caliberation.getcaliberation(self,device_id,qq)
                    df = Caliberation.getsensoralias(self,device_id,df)
                    df  = dataAccess.getcleanedtable(self,qq)
                else:
                    df = Caliberation.getsensoralias(self,device_id,qq)
                    df = dataAccess.getcleanedtable(self,df)
            return df
        except Exception as e:
            print(e)    
     
    
    def dataQuery(self, device_id, start_time, end_time = time.time(), sensors = None , cal = None,bands=None,echo=True):
        try:
            df = pd.DataFrame()
            s_time      = pd.to_datetime(start_time)
            st_time     = int(round(s_time.timestamp())) * 1000000000
            e_time      = pd.to_datetime(end_time)
            en_time     = int(round(e_time.timestamp())) * 1000000000
            header      = {'apikey': self.apikey}
            payload     = {}
            qq          = pd.DataFrame()
            rawdata_res = []
            
            if sensors is None:
                url     = "https://"+self.url+"/api/apiLayer/getDataByStEt?device="
            else:
                if len(sensors) == 1:
                    url = "https://"+self.url+"/api/apiLayer/getData?device="
                else:
                    url = "https://"+self.url+"/api/apiLayer/getAllData?device="
                    
            a      = 0 
            cursor = {'start': st_time, 'end': en_time}  
            
            while True:
                if echo == True:
                    for i in range(a):
                        sys.stdout.write('\r')
                        sys.stdout.write("Approx Records Fetched %d" % (10000*i))
                        # sys.stdout.write("[%-30s] %d%%" % ('='*i, 1*i))
                        sys.stdout.flush() 
                if sensors is None:
                    if a == 0:
                        temp = url +device_id+"&sTime="+str(st_time)+"&eTime="+str(en_time)+"&cursor=true"
                    else:
                        temp = url+device_id+"&sTime="+str(cursor['start'])+"&eTime="+str(cursor['end'])+"&cursor=true"
                if sensors != None:
                    if a == 0:
                        str1          = ","
                        sensor_values = str1.join(sensors)
                        temp          = url+device_id+"&sensor="+sensor_values+"&sTime="+str(st_time)+"&eTime="+str(en_time)+"&cursor=true"
                    else:
                        str1          = ","
                        sensor_values = str1.join(sensors)
                        temp          = url+device_id+"&sensor="+sensor_values+"&sTime="+str(cursor['start'])+"&eTime="+str(cursor['end'])+"&cursor=true"
                        
                response = requests.request("GET", temp, headers=header, data=payload)
                raw = json.loads(response.text)
                if response.status_code != 200:
                    raise ValueError(raw['error'])
                if 'success' in raw:
                    raise ValueError(raw['error']) 
                if len(json.loads(response.text)['data']) == 0 :
                    raise ValueError('No Data!')
                    
                else:
                    ArithmeticError
                    rawData     = json.loads(response.text)['data']
                    cursor      = json.loads(response.text)['cursor']
                    rawdata_res = rawdata_res + rawData   
                    a           = a + 1
                    qq          = pd.DataFrame(rawdata_res)
                   
                if cursor['start'] == None or cursor['end'] == None:
                   
                    break
            if len(qq.columns) == 2:
                    qq['sensor'] = sensors[0]
                    
            if cal == True or cal == 'true' or cal == "TRUE":
                
                df = Caliberation.getcaliberation(self,device_id,qq)
                df = Caliberation.getsensoralias(self,device_id,df)
                df = dataAccess.getcleanedtable(self,df)
            else:
                # print(qq)
                df = Caliberation.getsensoralias(self,device_id,qq)
                df = dataAccess.getcleanedtable(self,qq)
            
            if bands != None:
                df = dataAccess.timegrouping(self,df,bands)
           
            return df
                       
        except Exception as e:
            # print('Failed to fetch Data')
            print(e)    
    
