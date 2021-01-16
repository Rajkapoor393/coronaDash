from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import requests

# Create your views here.
df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

# Scraping data from worldometer
r = requests.get('https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/')
dfs = pd.read_html(r.text)
confirmedGlobal = dfs[0].iloc[:,:-1]
countries = confirmedGlobal['Country']
def index(request):
    TotalCount = sum(confirmedGlobal['Cases'])
    countryName = confirmedGlobal['Country'].values.tolist()
    countryValue = confirmedGlobal['Cases'].values.tolist()
    dataForMap = getDataforMap(countries,confirmedGlobal)
    maxVal=max(countryValue)
    logVals=list(np.log(ind) if ind != 0 else 0 for ind in countryValue )
    dataForMapGraph=getDataforMap(countries,confirmedGlobal)
    context = {'TotalCount':TotalCount, 'maxVal':maxVal,'logVals':logVals,'dataForMapGraph':dataForMapGraph,'countryName':countryName,'countryValue':countryValue, 'dataForMap':dataForMap}
    return render(request,'index.html',context)


def getDataforMap(countries,confirmedGlobal):
    dataForMap=[]
    for i in countries:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=confirmedGlobal[confirmedGlobal['Country']==i]['Cases'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap
